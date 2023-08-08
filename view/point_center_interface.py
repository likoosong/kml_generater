from PyQt5 import QtCore, QtGui, QtWidgets
from pyqt_toast import Toast

from tour.tour_point_centre import TourPointCentre

class PointCenterView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.right_bar_widget = QtWidgets.QWidget()  # 右侧顶部搜索框部件
        self.right_bar_layout = QtWidgets.QGridLayout()  # 右侧顶部搜索框网格布局
        self.right_bar_widget.setLayout(self.right_bar_layout)

        self.right_bar_tour_point = QtWidgets.QPushButton("四顾浏览")
        self.right_bar_tour_point.setObjectName("right_lable_title")

        # 名称输入框
        self.right_bar_tour_point_kmlname = QtWidgets.QLabel('名称  Kmlname')
        self.right_bar_tour_point_kmlname.setObjectName("right_bar_tour_label")
        self.right_bar_widget_point_kmlname_input = QtWidgets.QLineEdit()
        self.right_bar_widget_point_kmlname_input.setText('上海东方明珠')
        self.right_bar_widget_point_kmlname_input.setPlaceholderText("输入要保存的文件名")
        self.right_bar_widget_point_kmlname_input.setObjectName('right_bar_widget_qlinedit_input')

        # 经度输入框
        self.right_bar_tour_point_longitude = QtWidgets.QLabel('经度  Longitude')  # 文字栏
        self.right_bar_tour_point_longitude.setObjectName("right_bar_tour_label")
        self.right_bar_widget_point_longitude_input = QtWidgets.QLineEdit()  # 输入框栏
        self.right_bar_widget_point_longitude_input.setText('121.4952627807584')
        self.right_bar_widget_point_longitude_input.setPlaceholderText("输入经度 十进制度小数")
        self.right_bar_widget_point_longitude_input.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_widget_point_longitude_input_holder = QtWidgets.QLabel("输入经度 十进制度小数")  # 提示栏
        self.right_bar_widget_point_longitude_input_holder.setObjectName("right_bar_widget_holder")

        # 纬度输入框
        self.right_bar_tour_point_latitude = QtWidgets.QLabel('纬度  Latitude')  # 文字栏
        self.right_bar_tour_point_latitude.setObjectName("right_bar_tour_label")
        self.right_bar_widget_point_latitude_input = QtWidgets.QLineEdit()  # 输入框栏
        self.right_bar_widget_point_latitude_input.setText('31.24188370156092')
        self.right_bar_widget_point_latitude_input.setPlaceholderText("输入纬度 十进制度小数")
        self.right_bar_widget_point_latitude_input.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_widget_point_latitude_input_holder = QtWidgets.QLabel("输入纬度 十进制度小数")  # 提示栏
        self.right_bar_widget_point_latitude_input_holder.setObjectName("right_bar_widget_holder")

        # 高度输入框
        self.right_bar_tour_point_height = QtWidgets.QLabel('高度  Height')  # 文字栏
        self.right_bar_tour_point_height.setObjectName("right_bar_tour_label")
        self.right_bar_widget_point_height_input = QtWidgets.QLineEdit()  # 输入框栏
        self.right_bar_widget_point_height_input.setText('468')
        # self.right_bar_widget_point_height_input.setPlaceholderText("建筑、山体高度")
        self.right_bar_widget_point_height_input.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_widget_point_height_input_holder = QtWidgets.QLabel("建筑、山体高度")  # 提示栏
        self.right_bar_widget_point_height_input_holder.setObjectName("right_bar_widget_holder")

        # 环绕半径输入框
        self.right_bar_tour_point_radius = QtWidgets.QLabel('环绕半径  Radius')  # 文字栏
        self.right_bar_tour_point_radius.setObjectName("right_bar_tour_label")
        self.right_bar_widget_point_radius_input = QtWidgets.QLineEdit()  # 输入框栏
        self.right_bar_widget_point_radius_input.setText('781')
        # self.right_bar_widget_point_radius_input.setPlaceholderText("环绕半径  Radius")
        self.right_bar_widget_point_radius_input.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_widget_point_radius_input_holder = QtWidgets.QLabel("建议值为高度的1.67倍 , 0 表為環景")  # 提示文字
        self.right_bar_widget_point_radius_input_holder.setObjectName("right_bar_widget_holder")

        # 環繞視點高度 Height
        self.right_bar_tour_point_altitude = QtWidgets.QLabel('视点高度  Altitude')  # 文字栏
        self.right_bar_tour_point_altitude.setObjectName("right_bar_tour_label")
        self.right_bar_widget_point_altitude_input = QtWidgets.QLineEdit()  # 输入框栏
        self.right_bar_widget_point_altitude_input.setText('702')
        self.right_bar_widget_point_altitude_input.setPlaceholderText("建议值为高度的1.5倍")
        self.right_bar_widget_point_altitude_input.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_widget_point_altitude_input_holder = QtWidgets.QLabel("建议值为高度的1.5倍")  # 提示文字
        self.right_bar_widget_point_altitude_input_holder.setObjectName("right_bar_widget_holder")

        # 環繞視野角度
        self.right_bar_tour_point_horizfov = QtWidgets.QLabel('视野角度  Horizfov')  # 文字栏
        self.right_bar_tour_point_horizfov.setObjectName("right_bar_tour_label")
        self.right_bar_widget_point_horizfov_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)  # 滑块框栏
        # self.right_bar_widget_point_horizfov_slider.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_widget_point_horizfov_slider.setMinimum(30)  # 设置最小值
        self.right_bar_widget_point_horizfov_slider.setMaximum(120)  # 设置最大值
        self.right_bar_widget_point_horizfov_slider.setSingleStep(1)  # 设置滑动步长
        self.right_bar_widget_point_horizfov_slider.setValue(60)  # 设置当前值
        self.right_bar_widget_point_horizfov_slider_value = QtWidgets.QLabel("60°")  # 提示文字

        # 環繞傾斜角度 Tilt
        self.right_bar_tour_point_tilt = QtWidgets.QLabel('倾斜角度  Tilt')
        self.right_bar_tour_point_tilt.setObjectName("right_bar_tour_label")
        self.right_bar_widget_point_tilt_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)  # 滑块框栏
        self.right_bar_widget_point_tilt_slider.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_widget_point_tilt_slider.setMinimum(0)  # 设置最小值
        self.right_bar_widget_point_tilt_slider.setMaximum(90)  # 设置最大值
        self.right_bar_widget_point_tilt_slider.setSingleStep(1)  # 设置滑动步长
        self.right_bar_widget_point_tilt_slider.setValue(60)  # 设置当前值
        self.right_bar_widget_point_tilt_slider_value = QtWidgets.QLabel("60°")  # 提示文字
        self.right_bar_widget_point_tilt_slider_holder = QtWidgets.QLabel("0°为正射，90°为水平")  # 提示文字
        self.right_bar_widget_point_tilt_slider_holder.setObjectName("right_bar_widget_holder")

        # 環繞 啟始方向 Ring Around Start Direction: -180° <--> 180°
        self.right_bar_tour_point_heading = QtWidgets.QLabel('开启方向')
        self.right_bar_tour_point_heading.setObjectName("right_bar_tour_label")
        self.right_bar_widget_point_heading_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)  # 滑块框栏
        self.right_bar_widget_point_heading_slider.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_widget_point_heading_slider.setMinimum(-180)  # 设置最小值
        self.right_bar_widget_point_heading_slider.setMaximum(180)  # 设置最大值
        self.right_bar_widget_point_heading_slider.setSingleStep(1)  # 设置滑动步长
        self.right_bar_widget_point_heading_slider.setValue(0)  # 设置当前值
        self.right_bar_widget_point_heading_slider_value = QtWidgets.QLabel("0°")  # 提示文字

        # 環繞 环绕时间
        self.right_bar_tour_point_tour_time = QtWidgets.QLabel('环绕时间')
        self.right_bar_tour_point_tour_time.setObjectName("right_bar_tour_label")
        self.right_bar_widget_point_tour_time_input = QtWidgets.QLineEdit()
        self.right_bar_widget_point_tour_time_input.setPlaceholderText("建议20 ~ 30秒")
        self.right_bar_widget_point_tour_time_input.setText('30')
        self.right_bar_widget_point_tour_time_input.setObjectName('right_bar_widget_qlinedit_input')

        # 環繞 方向 clockwise:
        self.right_bar_tour_point_clock = QtWidgets.QLabel('环绕方向')
        self.right_bar_tour_point_clock.setObjectName("right_bar_tour_label")
        self.right_bar_tour_point_clock_wise_group_button = QtWidgets.QButtonGroup()  # 按钮分组
        self.right_bar_tour_point_clock_wise_button = QtWidgets.QRadioButton("顺时针")
        self.right_bar_tour_point_clock_wise_button.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_tour_point_clock_wise_button.setChecked(True)
        self.right_bar_tour_point_counter_clock_wise_button = QtWidgets.QRadioButton("逆时针")
        self.right_bar_tour_point_counter_clock_wise_button.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_tour_point_clock_wise_group_button.addButton(self.right_bar_tour_point_clock_wise_button,
                                                                    1)  # 设置ID为1
        self.right_bar_tour_point_clock_wise_group_button.addButton(self.right_bar_tour_point_counter_clock_wise_button,
                                                                    2)

        self.right_bar_widget_point_button_download = QtWidgets.QPushButton()
        self.right_bar_widget_point_button_download.setText("确定")
        self.right_bar_widget_point_button_download.setObjectName('right_bar_tour_button_download')

        self.right_bar_layout.addWidget(self.right_bar_tour_point, 0, 0, 1, 1)  # (跨行的控件，起始行，起始列，跨越的行数，跨越列数)
        self.right_bar_layout.addWidget(self.right_bar_tour_point_kmlname, 0, 0, 4, 1)
        self.right_bar_layout.addWidget(self.right_bar_widget_point_kmlname_input, 0, 1, 4, 3)  #
        self.right_bar_layout.addWidget(self.right_bar_tour_point_longitude, 1, 0, 4, 1)  # 经度 文字
        self.right_bar_layout.addWidget(self.right_bar_widget_point_longitude_input, 1, 1, 4, 3)  # 经度 输入框
        self.right_bar_layout.addWidget(self.right_bar_widget_point_longitude_input_holder, 1, 4, 4, 2)  # 经度 提示文字
        self.right_bar_layout.addWidget(self.right_bar_tour_point_latitude, 2, 0, 4, 1)  # 纬度 文字
        self.right_bar_layout.addWidget(self.right_bar_widget_point_latitude_input, 2, 1, 4, 3)  # 纬度 输入框
        self.right_bar_layout.addWidget(self.right_bar_widget_point_latitude_input_holder, 2, 4, 4, 3)  # 纬度 提示文字
        self.right_bar_layout.addWidget(self.right_bar_tour_point_height, 3, 0, 4, 1)  # 高度 文字
        self.right_bar_layout.addWidget(self.right_bar_widget_point_height_input, 3, 1, 4, 3)  # 高度 输入框
        self.right_bar_layout.addWidget(self.right_bar_widget_point_height_input_holder, 3, 4, 4, 3)  # 高度 提示文字
        self.right_bar_layout.addWidget(self.right_bar_tour_point_radius, 4, 0, 4, 1)  # 环绕半径 文字
        self.right_bar_layout.addWidget(self.right_bar_widget_point_radius_input, 4, 1, 4, 3)  # 环绕半径 输入框
        self.right_bar_layout.addWidget(self.right_bar_widget_point_radius_input_holder, 4, 4, 4, 3)  # 环绕半径 提示文字
        self.right_bar_layout.addWidget(self.right_bar_tour_point_altitude, 5, 0, 4, 1)  # 视点高度 文字
        self.right_bar_layout.addWidget(self.right_bar_widget_point_altitude_input, 5, 1, 4, 3)  # 视点高度 输入框
        self.right_bar_layout.addWidget(self.right_bar_widget_point_altitude_input_holder, 5, 4, 4, 3)  # 视点高度 提示文字
        self.right_bar_layout.addWidget(self.right_bar_tour_point_horizfov, 6, 0, 4, 1)  # 視野角度 文字
        self.right_bar_layout.addWidget(self.right_bar_widget_point_horizfov_slider, 6, 1, 4, 3)  # 視野角度 滑块
        self.right_bar_layout.addWidget(self.right_bar_widget_point_horizfov_slider_value, 6, 4, 4, 1)  # 視野角度 当前值
        self.right_bar_layout.addWidget(self.right_bar_tour_point_tilt, 7, 0, 4, 1)  # 傾斜角度 文字
        self.right_bar_layout.addWidget(self.right_bar_widget_point_tilt_slider, 7, 1, 4, 3)  # 傾斜角度 滑块
        self.right_bar_layout.addWidget(self.right_bar_widget_point_tilt_slider_value, 7, 4, 4, 1)  # 傾斜角度 当前值
        self.right_bar_layout.addWidget(self.right_bar_widget_point_tilt_slider_holder, 7, 5, 4, 1)  # 傾斜角度 提示文字
        self.right_bar_layout.addWidget(self.right_bar_tour_point_heading, 8, 0, 4, 1)  # 啟始方向 文字
        self.right_bar_layout.addWidget(self.right_bar_widget_point_heading_slider, 8, 1, 4, 3)  # 啟始方向 滑块
        self.right_bar_layout.addWidget(self.right_bar_widget_point_heading_slider_value, 8, 4, 4, 1)  # 啟始方向 当前值
        self.right_bar_layout.addWidget(self.right_bar_tour_point_tour_time, 9, 0, 4, 1)  # 環繞方向 文字
        self.right_bar_layout.addWidget(self.right_bar_widget_point_tour_time_input, 9, 1, 4, 3)  # 環繞方向 当前值

        self.right_bar_layout.addWidget(self.right_bar_tour_point_clock, 10, 0, 4, 1)
        self.right_bar_layout.addWidget(self.right_bar_tour_point_clock_wise_button, 10, 1, 4, 3)
        self.right_bar_layout.addWidget(self.right_bar_tour_point_counter_clock_wise_button, 10, 2, 4, 3)
        self.right_bar_layout.addWidget(self.right_bar_widget_point_button_download, 12, 2, 3, 2)  # (跨行的控件，起始行，起始列，跨越的行数，跨越列数)

        # 事件监听 四顾浏览 高度 Altitude 環繞半徑 Radius 環繞視點高度 Height
        self.right_bar_widget_point_height_input.textChanged.connect(self.right_bar_widget_point_height_slider_connect)
        # 事件监听 四顾浏览 環繞視野角度 horizfov 提示
        self.right_bar_widget_point_horizfov_slider.valueChanged.connect(self.right_bar_widget_point_horizfov_slider_connect)
        # 事件监听 四顾浏览  環繞傾斜角度 Tilt 提示
        self.right_bar_widget_point_tilt_slider.valueChanged.connect(self.right_bar_widget_point_tilt_slider_connect)
        # 事件监听 四顾浏览  環繞啟始方向 heading 提示
        self.right_bar_widget_point_heading_slider.valueChanged.connect(self.right_bar_widget_point_heading_slider_connect)
        self.right_bar_widget_point_button_download.clicked.connect(self.on_tour_point_kmlname_push_button_clicked)



        self.setLayout(self.right_bar_layout)

    def right_bar_widget_point_horizfov_slider_connect(self, value):
        """
        四顾浏览 環繞視野角度 提示
        :return:
        """
        slider_horizfov_value = self.right_bar_widget_point_horizfov_slider.value()  # 获取当前滑块值
        self.right_bar_widget_point_horizfov_slider_value.setText('%s°' % slider_horizfov_value)

    def right_bar_widget_point_tilt_slider_connect(self, value):
        """
        环绕浏览 啟始方向 当前值
        :param value:
        :return:
        """
        slider_tilt_value = self.right_bar_widget_point_tilt_slider.value()  # 获取当前滑块值
        self.right_bar_widget_point_tilt_slider_value.setText('%s°' % slider_tilt_value)

    def right_bar_widget_point_heading_slider_connect(self, value):
        """
        环绕浏览 啟始方向 当前值
        :param value:
        :return:
        """
        slider_heading_value = self.right_bar_widget_point_heading_slider.value()  # 获取当前滑块值
        self.right_bar_widget_point_heading_slider_value.setText('%s°' % slider_heading_value)

    def right_bar_widget_point_height_slider_connect(self):
        """
        环绕浏览 建筑物高度 当前值
        :param value:
        :return:
        """
        try:
            height = self.right_bar_widget_point_height_input.text()
            self.right_bar_widget_point_radius_input.setText(str(int(int(height) * 1.67)))
            self.right_bar_widget_point_altitude_input.setText(str(int(int(height) * 1.5)))
        except:
            self.toast = Toast(text='你输入有误', duration=1, parent=self)
            self.toast.setBackgroundColor(QtGui.QColor(255, 0, 0, 127))
            self.toast.show()

    # 下载按钮事件  right_bar_tour_point_kmlname
    def on_tour_point_kmlname_push_button_clicked(self):
        """
        :return:
        """
        try:
            kmlname = self.right_bar_widget_point_kmlname_input.text()
            TourPointCentre(kmlname).tour_point_centre(
                kmlname=kmlname,
                longitude=self.right_bar_widget_point_longitude_input.text(),  # 经度
                latitude=self.right_bar_widget_point_latitude_input.text(),  # 纬度
                altitude=self.right_bar_widget_point_altitude_input.text(),  # 实际:467.9   高度 1.67 倍
                tilt=self.right_bar_widget_point_tilt_slider.value(),  # 环绕倾斜角度
                tour_time=int(self.right_bar_widget_point_tour_time_input.text()),  # 环绕一圈時間,
                clock=1 if self.right_bar_tour_point_clock_wise_button.isChecked() else 0
            )
            QtWidgets.QMessageBox.information(self, "提示", "下载成功！")
        except:
            QtWidgets.QMessageBox.warning(self, "提示", "输入的数据有误!")