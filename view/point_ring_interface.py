from PyQt5 import QtCore, QtGui, QtWidgets

from tour.tour_point_ring import TourPointRing

class PointRingView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        # ======================右侧点击-圆环饼图====================================================
        self.right_bar_point_ring_widget = QtWidgets.QWidget()  # 右侧顶部搜索框部件
        self.right_bar_point_ring_layout = QtWidgets.QGridLayout()  # 右侧顶部搜索框网格布局
        self.right_bar_point_ring_widget.setLayout(self.right_bar_point_ring_layout)

        self.right_bar_tour_point_ring = QtWidgets.QPushButton("圆环饼图")
        self.right_bar_tour_point_ring.setObjectName("right_lable_title")

        # 坐标浏览 圆环饼图 名称输入框
        self.right_bar_tour_point_ring_kmlname = QtWidgets.QLabel('名称  Kmlname')
        self.right_bar_tour_point_ring_kmlname.setObjectName("right_bar_tour_label")
        self.right_bar_widget_point_ring_kmlname_input = QtWidgets.QLineEdit()
        self.right_bar_widget_point_ring_kmlname_input.setText('上海东方明珠')
        self.right_bar_widget_point_ring_kmlname_input.setPlaceholderText("输入要保存的文件名")
        self.right_bar_widget_point_ring_kmlname_input.setObjectName('right_bar_widget_qlinedit_input')

        # 坐标浏览 圆环饼图 经度输入框
        self.right_bar_tour_point_ring_longitude = QtWidgets.QLabel('经度  Longitude')  # 文字栏
        self.right_bar_tour_point_ring_longitude.setObjectName("right_bar_tour_label")
        self.right_bar_widget_point_ring_longitude_input = QtWidgets.QLineEdit()  # 输入框栏
        self.right_bar_widget_point_ring_longitude_input.setText('121.4952627807584')
        self.right_bar_widget_point_ring_longitude_input.setPlaceholderText("输入经度 十进制度小数")
        self.right_bar_widget_point_ring_longitude_input.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_widget_point_ring_longitude_input_holder = QtWidgets.QLabel("输入经度 十进制度小数")  # 提示栏
        self.right_bar_widget_point_ring_longitude_input_holder.setObjectName("right_bar_widget_holder")

        # 坐标浏览 圆环饼图 纬度输入框
        self.right_bar_tour_point_ring_latitude = QtWidgets.QLabel('纬度  Latitude')  # 文字栏
        self.right_bar_tour_point_ring_latitude.setObjectName("right_bar_tour_label")
        self.right_bar_widget_point_ring_latitude_input = QtWidgets.QLineEdit()  # 输入框栏
        self.right_bar_widget_point_ring_latitude_input.setText('31.24188370156092')
        self.right_bar_widget_point_ring_latitude_input.setPlaceholderText("输入纬度 十进制度小数")
        self.right_bar_widget_point_ring_latitude_input.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_widget_point_ring_latitude_input_holder = QtWidgets.QLabel("输入纬度 十进制度小数")  # 提示栏
        self.right_bar_widget_point_ring_latitude_input_holder.setObjectName("right_bar_widget_holder")

        # 坐标浏览 圆环饼图 圆外半径   outer_radius
        self.right_bar_tour_point_ring_outer_radius = QtWidgets.QLabel('外圆半径  Radius')  # 文字栏
        self.right_bar_tour_point_ring_outer_radius.setObjectName("right_bar_tour_label")
        self.right_bar_widget_point_ring_outer_radius_input = QtWidgets.QLineEdit()  # 输入框栏
        self.right_bar_widget_point_ring_outer_radius_input.setText('468')
        self.right_bar_widget_point_ring_outer_radius_input.setPlaceholderText("外圆半径")
        self.right_bar_widget_point_ring_outer_radius_input.setObjectName('right_bar_widget_qlinedit_input')

        # 坐标浏览 圆环饼图 环宽 inner_radius
        self.right_bar_tour_point_ring_inner_radius = QtWidgets.QLabel('内圆半径  Radius')  # 文字栏
        self.right_bar_tour_point_ring_inner_radius.setObjectName("right_bar_tour_label")
        self.right_bar_widget_point_ring_inner_radius_input = QtWidgets.QLineEdit()  # 输入框栏
        self.right_bar_widget_point_ring_inner_radius_input.setText('0')
        self.right_bar_widget_point_ring_inner_radius_input.setPlaceholderText("内圆半径")

        self.right_bar_widget_point_ring_inner_radius_input.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_widget_point_ring_inner_radius_input_holder_value = QtWidgets.QLabel("0则实心圆")  # 提示文字

        # 坐标浏览 圆环饼图 下载
        self.right_bar_widget_point_ring_button_download = QtWidgets.QPushButton()
        self.right_bar_widget_point_ring_button_download.setText("确定")
        self.right_bar_widget_point_ring_button_download.setObjectName('right_bar_tour_button_download')
        self.right_bar_widget_point_ring_placeholder = QtWidgets.QLabel("")  # 占位符

        self.right_bar_point_ring_layout.addWidget(self.right_bar_tour_point_ring, 0, 0, 1,
                                                   1)  # (跨行的控件，起始行，起始列，跨越的行数，跨越列数)
        self.right_bar_point_ring_layout.addWidget(self.right_bar_tour_point_ring_kmlname, 0, 0, 4, 1)
        self.right_bar_point_ring_layout.addWidget(self.right_bar_widget_point_ring_kmlname_input, 0, 1, 4, 3)
        self.right_bar_point_ring_layout.addWidget(self.right_bar_tour_point_ring_longitude, 1, 0, 4, 1)  # 圆环饼图 经度 文字
        self.right_bar_point_ring_layout.addWidget(self.right_bar_widget_point_ring_longitude_input, 1, 1, 4,
                                                   3)  # 圆环饼图 经度 输入框
        self.right_bar_point_ring_layout.addWidget(self.right_bar_widget_point_ring_longitude_input_holder, 1, 4, 4,
                                                   2)  # 圆环饼图 经度 提示文字
        self.right_bar_point_ring_layout.addWidget(self.right_bar_tour_point_ring_latitude, 2, 0, 4, 1)  # 圆环饼图 纬度 文字
        self.right_bar_point_ring_layout.addWidget(self.right_bar_widget_point_ring_latitude_input, 2, 1, 4,
                                                   3)  # 圆环饼图 纬度 输入框
        self.right_bar_point_ring_layout.addWidget(self.right_bar_widget_point_ring_latitude_input_holder, 2, 4, 4,
                                                   3)  # 圆环饼图 纬度 提示文字
        self.right_bar_point_ring_layout.addWidget(self.right_bar_tour_point_ring_outer_radius, 3, 0, 4,
                                                   1)  # 圆环饼图 圆外半径 文字
        self.right_bar_point_ring_layout.addWidget(self.right_bar_widget_point_ring_outer_radius_input, 3, 1, 4,
                                                   3)  # 圆环饼图 圆外半径 输入框
        self.right_bar_point_ring_layout.addWidget(self.right_bar_tour_point_ring_inner_radius, 4, 0, 4,
                                                   1)  # 圆环饼图 环绕宽度 文字
        self.right_bar_point_ring_layout.addWidget(self.right_bar_widget_point_ring_inner_radius_input, 4, 1, 4,
                                                   3)  # 圆环饼图 环绕宽度 输入框
        self.right_bar_point_ring_layout.addWidget(self.right_bar_widget_point_ring_inner_radius_input_holder_value, 4,
                                                   4, 4, 1)  # 圆环饼图 环绕宽度 当前值
        self.right_bar_point_ring_layout.addWidget(self.right_bar_widget_point_ring_button_download, 5, 1, 4,
                                                   2)  # (跨行的控件，起始行，起始列，跨越的行数，跨越列数)
        self.right_bar_point_ring_layout.addWidget(self.right_bar_widget_point_ring_placeholder, 18, 2, 4,
                                                   2)  # 圆环饼图 环绕宽度 占位符


        self.right_bar_widget_point_ring_button_download.clicked.connect(self.on_tour_point_ring_kmlname_push_button_clicked)

        self.setLayout(self.right_bar_point_ring_layout)

    def on_tour_point_ring_kmlname_push_button_clicked(self):
        """
        环绕浏览 啟始方向 当前值
        :param value:
        :return:
        """
        try:
            TourPointRing().tour_point_ring(
                kmlname=self.right_bar_widget_point_ring_kmlname_input.text(),
                latitude=float(self.right_bar_widget_point_ring_latitude_input.text()),
                longitude=float(self.right_bar_widget_point_ring_longitude_input.text()),
                outer_radius=int(self.right_bar_widget_point_ring_outer_radius_input.text()),
                inner_radius=int(self.right_bar_widget_point_ring_inner_radius_input.text())
            )
            QtWidgets.QMessageBox.information(self, "提示", "下载成功！")
        except Exception as e:
            import traceback
            traceback.print_exc()
            QtWidgets.QMessageBox.warning(self, "提示", "输入的数据有误!")
