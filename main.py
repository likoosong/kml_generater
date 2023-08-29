import os
import sys
import time
import traceback

import simplekml
import qtawesome
from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg
from PyQt5.QtGui import QColor
from pyqt_toast import Toast

from settings.qss_style import LEFT_WIDGET_STYLE_SHEET, RIGHT_WIDGET_STYLE_SHEET

from view.point_around_interface import PointAroundView
from view.point_center_interface import PointCenterView
from view.point_day24_interface import PointDay24View
from view.point_ring_interface import PointRingView
from view.line_tour_interface import LineTourView
from view.polygon_region_interface import PolygonRegionView
from view.polygon_change_interface import PolygonChangeView
from view.polygon_latlonaltbox_interface import PolygonLatLonaltBoxView
from view.polygon_show_hide_interface import PolygonShowHideView
from view.follow_me_interface import FollowMeView

class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(960, 700)
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        # ======================左侧导航栏====================================================
        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout)  # 设置左侧部件布局为网格

        # ======================右侧底图====================================================
        # self.right_widget = QtWidgets.QWidget()  # 创建右侧部件
        self.right_widget = QtWidgets.QStackedWidget()  # Renamed to right_widget
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout)  # 设置右侧部件布局为网格

        self.main_layout.addWidget(self.left_widget, 0, 0, 12, 2)  # 左侧部件在第0行第0列，占8行3列  (跨行的控件，起始行，起始列，跨越的行数，跨越列数)
        self.main_layout.addWidget(self.right_widget, 0, 2, 12, 10)  # 右侧部件在第0行第3列，占8行9列

        self.left_close = QtWidgets.QPushButton("x")  # 关闭按钮
        self.left_visit = QtWidgets.QPushButton("")  # 空白按钮
        self.left_mini = QtWidgets.QPushButton("-")  # 最小化按钮

        self.left_close.setFixedSize(15, 15)
        self.left_visit.setFixedSize(15, 15)
        self.left_mini.setFixedSize(15, 15)
        self.left_close.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}'''
        )
        self.left_visit.setStyleSheet(
            '''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}'''
        )
        self.left_mini.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}'''
        )

        self.left_label_1 = QtWidgets.QPushButton("坐标浏览")
        self.left_label_1.setObjectName('left_label')
        self.left_label_2 = QtWidgets.QPushButton("线路浏览")
        self.left_label_2.setObjectName('left_label')
        self.left_label_3 = QtWidgets.QPushButton("多边区域")
        self.left_label_3.setObjectName('left_label')
        self.left_label_4 = QtWidgets.QPushButton("联系与帮助")
        self.left_label_4.setObjectName('left_label')

        self.left_button_1 = QtWidgets.QPushButton(qtawesome.icon('fa.envira', color='white'), "环绕浏览")
        self.left_button_1.setObjectName('left_button')
        self.left_button_2 = QtWidgets.QPushButton(qtawesome.icon('fa.circle-o', color='white'), "四顾浏览")
        self.left_button_2.setObjectName('left_button')
        self.left_button_3 = QtWidgets.QPushButton(qtawesome.icon('fa.clock-o', color='white'), "缩时环景")
        self.left_button_3.setObjectName('left_button')
        self.left_button_4 = QtWidgets.QPushButton(qtawesome.icon('fa.eercast', color='white'), "圆饼环图")
        self.left_button_4.setObjectName('left_button')
        self.left_button_5 = QtWidgets.QPushButton(qtawesome.icon('fa.cab', color='white'), "线路浏览")
        self.left_button_5.setObjectName('left_button')

        self.left_button_6 = QtWidgets.QPushButton(qtawesome.icon('fa.grav', color='white'), "省市县区")
        self.left_button_6.setObjectName('left_button')
        self.left_button_7 = QtWidgets.QPushButton(qtawesome.icon('fa.download', color='white'), "形状变化")
        self.left_button_7.setObjectName('left_button')
        # <i class="fa-duotone fa-person-fairy"></i>
        self.left_button_11 = QtWidgets.QPushButton(qtawesome.icon('fa.vimeo', color='white'), "显示隐藏")
        self.left_button_11.setObjectName('left_button')
        self.left_button_10 = QtWidgets.QPushButton(qtawesome.icon('fa.xing-square', color='white'), "区域显示")
        self.left_button_10.setObjectName('left_button')

        self.left_button_8 = QtWidgets.QPushButton(qtawesome.icon('fa.star', color='white'), "关注我们")
        self.left_button_8.setObjectName('left_button')
        self.left_button_9 = QtWidgets.QPushButton(qtawesome.icon('fa.question', color='white'), "遇到问题")
        self.left_button_9.setObjectName('left_button')

        self.left_layout.addWidget(self.left_mini, 0, 0, 1, 1)   # 最小化   第一行 第一列 占用的行数 占用的列数
        self.left_layout.addWidget(self.left_visit, 0, 1, 1, 1)  # 浏览
        self.left_layout.addWidget(self.left_close, 0, 2, 1, 1)  # 关闭

        self.left_layout.addWidget(self.left_label_1, 1, 0, 1, 3)   # 一级标题 坐标浏览
        self.left_layout.addWidget(self.left_button_1, 2, 0, 1, 3)  # 二级标题 环绕浏览
        self.left_layout.addWidget(self.left_button_2, 3, 0, 1, 3)  # 二级标题 四顾浏览
        self.left_layout.addWidget(self.left_button_3, 4, 0, 1, 3)  # 二级标题 缩时环景
        self.left_layout.addWidget(self.left_button_4, 5, 0, 1, 3)  # 二级标题 圆环饼图

        self.left_layout.addWidget(self.left_label_2, 6, 0, 1, 3)  # 一级标题 线路浏览
        self.left_layout.addWidget(self.left_button_5, 7, 0, 1, 3)  # 二级标题 线路浏览

        self.left_layout.addWidget(self.left_label_3, 8, 0, 1, 3)  # 一级标题 多变区域
        self.left_layout.addWidget(self.left_button_6, 9, 0, 1, 3)  # 二级标题 省市县区
        self.left_layout.addWidget(self.left_button_7, 10, 0, 1, 3)  # 二级标题 形状变化
        self.left_layout.addWidget(self.left_button_11, 11, 0, 1, 3)  # 二级标题 显示隐藏
        self.left_layout.addWidget(self.left_button_10, 12, 0, 1, 3)  # 二级标题 区域渐显

        self.left_layout.addWidget(self.left_label_4, 13, 0, 1, 3)   # 一级标题 联系与帮助
        self.left_layout.addWidget(self.left_button_8, 14, 0, 1, 3)  # 二级标题 关注我们
        self.left_layout.addWidget(self.left_button_9, 15, 0, 1, 3)  # 二级标题 省市县区

        self.right_widget.addWidget(PointCenterView())
        self.right_widget.addWidget(PointAroundView())
        self.right_widget.addWidget(PointDay24View())
        self.right_widget.addWidget(PointRingView())
        self.right_widget.addWidget(LineTourView())
        self.right_widget.addWidget(PolygonRegionView())
        self.right_widget.addWidget(PolygonChangeView())
        self.right_widget.addWidget(PolygonShowHideView())
        self.right_widget.addWidget(PolygonLatLonaltBoxView())
        self.right_widget.addWidget(FollowMeView())

        # ======================右侧表格的样式=== ========================================================
        self.left_widget.setStyleSheet(LEFT_WIDGET_STYLE_SHEET)        # 主界面 - 左侧导航栏样式
        self.right_widget.setStyleSheet(RIGHT_WIDGET_STYLE_SHEET)

        # ======================左侧导航栏被点击===========================================================
        self.left_close.clicked.connect(self.close_window)  # 关闭按钮
        self.left_mini.clicked.connect(self.minimize_window)  # 最小化按钮

        # Connect buttons to the switch_to_subpage method using lambda functions
        self.left_button_1.clicked.connect(lambda: self.switch_to_subpage(1))   # 环绕浏览
        self.left_button_2.clicked.connect(lambda: self.switch_to_subpage(0))   # 四顾浏览
        self.left_button_3.clicked.connect(lambda: self.switch_to_subpage(2))   # 缩时环景
        self.left_button_4.clicked.connect(lambda: self.switch_to_subpage(3))   # 圆环饼图
        self.left_button_5.clicked.connect(lambda: self.switch_to_subpage(4))   # 线路浏览
        self.left_button_6.clicked.connect(lambda: self.switch_to_subpage(5))   # 行政区域
        self.left_button_7.clicked.connect(lambda: self.switch_to_subpage(6))   # 区域动画
        self.left_button_11.clicked.connect(lambda: self.switch_to_subpage(7))  # 显示隐藏(相机)
        self.left_button_10.clicked.connect(lambda: self.switch_to_subpage(8))  # 显示隐藏(非相机)
        self.left_button_8.clicked.connect(lambda: self.switch_to_subpage(9))   # 关于我们

        self.left_button_9.clicked.connect(self.open_webpage)  # 连接到open_webpage方法

        self.switch_to_subpage(1)  # Call switch_to_subpage directly to show Subpage 1
        self.main_layout.setSpacing(0)  # 设置网格布局层中部件的间隙
        # ======================主控件  观看====================================================
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件
        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框


    def open_webpage(self):
        # 打开特定的URL

        QtGui.QDesktopServices.openUrl(QtCore.QUrl('https://space.bilibili.com/153276950'))

    def switch_to_subpage(self, index):
        print(index, '='*100)
        self.right_widget.setCurrentIndex(index)

    def close_window(self):
        # Close the window when the close button is clicked
        self.close()

    def minimize_window(self):
        # Minimize the window when the minimize button is clicked
        # self.setWindowState(QtCore.Qt.WindowMinimized)
        self.showMinimized()


    # def enterEvent (self, event):   # =鼠标进入控件事件
    #     print("========鼠标进入控件事件==================")
    #     now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    #     if now > EXPIRED_DATE:
    #         QtWidgets.QMessageBox.warning(self, "提示", EXPIRED_WARN)
    #         self.close()


    # 重写三个方法使我们的Example窗口支持拖动,上面参数window就是拖动对象
    def mousePressEvent(self, event):  # 鼠标长按事件

        if event.buttons() == QtCore.Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent):  # 鼠标移动事件
        if QtCore.Qt.LeftButton and self.m_drag:
            self.move(QMouseEvent.globalPos() - self.m_DragPosition)
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):  # 鼠标释放事件
        self.m_drag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def paintEvent(self, ev):  # 重绘窗口边框线条
        painter = QtGui.QPainter(self)
        painter.begin(self)
        gradient = QtGui.QLinearGradient(QtCore.QRectF(self.rect()).topLeft(), QtCore.QRectF(self.rect()).bottomLeft())
        # gradient.setColorAt(0.0, QtCore.Qt.black)
        gradient.setColorAt(0.5, QtCore.Qt.darkGray)
        # gradient.setColorAt(0.7, QtCore.Qt.)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setBrush(gradient)
        painter.setPen(QtCore.Qt.transparent)
        painter.drawRoundedRect(self.rect(), 10.0, 10.0)
        painter.end()


def main():
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
