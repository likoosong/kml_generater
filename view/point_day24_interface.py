from PyQt5 import QtCore, QtGui, QtWidgets

from utlis.util import random_content
from utlis.show_toast_interface import Toast, AlertLevel
from tour.tour_point_day24 import TourPointDay24

class PointDay24View(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        # ======================右侧点击-缩时环图====================================================
        self.right_bar_point_day24_widget = QtWidgets.QWidget()  # 右侧顶部搜索框部件
        self.right_bar_point_day24_layout = QtWidgets.QGridLayout()  # 右侧顶部搜索框网格布局
        self.right_bar_point_day24_widget.setLayout(self.right_bar_point_day24_layout)

        self.right_bar_tour_point_day24 = QtWidgets.QPushButton("缩时环景")
        self.right_bar_tour_point_day24.setObjectName("right_lable_title")

        # 坐标浏览 缩时环景 名称输入框
        self.right_bar_tour_point_day24_kmlname = QtWidgets.QLabel('名称  Kmlname')
        self.right_bar_tour_point_day24_kmlname.setObjectName("right_bar_tour_label")
        self.right_bar_widget_point_day24_kmlname_input = QtWidgets.QLineEdit()
        self.right_bar_widget_point_day24_kmlname_input.setText('上海东方明珠')
        self.right_bar_widget_point_day24_kmlname_input.setPlaceholderText("输入要保存的文件名")
        self.right_bar_widget_point_day24_kmlname_input.setObjectName('right_bar_widget_qlinedit_input')

        # 坐标浏览 缩时环景 经度输入框
        self.right_bar_tour_point_day24_longitude = QtWidgets.QLabel('经度  Longitude')  # 文字栏
        self.right_bar_tour_point_day24_longitude.setObjectName("right_bar_tour_label")
        self.right_bar_widget_point_day24_longitude_input = QtWidgets.QLineEdit()  # 输入框栏
        self.right_bar_widget_point_day24_longitude_input.setText('121.4822068677437')
        self.right_bar_widget_point_day24_longitude_input.setPlaceholderText("输入经度 85 <= xx.xxxxx => -85")
        self.right_bar_widget_point_day24_longitude_input.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_widget_point_day24_longitude_input_holder = QtWidgets.QLabel("输入经度 十进制度小数")  # 提示栏
        self.right_bar_widget_point_day24_longitude_input_holder.setObjectName("right_bar_widget_holder")

        # 坐标浏览 缩时环景 纬度输入框
        self.right_bar_tour_point_day24_latitude = QtWidgets.QLabel('纬度  Latitude')  # 文字栏
        self.right_bar_tour_point_day24_latitude.setObjectName("right_bar_tour_label")
        self.right_bar_widget_point_day24_latitude_input = QtWidgets.QLineEdit()  # 输入框栏
        self.right_bar_widget_point_day24_latitude_input.setText('31.24177813485763')
        self.right_bar_widget_point_day24_latitude_input.setPlaceholderText("输入纬度 180 <= xxx.xxxxx => -180")
        self.right_bar_widget_point_day24_latitude_input.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_widget_point_day24_latitude_input_holder = QtWidgets.QLabel("输入纬度 十进制度小数")  # 提示栏
        self.right_bar_widget_point_day24_latitude_input_holder.setObjectName("right_bar_widget_holder")

        # 坐标浏览 缩时环景 圆外半径   Altitude
        self.right_bar_tour_point_day24_altitude = QtWidgets.QLabel('高度  Altitude')  # 文字栏
        self.right_bar_tour_point_day24_altitude.setObjectName("right_bar_tour_label")
        self.right_bar_widget_point_day24_altitude_input = QtWidgets.QLineEdit()  # 输入框栏
        self.right_bar_widget_point_day24_altitude_input.setText('200')
        self.right_bar_widget_point_day24_altitude_input.setPlaceholderText("高度")
        self.right_bar_widget_point_day24_altitude_input.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_widget_point_day24_altitude_input_holder = QtWidgets.QLabel("相对于地面 xxx >= 10")  # 提示栏
        self.right_bar_widget_point_day24_altitude_input_holder.setObjectName("right_bar_widget_holder")

        # 坐标浏览 缩时环景 下载
        self.right_bar_widget_point_day24_button_download = QtWidgets.QPushButton()
        self.right_bar_widget_point_day24_button_download.setText("确定")
        self.right_bar_widget_point_day24_button_download.setObjectName('right_bar_tour_button_download')
        self.right_bar_widget_point_day24_placeholder = QtWidgets.QLabel("")  # 占位符

        self.right_bar_point_day24_layout.addWidget(self.right_bar_tour_point_day24, 0, 0, 1,
                                                    1)  # (跨行的控件，起始行，起始列，跨越的行数，跨越列数)
        self.right_bar_point_day24_layout.addWidget(self.right_bar_tour_point_day24_kmlname, 0, 0, 4, 1)
        self.right_bar_point_day24_layout.addWidget(self.right_bar_widget_point_day24_kmlname_input, 0, 1, 4, 3)
        self.right_bar_point_day24_layout.addWidget(self.right_bar_tour_point_day24_longitude, 1, 0, 4, 1)  # 圆环饼图 经度 文字
        self.right_bar_point_day24_layout.addWidget(self.right_bar_widget_point_day24_longitude_input, 1, 1, 4,
                                                    3)  # 圆环饼图 经度 输入框
        self.right_bar_point_day24_layout.addWidget(self.right_bar_widget_point_day24_longitude_input_holder, 1, 4, 4,
                                                    2)  # 圆环饼图 经度 提示文字
        self.right_bar_point_day24_layout.addWidget(self.right_bar_tour_point_day24_latitude, 2, 0, 4, 1)  # 圆环饼图 纬度 文字
        self.right_bar_point_day24_layout.addWidget(self.right_bar_widget_point_day24_latitude_input, 2, 1, 4,
                                                    3)  # 圆环饼图 纬度 输入框
        self.right_bar_point_day24_layout.addWidget(self.right_bar_widget_point_day24_latitude_input_holder, 2, 4, 4,
                                                    3)  # 圆环饼图 纬度 提示文字

        self.right_bar_point_day24_layout.addWidget(self.right_bar_tour_point_day24_altitude, 3, 0, 4, 1)  # 圆环饼图 纬度 文字
        self.right_bar_point_day24_layout.addWidget(self.right_bar_widget_point_day24_altitude_input, 3, 1, 4,
                                                    3)  # 圆环饼图 环绕宽度 输入框
        self.right_bar_point_day24_layout.addWidget(self.right_bar_widget_point_day24_altitude_input_holder, 3, 4, 4,
                                                    3)  # 圆环饼图 环绕宽度 当前值

        self.right_bar_point_day24_layout.addWidget(self.right_bar_widget_point_day24_button_download, 4, 1, 4,
                                                    2)  # (跨行的控件，起始行，起始列，跨越的行数，跨越列数)
        self.right_bar_point_day24_layout.addWidget(self.right_bar_widget_point_day24_placeholder, 18, 2, 4,
                                                    2)  # 圆环饼图 环绕宽度 占位符


        self.right_bar_widget_point_day24_button_download.clicked.connect(self.on_tour_point_day24_kmlname_push_button_clicked)

        self.setLayout(self.right_bar_point_day24_layout)


    def on_tour_point_day24_kmlname_push_button_clicked(self):
        """
        环绕浏览 啟始方向 当前值
        :param value:
        :return:
        """
        kmlname = self.right_bar_widget_point_day24_kmlname_input.text()
        kmlname = kmlname if kmlname else ''
        try:
            TourPointDay24(kmlname).tour_point_day_neight_change(
                kmlname=self.right_bar_widget_point_day24_kmlname_input.text(),
                latitude=float(self.right_bar_widget_point_day24_latitude_input.text()),
                longitude=float(self.right_bar_widget_point_day24_longitude_input.text()),
                altitude=int(self.right_bar_widget_point_day24_altitude_input.text())
            )

            toast = Toast(title="下载成功", content=random_content(), level=AlertLevel.SUCCESS, parent=self)
            # 获取Demo窗口的顶部中心位置
            top_center_point = self.mapToGlobal(QtCore.QPoint(self.rect().width() // 2, 0))
            x_position = top_center_point.x() - toast.width() // 2
            y_position = top_center_point.y()
            toast.showToast(x_position, y_position)

        except Exception as e:
            toast = Toast(title="提示", content="输入的数据有误!", level=AlertLevel.ERROR, parent=self)
            # 获取Demo窗口的顶部中心位置
            top_center_point = self.mapToGlobal(QtCore.QPoint(self.rect().width() // 2, 0))
            x_position = top_center_point.x() - toast.width() // 2
            y_position = top_center_point.y()
            toast.showToast(x_position, y_position)