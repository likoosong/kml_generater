import traceback
import requests
from PyQt5 import QtCore, QtGui, QtWidgets

from settings.model import BilibiliUser


class HoverDelegate(QtWidgets.QStyledItemDelegate):
    def paint(self, painter, option, index):
        # 如果当前行处于悬停状态，则修改其样式
        if option.state & QtWidgets.QStyle.State_MouseOver:
            option.palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(220, 220, 220))
            option.state |= QtWidgets.QStyle.State_Selected
        super(HoverDelegate, self).paint(painter, option, index)


class FollowMeView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.last_selected_row = -1  # 用于存储上一次选中的行


    def setup_ui(self):
        # ======================右侧点击-区域渐显====================================================
        self.right_bar_follow_me_widget = QtWidgets.QWidget()  # 右侧顶部搜索框部件
        self.right_bar_follow_me_layout = QtWidgets.QGridLayout()  # 右侧顶部搜索框网格布局
        self.right_bar_follow_me_widget.setLayout(self.right_bar_follow_me_layout)

        self.right_bar_follow_me_title = QtWidgets.QPushButton("优质博主")
        self.right_bar_follow_me_title.setObjectName("right_lable_title")

        # Create the table
        self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.setStyleSheet("""
            /* 奇数行悬停颜色 */
            QTableWidget::item:hover {
                background-color: #A9A9A9;
            }
            /* 偶数行悬停颜色 */
            QTableWidget::item:alternate:hover {
                background-color: #A9A9A9;
            }
            /* 选中时的颜色 */
            QTableWidget::item:selected {
                background-color: #A9A9A9;
            }
            /* 滚动条的整体样式 */
            QScrollBar:vertical {
                border: 2px solid grey;  /* 滚动条的边框颜色 */
                background: #f1f1f1;  /* 滚动条的背景色 */
                width: 15px;  /* 滚动条的宽度 */
                margin: 15px 0 15px 0;  /* 滚动条的边距 */
            }
        """)

        # 设置表格的交替行颜色功能，使偶数行和奇数行的背景颜色有所不同，增强可读性
        self.tableWidget.setAlternatingRowColors(True)
        # 开启鼠标跟踪，这样即使没有点击鼠标按钮，QWidget也会接收到鼠标移动事件
        self.tableWidget.setMouseTracking(True)
        # 设置一个自定义的委托（Delegate）以处理单元格的悬停事件和绘制
        self.tableWidget.setItemDelegate(HoverDelegate(self.tableWidget))

        # Set the number of rows and columns
        self.tableWidget.setRowCount(15)  # 10 rows for this example
        self.tableWidget.setColumnCount(5)  # 4 columns for "姓名", "粉丝", "关注数", "投稿数量"
        self.tableWidget.setHorizontalHeaderLabels(['姓名', '粉丝', '获赞', '播放', '投稿'])

        # 设置列宽
        self.tableWidget.setColumnWidth(0, 150)  # Set width for "姓名" column
        self.tableWidget.setColumnWidth(1, 140)  # Set width for "粉丝" column
        self.tableWidget.setColumnWidth(2, 140)  # Set width for "粉丝" column
        self.tableWidget.setColumnWidth(3, 140)  # Set width for "获赞" column
        self.tableWidget.setColumnWidth(4, 140)  # Set width for "播放" column
        # self.tableWidget.setColumnWidth(5, 100)  # Set width for "投稿" column
        # self.tableWidget.setColumnWidth(6, 100)  # Set width for "时间" column

        # 按“粉丝”栏排序
        self.tableWidget.sortItems(1, QtCore.Qt.DescendingOrder)
        # 设置默认列高
        self.tableWidget.verticalHeader().setDefaultSectionSize(32)
        # 设置垂直表头不可移动
        self.tableWidget.verticalHeader().setSectionsMovable(False)
        # 设置水平表头不可移动
        self.tableWidget.horizontalHeader().setSectionsMovable(False)
        # 设置水平表头的每一列的大小不可通过拖动来改变
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        # 设置垂直表头的每一行的大小不可通过拖动来改变
        self.tableWidget.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        # 设置表格中的项目不可编辑
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # 设置水平滚动条策略为始终关闭，这意味着水平滚动条将永远不会显示，无论内容是否超出视图
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.right_bar_follow_me_layout.addWidget(self.right_bar_follow_me_title, 0, 0, 1, 1)  # (跨行的控件，起始行，起始列，跨越的行数，跨越列数)
        self.right_bar_follow_me_layout.addWidget(self.tableWidget, 1, 0, 2, 7)  # Add at position 0,0 in the grid layout

        # 渲染表格的内容
        self.populate_table()

        self.tableWidget.itemEntered.connect(self.on_item_hovered)
        self.tableWidget.cellPressed.connect(self.on_item_pressed)
        # 跳转到新的用户bilibili的首页
        self.tableWidget.cellClicked.connect(self.open_user_webpage)

        self.setLayout(self.right_bar_follow_me_layout)

    def on_item_hovered(self, item):
        self.tableWidget.selectRow(item.row())

    def on_item_pressed(self, row, _):
        # 设置为整行选择模式
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        # 如果之前有选中的行，恢复其默认样式并取消其选中状态
        if self.last_selected_row >= 0:
            for col in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(self.last_selected_row, col)
                if not item:  # 如果单元格没有item，为它创建一个
                    item = QtWidgets.QTableWidgetItem()
                    self.tableWidget.setItem(self.last_selected_row, col, item)
                item.setBackground(QtGui.QColor(255, 255, 255))  # 恢复默认背景色
            self.tableWidget.setRangeSelected(
                QtWidgets.QTableWidgetSelectionRange(self.last_selected_row, 0, self.last_selected_row,self.tableWidget.columnCount() - 1),False)

        # 为新选中的行设置蓝色背景并选择它
        for col in range(self.tableWidget.columnCount()):
            item = self.tableWidget.item(row, col)
            if not item:  # 如果单元格没有item，为它创建一个
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget.setItem(row, col, item)
            item.setBackground(QtGui.QColor(128, 128, 128))  # 蓝色背景
        self.tableWidget.setRangeSelected(QtWidgets.QTableWidgetSelectionRange(row, 0, row, self.tableWidget.columnCount() - 1),True)

        # 保存当前选中的行索引
        self.last_selected_row = row

    def open_user_webpage(self, row, column):
        # Ensure the first column (nickname) was clicked
        if column == 0:
            item = self.tableWidget.item(row, column)
            if item:
                mid = item.data(QtCore.Qt.UserRole)
                # Now use the `mid` to open the webpage
                url = f"https://space.bilibili.com/{mid}"
                QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))

    def fetch_image_from_url(self, url, size=QtCore.QSize(50, 50)):  # 默认尺寸为50x50
        response = requests.get(url)
        image = QtGui.QPixmap()
        image.loadFromData(response.content)
        # 调整图片的尺寸
        image = image.scaled(size, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        # 创建一个与图片相同大小的空 QPixmap，背景透明
        mask = QtGui.QPixmap(image.size())
        mask.fill(QtCore.Qt.transparent)
        # 在遮罩上绘制一个填充的白色圆形
        painter = QtGui.QPainter(mask)
        painter.setBrush(QtGui.QBrush(QtCore.Qt.white))
        painter.drawEllipse(0, 0, image.width(), image.height())
        painter.end()
        # 将遮罩应用到图片上
        image.setMask(mask.mask())
        return QtGui.QIcon(image)

    def populate_table(self):

        data = BilibiliUser.select(
            BilibiliUser.nickname, BilibiliUser.mid, BilibiliUser.face,
            BilibiliUser.face, BilibiliUser.fans, BilibiliUser.likes, BilibiliUser.video
        ).dicts()

        self.tableWidget.setRowCount(len(data))

        for row_idx, user_data in enumerate(data):
            icon = self.fetch_image_from_url(user_data['face'], QtCore.QSize(32, 32))
            item = QtWidgets.QTableWidgetItem(user_data['nickname'])
            item.setIcon(icon)
            item.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)  # 左对齐并垂直居中
            item.setData(QtCore.Qt.UserRole, user_data['mid'])
            # item.setForeground(QtGui.QBrush(QtGui.QColor(0, 0, 255)))
            self.tableWidget.setItem(row_idx, 0, item)

            item = QtWidgets.QTableWidgetItem(str(user_data['fans']))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(row_idx, 1, item)

            item = QtWidgets.QTableWidgetItem(str(user_data['likes']))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(row_idx, 2, item)

            item = QtWidgets.QTableWidgetItem(str(user_data['video']))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(row_idx, 4, item)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = FollowMeView()
    window.show()
    app.exec_()

# 设置鼠标跟踪开启
# self.tableWidget.setMouseTracking(True)
# self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
# self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

# 当鼠标进入某个单元格时，选择该单元格所在的整行
# self.tableWidget.cellEntered.connect(self.tableWidget.selectRow)
# 设置为整行选择模式
# self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

# 按“粉丝”栏排序：要按“粉丝”列（即列索引 1）升序排序，可以使用
# self.tableWidget.sortItems(1, QtCore.Qt.AscendingOrder)

# 按“粉丝”栏排序：对于降序排列：，可以使用
# self.tableWidget.sortItems(1, QtCore.Qt.DescendingOrder)
