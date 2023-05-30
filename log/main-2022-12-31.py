import sys

import qtawesome
from PyQt5 import QtCore, QtGui, QtWidgets
from pyqt_toast import Toast

from tour.tour_point_centre import TourPointCentre
from tour.tour_point_around import TourPointAround
from tour.tour_point_ring import TourPointRing

class MainUi(QtWidgets.QMainWindow):


    def __init__(self):

        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(960, 700)
        self.main_widget = QtWidgets.QWidget()          # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()      # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)    # 设置窗口主部件布局为网格布局

        self.left_widget = QtWidgets.QWidget()         # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()     # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout)   # 设置左侧部件布局为网格

        # ======================右侧点击-中心浏览====================================================
        self.right_widget = QtWidgets.QWidget()          #  创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout)   # 设置右侧部件布局为网格

        # 右侧先在此注册 - 然后默认隐藏
        self.main_layout.addWidget(self.left_widget, 0, 0, 12, 2) # 左侧部件在第0行第0列，占8行3列  (跨行的控件，起始行，起始列，跨越的行数，跨越列数)
        self.main_layout.addWidget(self.right_widget, 0, 2, 12, 10)  # 右侧部件在第0行第3列，占8行9列

        self.left_close = QtWidgets.QPushButton("x")   # 关闭按钮
        self.left_visit = QtWidgets.QPushButton("")   # 空白按钮
        self.left_mini = QtWidgets.QPushButton("-")    # 最小化按钮

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

        self.left_button_1 = QtWidgets.QPushButton(qtawesome.icon('fa.music',color='white'),"四顾浏览")
        self.left_button_1.setObjectName('left_button')
        self.left_button_2 = QtWidgets.QPushButton(qtawesome.icon('fa.sellsy',color='white'),"环绕浏览")
        self.left_button_2.setObjectName('left_button')
        self.left_button_3 = QtWidgets.QPushButton(qtawesome.icon('fa.film',color='white'),"圆饼环图")
        self.left_button_3.setObjectName('left_button')
        self.left_button_4 = QtWidgets.QPushButton(qtawesome.icon('fa.home',color='white'),"线路浏览")
        self.left_button_4.setObjectName('left_button')
        self.left_button_5 = QtWidgets.QPushButton(qtawesome.icon('fa.download',color='white'),"高铁线路")
        self.left_button_5.setObjectName('left_button')
        self.left_button_6 = QtWidgets.QPushButton(qtawesome.icon('fa.heart',color='white'),"地铁线路")
        self.left_button_6.setObjectName('left_button')
        self.left_button_7 = QtWidgets.QPushButton(qtawesome.icon('fa.comment',color='white'),"省市县区")
        self.left_button_7.setObjectName('left_button')
        self.left_button_8 = QtWidgets.QPushButton(qtawesome.icon('fa.star',color='white'),"关注我们")
        self.left_button_8.setObjectName('left_button')
        self.left_button_9 = QtWidgets.QPushButton(qtawesome.icon('fa.question',color='white'),"遇到问题")
        self.left_button_9.setObjectName('left_button')

        self.left_layout.addWidget(self.left_mini, 0, 0, 1, 1)       # 最小化
        self.left_layout.addWidget(self.left_visit, 0, 1, 1, 1)      # 浏览
        self.left_layout.addWidget(self.left_close, 0, 2, 1, 1)      # 关闭
        self.left_layout.addWidget(self.left_label_1, 1, 0, 1, 3)    # 一级标题 坐标浏览
        self.left_layout.addWidget(self.left_button_1, 3, 0, 1, 3)   # 二级标题 环绕浏览
        self.left_layout.addWidget(self.left_button_2, 2, 0, 1, 3)   # 二级标题 四顾浏览
        self.left_layout.addWidget(self.left_button_3, 4, 0, 1, 3)   # 二级标题 四顾浏览
        self.left_layout.addWidget(self.left_label_2, 5, 0, 1, 3)    # 一级标题 线路浏览
        self.left_layout.addWidget(self.left_button_4, 6, 0, 1, 3)   # 二级标题 线路浏览
        self.left_layout.addWidget(self.left_button_5, 7, 0, 1, 3)   # 二级标题 高铁浏览
        self.left_layout.addWidget(self.left_button_6, 8, 0, 1, 3)   # 二级标题 地铁浏览
        self.left_layout.addWidget(self.left_label_3, 9, 0, 1, 3)    # 一级标题 多变区域
        self.left_layout.addWidget(self.left_button_7, 10, 0, 1, 3)  # 二级标题 省市县区
        self.left_layout.addWidget(self.left_label_4, 11, 0, 1, 3)   # 一级标题 联系与帮助
        self.left_layout.addWidget(self.left_button_8, 12, 0, 1, 3)  # 二级标题 省市县区
        self.left_layout.addWidget(self.left_button_9, 13, 0, 1, 3)  # 二级标题 省市县区

        self.right_bar_widget = QtWidgets.QWidget()     # 右侧顶部搜索框部件
        self.right_bar_layout = QtWidgets.QGridLayout() # 右侧顶部搜索框网格布局
        self.right_bar_widget.setLayout(self.right_bar_layout)

        self.right_bar_tour_point = QtWidgets.QPushButton("四顾浏览")
        self.right_bar_tour_point.setObjectName("right_lable_title")

        # 名称输入框
        self.right_bar_tour_point_kmlname = QtWidgets.QLabel('名称  Kmlname')
        self.right_bar_tour_point_kmlname.setObjectName("right_bar_tour_point_label")
        self.right_bar_widget_point_kmlname_input = QtWidgets.QLineEdit()
        self.right_bar_widget_point_kmlname_input.setText('上海东方明珠')
        self.right_bar_widget_point_kmlname_input.setPlaceholderText("输入要保存的文件名")
        self.right_bar_widget_point_kmlname_input.setObjectName('right_bar_widget_qlinedit_point_input')

        # 经度输入框
        self.right_bar_tour_point_longitude = QtWidgets.QLabel('经度  Longitude')            # 文字栏
        self.right_bar_tour_point_longitude.setObjectName("right_bar_tour_point_label")
        self.right_bar_widget_point_longitude_input = QtWidgets.QLineEdit()                 # 输入框栏
        self.right_bar_widget_point_longitude_input.setText('121.4952627807584')
        self.right_bar_widget_point_longitude_input.setPlaceholderText("输入经度 十进制度小数")
        self.right_bar_widget_point_longitude_input.setObjectName('right_bar_widget_qlinedit_point_input')
        self.right_bar_widget_point_longitude_input_holder = QtWidgets.QLabel("输入经度 十进制度小数")  # 提示栏
        self.right_bar_widget_point_longitude_input_holder.setObjectName("right_bar_widget_point_input_holder")

        # 纬度输入框
        self.right_bar_tour_point_latitude = QtWidgets.QLabel('纬度  Latitude')             # 文字栏
        self.right_bar_tour_point_latitude.setObjectName("right_bar_tour_point_label")
        self.right_bar_widget_point_latitude_input = QtWidgets.QLineEdit()                 # 输入框栏
        self.right_bar_widget_point_latitude_input.setText('31.24188370156092')
        self.right_bar_widget_point_latitude_input.setPlaceholderText("输入纬度 十进制度小数")
        self.right_bar_widget_point_latitude_input.setObjectName('right_bar_widget_qlinedit_point_input')
        self.right_bar_widget_point_latitude_input_holder = QtWidgets.QLabel("输入纬度 十进制度小数")    # 提示栏
        self.right_bar_widget_point_latitude_input_holder.setObjectName("right_bar_widget_point_input_holder")

        # 高度输入框
        self.right_bar_tour_point_height = QtWidgets.QLabel('高度  Height')                # 文字栏
        self.right_bar_tour_point_height.setObjectName("right_bar_tour_point_label")
        self.right_bar_widget_point_height_input = QtWidgets.QLineEdit()                  # 输入框栏
        self.right_bar_widget_point_height_input.setText('468')
        # self.right_bar_widget_point_height_input.setPlaceholderText("建筑、山体高度")
        self.right_bar_widget_point_height_input.setObjectName('right_bar_widget_qlinedit_point_input')
        self.right_bar_widget_point_height_input_holder = QtWidgets.QLabel("建筑、山体高度")    # 提示栏
        self.right_bar_widget_point_height_input_holder.setObjectName("right_bar_widget_point_input_holder")

        # 环绕半径输入框
        self.right_bar_tour_point_radius = QtWidgets.QLabel('环绕半径  Radius')             # 文字栏
        self.right_bar_tour_point_radius.setObjectName("right_bar_tour_point_label")
        self.right_bar_widget_point_radius_input = QtWidgets.QLineEdit()                  # 输入框栏
        self.right_bar_widget_point_radius_input.setText('781')
        # self.right_bar_widget_point_radius_input.setPlaceholderText("环绕半径  Radius")
        self.right_bar_widget_point_radius_input.setObjectName('right_bar_widget_qlinedit_point_input')
        self.right_bar_widget_point_radius_input_holder = QtWidgets.QLabel("建議值為高度的1.67倍 , 0 表為環景")  # 提示文字
        self.right_bar_widget_point_radius_input_holder.setObjectName("right_bar_widget_point_input_holder")

        # 環繞視點高度 Height
        self.right_bar_tour_point_altitude = QtWidgets.QLabel('视点高度  Altitude')          # 文字栏
        self.right_bar_tour_point_altitude.setObjectName("right_bar_tour_point_label")
        self.right_bar_widget_point_altitude_input = QtWidgets.QLineEdit()                  # 输入框栏
        self.right_bar_widget_point_altitude_input.setText('702')
        self.right_bar_widget_point_altitude_input.setPlaceholderText("建議值為高度的1.5倍")
        self.right_bar_widget_point_altitude_input.setObjectName('right_bar_widget_qlinedit_point_input')
        self.right_bar_widget_point_altitude_input_holder = QtWidgets.QLabel("建議值為高度的1.5倍")  # 提示文字
        self.right_bar_widget_point_altitude_input_holder.setObjectName("right_bar_widget_point_input_holder")

        # 環繞視野角度
        self.right_bar_tour_point_horizfov = QtWidgets.QLabel('視野角度  Horizfov')              # 文字栏
        self.right_bar_tour_point_horizfov.setObjectName("right_bar_tour_point_label")
        self.right_bar_widget_point_horizfov_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)   # 滑块框栏
        # self.right_bar_widget_point_horizfov_slider.setObjectName('right_bar_widget_qlinedit_point_input')
        self.right_bar_widget_point_horizfov_slider.setMinimum(30) #设置最小值
        self.right_bar_widget_point_horizfov_slider.setMaximum(120) #设置最大值
        self.right_bar_widget_point_horizfov_slider.setSingleStep(1) #设置滑动步长
        self.right_bar_widget_point_horizfov_slider.setValue(60)    # 设置当前值
        self.right_bar_widget_point_horizfov_slider_value = QtWidgets.QLabel("60°")  # 提示文字

        # 環繞傾斜角度 Tilt
        self.right_bar_tour_point_tilt = QtWidgets.QLabel('傾斜角度  Tilt')
        self.right_bar_tour_point_tilt.setObjectName("right_bar_tour_point_label")
        self.right_bar_widget_point_tilt_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)   # 滑块框栏
        self.right_bar_widget_point_tilt_slider.setObjectName('right_bar_widget_qlinedit_point_input')
        self.right_bar_widget_point_tilt_slider.setMinimum(0) #设置最小值
        self.right_bar_widget_point_tilt_slider.setMaximum(90) #设置最大值
        self.right_bar_widget_point_tilt_slider.setSingleStep(1) #设置滑动步长
        self.right_bar_widget_point_tilt_slider.setValue(60)    # 设置当前值
        self.right_bar_widget_point_tilt_slider_value = QtWidgets.QLabel("60°")  # 提示文字
        self.right_bar_widget_point_tilt_slider_holder = QtWidgets.QLabel("0°為正射，90°為水平")      # 提示文字
        self.right_bar_widget_point_tilt_slider_holder.setObjectName("right_bar_widget_point_input_holder")

        # 環繞 啟始方向 Ring Around Start Direction: -180° <--> 180°
        self.right_bar_tour_point_heading = QtWidgets.QLabel('开启方向')
        self.right_bar_tour_point_heading.setObjectName("right_bar_tour_point_label")
        self.right_bar_widget_point_heading_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)   # 滑块框栏
        self.right_bar_widget_point_heading_slider.setObjectName('right_bar_widget_qlinedit_point_input')
        self.right_bar_widget_point_heading_slider.setMinimum(-180) #设置最小值
        self.right_bar_widget_point_heading_slider.setMaximum(180) #设置最大值
        self.right_bar_widget_point_heading_slider.setSingleStep(1) #设置滑动步长
        self.right_bar_widget_point_heading_slider.setValue(0)    # 设置当前值
        self.right_bar_widget_point_heading_slider_value = QtWidgets.QLabel("0°")  # 提示文字

        # 環繞 环绕时间
        self.right_bar_tour_point_tour_time = QtWidgets.QLabel('环绕时间')
        self.right_bar_tour_point_tour_time.setObjectName("right_bar_tour_point_label")
        self.right_bar_widget_point_tour_time_input = QtWidgets.QLineEdit()
        self.right_bar_widget_point_tour_time_input.setPlaceholderText("建议20 ~ 30秒")
        self.right_bar_widget_point_tour_time_input.setText('30')
        self.right_bar_widget_point_tour_time_input.setObjectName('right_bar_widget_qlinedit_point_input')

        # 環繞 方向 clockwise:
        self.right_bar_tour_point_clock = QtWidgets.QLabel('环绕方向')
        self.right_bar_tour_point_clock.setObjectName("right_bar_tour_point_label")
        self.right_bar_tour_point_clock_wise_group_button = QtWidgets.QButtonGroup()    # 按钮分组
        self.right_bar_tour_point_clock_wise_button = QtWidgets.QRadioButton("顺时针")
        self.right_bar_tour_point_clock_wise_button.setObjectName('right_bar_widget_qlinedit_point_input')
        self.right_bar_tour_point_clock_wise_button.setChecked(True)
        self.right_bar_tour_point_counter_clock_wise_button = QtWidgets.QRadioButton("逆时针")
        self.right_bar_tour_point_counter_clock_wise_button.setObjectName('right_bar_widget_qlinedit_point_input')
        self.right_bar_tour_point_clock_wise_group_button.addButton(self.right_bar_tour_point_clock_wise_button, 1)  # 设置ID为1
        self.right_bar_tour_point_clock_wise_group_button.addButton(self.right_bar_tour_point_counter_clock_wise_button, 2)

        self.right_bar_widget_point_button_download = QtWidgets.QPushButton()
        self.right_bar_widget_point_button_download.setText("确定")
        self.right_bar_widget_point_button_download.setObjectName('right_bar_tour_point_button_download')

        self.right_bar_layout.addWidget(self.right_bar_tour_point, 0, 0, 1, 1)  # (跨行的控件，起始行，起始列，跨越的行数，跨越列数)
        self.right_bar_layout.addWidget(self.right_bar_tour_point_kmlname, 0, 0, 4, 1)
        self.right_bar_layout.addWidget(self.right_bar_widget_point_kmlname_input, 0, 1, 4, 3)           #
        self.right_bar_layout.addWidget(self.right_bar_tour_point_longitude, 1, 0, 4, 1)                 # 经度 文字
        self.right_bar_layout.addWidget(self.right_bar_widget_point_longitude_input, 1, 1, 4, 3)         # 经度 输入框
        self.right_bar_layout.addWidget(self.right_bar_widget_point_longitude_input_holder, 1, 4, 4, 2)  # 经度 提示文字
        self.right_bar_layout.addWidget(self.right_bar_tour_point_latitude, 2, 0, 4, 1)                  # 纬度 文字
        self.right_bar_layout.addWidget(self.right_bar_widget_point_latitude_input, 2, 1, 4, 3)          # 纬度 输入框
        self.right_bar_layout.addWidget(self.right_bar_widget_point_latitude_input_holder, 2, 4, 4, 3)   # 纬度 提示文字
        self.right_bar_layout.addWidget(self.right_bar_tour_point_height, 3, 0, 4, 1)                    # 高度 文字
        self.right_bar_layout.addWidget(self.right_bar_widget_point_height_input, 3, 1, 4, 3)            # 高度 输入框
        self.right_bar_layout.addWidget(self.right_bar_widget_point_height_input_holder, 3, 4, 4, 3)     # 高度 提示文字
        self.right_bar_layout.addWidget(self.right_bar_tour_point_radius, 4, 0, 4, 1)                    # 环绕半径 文字
        self.right_bar_layout.addWidget(self.right_bar_widget_point_radius_input, 4, 1, 4, 3)            # 环绕半径 输入框
        self.right_bar_layout.addWidget(self.right_bar_widget_point_radius_input_holder, 4, 4, 4, 3)     # 环绕半径 提示文字
        self.right_bar_layout.addWidget(self.right_bar_tour_point_altitude, 5, 0, 4, 1)                  # 视点高度 文字
        self.right_bar_layout.addWidget(self.right_bar_widget_point_altitude_input, 5, 1, 4, 3)          # 视点高度 输入框
        self.right_bar_layout.addWidget(self.right_bar_widget_point_altitude_input_holder, 5, 4, 4, 3)   # 视点高度 提示文字
        self.right_bar_layout.addWidget(self.right_bar_tour_point_horizfov, 6, 0, 4, 1)                  # 視野角度 文字
        self.right_bar_layout.addWidget(self.right_bar_widget_point_horizfov_slider, 6, 1, 4, 3)         # 視野角度 滑块
        self.right_bar_layout.addWidget(self.right_bar_widget_point_horizfov_slider_value, 6, 4, 4, 1)   # 視野角度 当前值
        self.right_bar_layout.addWidget(self.right_bar_tour_point_tilt, 7, 0, 4, 1)                   # 傾斜角度 文字
        self.right_bar_layout.addWidget(self.right_bar_widget_point_tilt_slider, 7, 1, 4, 3)          # 傾斜角度 滑块
        self.right_bar_layout.addWidget(self.right_bar_widget_point_tilt_slider_value, 7, 4, 4, 1)    # 傾斜角度 当前值
        self.right_bar_layout.addWidget(self.right_bar_widget_point_tilt_slider_holder, 7, 5, 4, 1)   # 傾斜角度 提示文字
        self.right_bar_layout.addWidget(self.right_bar_tour_point_heading, 8, 0, 4, 1)                   # 啟始方向 文字
        self.right_bar_layout.addWidget(self.right_bar_widget_point_heading_slider, 8, 1, 4, 3)          # 啟始方向 滑块
        self.right_bar_layout.addWidget(self.right_bar_widget_point_heading_slider_value, 8, 4, 4, 1)    # 啟始方向 当前值
        self.right_bar_layout.addWidget(self.right_bar_tour_point_tour_time, 9, 0, 4, 1)                 # 環繞方向 文字
        self.right_bar_layout.addWidget(self.right_bar_widget_point_tour_time_input, 9, 1, 4, 3)         # 環繞方向 当前值

        self.right_bar_layout.addWidget(self.right_bar_tour_point_clock, 10, 0, 4, 1)
        self.right_bar_layout.addWidget(self.right_bar_tour_point_clock_wise_button, 10, 1, 4, 3)
        self.right_bar_layout.addWidget(self.right_bar_tour_point_counter_clock_wise_button, 10, 2, 4, 3)
        self.right_bar_layout.addWidget(self.right_bar_widget_point_button_download, 12, 2, 3, 2) # (跨行的控件，起始行，起始列，跨越的行数，跨越列数)


        # ======================右侧点击-环绕浏览====================================================
        # right_tour_point_ring_around
        self.right_bar_point_around_widget = QtWidgets.QWidget()     # 右侧顶部搜索框部件
        self.right_bar_point_around_layout = QtWidgets.QGridLayout() # 右侧顶部搜索框网格布局
        self.right_bar_point_around_widget.setLayout(self.right_bar_point_around_layout)

        self.right_bar_tour_point_around = QtWidgets.QPushButton("环绕浏览")
        self.right_bar_tour_point_around.setObjectName("right_lable_title")

        # 名称输入框
        self.right_bar_tour_point_around_kmlname = QtWidgets.QLabel('名称  Kmlname')
        self.right_bar_tour_point_around_kmlname.setObjectName("right_bar_tour_point_label")
        self.right_bar_widget_point_around_kmlname_input = QtWidgets.QLineEdit()
        self.right_bar_widget_point_around_kmlname_input.setText('上海东方明珠')
        self.right_bar_widget_point_around_kmlname_input.setPlaceholderText("输入要保存的文件名")
        self.right_bar_widget_point_around_kmlname_input.setObjectName('right_bar_widget_qlinedit_point_input')

        # 经度输入框
        self.right_bar_tour_point_around_longitude = QtWidgets.QLabel('经度  Longitude')            # 文字栏
        self.right_bar_tour_point_around_longitude.setObjectName("right_bar_tour_point_label")
        self.right_bar_widget_point_around_longitude_input = QtWidgets.QLineEdit()                 # 输入框栏
        self.right_bar_widget_point_around_longitude_input.setText('121.4952627807584')
        # self.right_bar_widget_point_around_longitude_input.setPlaceholderText("输入经度 十进制度小数")
        self.right_bar_widget_point_around_longitude_input.setObjectName('right_bar_widget_qlinedit_point_input')
        self.right_bar_widget_point_around_longitude_input_holder = QtWidgets.QLabel("输入经度 十进制度小数")  # 提示栏
        self.right_bar_widget_point_around_longitude_input_holder.setObjectName("right_bar_widget_point_input_holder")

        # 纬度输入框
        self.right_bar_tour_point_around_latitude = QtWidgets.QLabel('纬度  Latitude')             # 文字栏
        self.right_bar_tour_point_around_latitude.setObjectName("right_bar_tour_point_label")
        self.right_bar_widget_point_around_latitude_input = QtWidgets.QLineEdit()                 # 输入框栏
        self.right_bar_widget_point_around_latitude_input.setText('31.24188370156092')
        # self.right_bar_widget_point_around_latitude_input.setPlaceholderText("输入纬度 十进制度小数")
        self.right_bar_widget_point_around_latitude_input.setObjectName('right_bar_widget_qlinedit_point_input')
        self.right_bar_widget_point_around_latitude_input_holder = QtWidgets.QLabel("输入纬度 十进制度小数")    # 提示栏
        self.right_bar_widget_point_around_latitude_input_holder.setObjectName("right_bar_widget_point_input_holder")

        # 高度输入框
        self.right_bar_tour_point_around_height = QtWidgets.QLabel('高度  Height')                # 文字栏
        self.right_bar_tour_point_around_height.setObjectName("right_bar_tour_point_label")
        self.right_bar_widget_point_around_height_input = QtWidgets.QLineEdit()                  # 输入框栏
        self.right_bar_widget_point_around_height_input.setText('468')
        # self.right_bar_widget_point_around_height_input.setPlaceholderText("建筑、山体高度")
        self.right_bar_widget_point_around_height_input.setObjectName('right_bar_widget_qlinedit_point_input')
        self.right_bar_widget_point_around_height_input_holder = QtWidgets.QLabel("建筑、山体高度")    # 提示栏
        self.right_bar_widget_point_around_height_input_holder.setObjectName("right_bar_widget_point_input_holder")

        # 环绕半径输入框
        self.right_bar_tour_point_around_radius = QtWidgets.QLabel('环绕半径  Radius')             # 文字栏
        self.right_bar_tour_point_around_radius.setObjectName("right_bar_tour_point_label")
        self.right_bar_widget_point_around_radius_input = QtWidgets.QLineEdit()                  # 输入框栏
        self.right_bar_widget_point_around_radius_input.setText('781')
        # self.right_bar_widget_point_around_radius_input.setPlaceholderText("环绕半径  Radius")
        self.right_bar_widget_point_around_radius_input.setObjectName('right_bar_widget_qlinedit_point_input')
        self.right_bar_widget_point_around_radius_input_holder = QtWidgets.QLabel("建議值為高度的1.67倍 , 0 表為環景")  # 提示文字
        self.right_bar_widget_point_around_radius_input_holder.setObjectName("right_bar_widget_point_input_holder")

        # 環繞視點高度 Height
        self.right_bar_tour_point_around_altitude = QtWidgets.QLabel('视点高度  Altitude')          # 文字栏
        self.right_bar_tour_point_around_altitude.setObjectName("right_bar_tour_point_label")
        self.right_bar_widget_point_around_altitude_input = QtWidgets.QLineEdit()                  # 输入框栏
        self.right_bar_widget_point_around_altitude_input.setText('702')
        self.right_bar_widget_point_around_altitude_input.setPlaceholderText("建議值為高度的1.5倍")
        self.right_bar_widget_point_around_altitude_input.setObjectName('right_bar_widget_qlinedit_point_input')
        self.right_bar_widget_point_around_altitude_input_holder = QtWidgets.QLabel("建議值為高度的1.5倍")  # 提示文字
        self.right_bar_widget_point_around_altitude_input_holder.setObjectName("right_bar_widget_point_input_holder")

        # 環繞視野角度
        self.right_bar_tour_point_around_horizfov = QtWidgets.QLabel('視野角度  Horizfov')              # 文字栏
        self.right_bar_tour_point_around_horizfov.setObjectName("right_bar_tour_point_label")
        self.right_bar_widget_point_around_horizfov_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)   # 滑块框栏
        self.right_bar_widget_point_around_horizfov_slider.setObjectName('right_bar_widget_qlinedit_point_input')
        self.right_bar_widget_point_around_horizfov_slider.setMinimum(30) #设置最小值
        self.right_bar_widget_point_around_horizfov_slider.setMaximum(120) #设置最大值
        self.right_bar_widget_point_around_horizfov_slider.setSingleStep(1) #设置滑动步长
        self.right_bar_widget_point_around_horizfov_slider.setValue(60)    # 设置当前值
        self.right_bar_widget_point_around_horizfov_slider_value = QtWidgets.QLabel("60°")  # 提示文字

        # 環繞傾斜角度 Tilt
        self.right_bar_tour_point_around_tilt = QtWidgets.QLabel('傾斜角度  Tilt')
        self.right_bar_tour_point_around_tilt.setObjectName("right_bar_tour_point_label")
        self.right_bar_widget_point_around_tilt_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)   # 滑块框栏
        self.right_bar_widget_point_around_tilt_slider.setObjectName('right_bar_widget_qlinedit_point_input')
        self.right_bar_widget_point_around_tilt_slider.setMinimum(0) #设置最小值
        self.right_bar_widget_point_around_tilt_slider.setMaximum(90) #设置最大值
        self.right_bar_widget_point_around_tilt_slider.setSingleStep(1) #设置滑动步长
        self.right_bar_widget_point_around_tilt_slider.setValue(60)    # 设置当前值
        self.right_bar_widget_point_around_tilt_slider_value = QtWidgets.QLabel("60°")  # 提示文字
        self.right_bar_widget_point_around_tilt_slider_holder = QtWidgets.QLabel("0°為正射，90°為水平")      # 提示文字
        self.right_bar_widget_point_around_tilt_slider_holder.setObjectName("right_bar_widget_point_input_holder")

        # 環繞 啟始方向 Ring Around Start Direction: -180° <--> 180°
        self.right_bar_tour_point_around_heading = QtWidgets.QLabel('开启方向')
        self.right_bar_tour_point_around_heading.setObjectName("right_bar_tour_point_label")
        self.right_bar_widget_point_around_heading_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)   # 滑块框栏
        self.right_bar_widget_point_around_heading_slider.setObjectName('right_bar_widget_qlinedit_point_input')
        self.right_bar_widget_point_around_heading_slider.setMinimum(-180) #设置最小值
        self.right_bar_widget_point_around_heading_slider.setMaximum(180) #设置最大值
        self.right_bar_widget_point_around_heading_slider.setSingleStep(1) #设置滑动步长
        self.right_bar_widget_point_around_heading_slider.setValue(0)    # 设置当前值
        self.right_bar_widget_point_around_heading_slider_value = QtWidgets.QLabel("0°")  # 提示文字

        # 環繞 环绕时间
        self.right_bar_tour_point_around_tour_time = QtWidgets.QLabel('环绕时间')
        self.right_bar_tour_point_around_tour_time.setObjectName("right_bar_tour_point_label")
        self.right_bar_widget_point_around_tour_time_input = QtWidgets.QLineEdit()
        # self.right_bar_widget_point_tour_time_input.setPlaceholderText("建议20 ~ 30秒")
        self.right_bar_widget_point_around_tour_time_input.setText('30')
        self.right_bar_widget_point_around_tour_time_input.setObjectName('right_bar_widget_qlinedit_point_input')

        # 環繞 方向 clockwise:
        self.right_bar_tour_point_around_clock = QtWidgets.QLabel('环绕方向')
        self.right_bar_tour_point_around_clock.setObjectName("right_bar_tour_point_label")
        self.right_bar_tour_point_around_clock_wise_group_button = QtWidgets.QButtonGroup()    # 按钮分组
        self.right_bar_tour_point_around_clock_wise_button = QtWidgets.QRadioButton("顺时针")
        self.right_bar_tour_point_around_clock_wise_button.setObjectName('right_bar_widget_qlinedit_point_input')
        self.right_bar_tour_point_around_clock_wise_button.setChecked(True)
        self.right_bar_tour_point_around_counter_clock_wise_button = QtWidgets.QRadioButton("逆时针")
        self.right_bar_tour_point_around_counter_clock_wise_button.setObjectName('right_bar_widget_qlinedit_point_input')
        self.right_bar_tour_point_around_clock_wise_group_button.addButton(self.right_bar_tour_point_around_clock_wise_button, 1)  # 设置ID为1
        self.right_bar_tour_point_around_clock_wise_group_button.addButton(self.right_bar_tour_point_around_counter_clock_wise_button, 2)

        self.right_bar_widget_point_around_button_download = QtWidgets.QPushButton()
        self.right_bar_widget_point_around_button_download.setText("确定")
        self.right_bar_widget_point_around_button_download.setObjectName('right_bar_tour_point_button_download')

        self.right_bar_point_around_layout.addWidget(self.right_bar_tour_point_around, 0, 0, 1, 1)  # (跨行的控件，起始行，起始列，跨越的行数，跨越列数)
        self.right_bar_point_around_layout.addWidget(self.right_bar_tour_point_around_kmlname, 0, 0, 4, 1)
        self.right_bar_point_around_layout.addWidget(self.right_bar_widget_point_around_kmlname_input, 0, 1, 4, 3)
        self.right_bar_point_around_layout.addWidget(self.right_bar_tour_point_around_longitude, 1, 0, 4, 1)                 # 经度 文字
        self.right_bar_point_around_layout.addWidget(self.right_bar_widget_point_around_longitude_input, 1, 1, 4, 3)         # 经度 输入框
        self.right_bar_point_around_layout.addWidget(self.right_bar_widget_point_around_longitude_input_holder, 1, 4, 4, 2)  # 经度 提示文字
        self.right_bar_point_around_layout.addWidget(self.right_bar_tour_point_around_latitude, 2, 0, 4, 1)                  # 纬度 文字
        self.right_bar_point_around_layout.addWidget(self.right_bar_widget_point_around_latitude_input, 2, 1, 4, 3)          # 纬度 输入框
        self.right_bar_point_around_layout.addWidget(self.right_bar_widget_point_around_latitude_input_holder, 2, 4, 4, 3)   # 纬度 提示文字
        self.right_bar_point_around_layout.addWidget(self.right_bar_tour_point_around_height, 3, 0, 4, 1)                    # 高度 文字
        self.right_bar_point_around_layout.addWidget(self.right_bar_widget_point_around_height_input, 3, 1, 4, 3)            # 高度 输入框
        self.right_bar_point_around_layout.addWidget(self.right_bar_widget_point_around_height_input_holder, 3, 4, 4, 3)     # 高度 提示文字
        self.right_bar_point_around_layout.addWidget(self.right_bar_tour_point_around_radius, 4, 0, 4, 1)                    # 环绕半径 文字
        self.right_bar_point_around_layout.addWidget(self.right_bar_widget_point_around_radius_input, 4, 1, 4, 3)            # 环绕半径 输入框
        self.right_bar_point_around_layout.addWidget(self.right_bar_widget_point_around_radius_input_holder, 4, 4, 4, 3)     # 环绕半径 提示文字
        self.right_bar_point_around_layout.addWidget(self.right_bar_tour_point_around_altitude, 5, 0, 4, 1)                  # 视点高度 文字
        self.right_bar_point_around_layout.addWidget(self.right_bar_widget_point_around_altitude_input, 5, 1, 4, 3)          # 视点高度 输入框
        self.right_bar_point_around_layout.addWidget(self.right_bar_widget_point_around_altitude_input_holder, 5, 4, 4, 3)   # 视点高度 提示文字
        self.right_bar_point_around_layout.addWidget(self.right_bar_tour_point_around_horizfov, 6, 0, 4, 1)                  # 視野角度 文字
        self.right_bar_point_around_layout.addWidget(self.right_bar_widget_point_around_horizfov_slider, 6, 1, 4, 3)         # 視野角度 滑块
        self.right_bar_point_around_layout.addWidget(self.right_bar_widget_point_around_horizfov_slider_value, 6, 4, 4, 1)   # 視野角度 当前值
        self.right_bar_point_around_layout.addWidget(self.right_bar_tour_point_around_tilt, 7, 0, 4, 1)                   # 傾斜角度 文字
        self.right_bar_point_around_layout.addWidget(self.right_bar_widget_point_around_tilt_slider, 7, 1, 4, 3)          # 傾斜角度 滑块
        self.right_bar_point_around_layout.addWidget(self.right_bar_widget_point_around_tilt_slider_value, 7, 4, 4, 1)    # 傾斜角度 当前值
        self.right_bar_point_around_layout.addWidget(self.right_bar_widget_point_around_tilt_slider_holder, 7, 5, 4, 1)   # 傾斜角度 提示文字
        self.right_bar_point_around_layout.addWidget(self.right_bar_tour_point_around_heading, 8, 0, 4, 1)                   # 啟始方向 文字
        self.right_bar_point_around_layout.addWidget(self.right_bar_widget_point_around_heading_slider, 8, 1, 4, 3)          # 啟始方向 滑块
        self.right_bar_point_around_layout.addWidget(self.right_bar_widget_point_around_heading_slider_value, 8, 4, 4, 1)    # 啟始方向 当前值
        self.right_bar_point_around_layout.addWidget(self.right_bar_tour_point_around_tour_time, 9, 0, 4, 1)                 # 環繞方向 文字
        self.right_bar_point_around_layout.addWidget(self.right_bar_widget_point_around_tour_time_input, 9, 1, 4, 3)         # 環繞方向 当前值

        self.right_bar_point_around_layout.addWidget(self.right_bar_tour_point_around_clock, 10, 0, 4, 1)
        self.right_bar_point_around_layout.addWidget(self.right_bar_tour_point_around_clock_wise_button, 10, 1, 4, 3)
        self.right_bar_point_around_layout.addWidget(self.right_bar_tour_point_around_counter_clock_wise_button, 10, 2, 4, 3)
        self.right_bar_point_around_layout.addWidget(self.right_bar_widget_point_around_button_download, 12, 2, 3, 2) # (跨行的控件，起始行，起始列，跨越的行数，跨越列数)


        # ======================右侧点击-线路浏览====================================================
        self.right_bar_point_line_widget = QtWidgets.QWidget()  # 右侧顶部搜索框部件
        self.right_bar_point_line_layout = QtWidgets.QGridLayout()  # 右侧顶部搜索框网格布局
        self.right_bar_point_line_widget.setLayout(self.right_bar_point_line_layout)

        self.right_bar_tour_point_line = QtWidgets.QPushButton("线路浏览")
        self.right_bar_tour_point_line.setObjectName("right_lable_title")

        # 线路浏览 线路浏览  名称输入框
        self.right_bar_tour_point_line_kmlname = QtWidgets.QLabel('名称  Kmlname')
        self.right_bar_tour_point_line_kmlname.setObjectName("right_bar_tour_point_label")
        self.right_bar_widget_point_line_kmlname_input = QtWidgets.QLineEdit()
        self.right_bar_widget_point_line_kmlname_input.setText('上海东方明珠')
        self.right_bar_widget_point_line_kmlname_input.setPlaceholderText("输入要保存的文件名")
        self.right_bar_widget_point_line_kmlname_input.setObjectName('right_bar_widget_qlinedit_point_input')

        # 线路浏览 线路浏览  浏览样式
        self.right_bar_tour_point_line_tour_type = QtWidgets.QLabel('浏览方式')
        self.right_bar_tour_point_line_tour_type.setObjectName("right_bar_tour_point_label")
        self.right_bar_widget_point_line_tour_type_input = QtWidgets.QComboBox()
        self.right_bar_widget_point_line_tour_type_input.addItems(["仅路线", "生长路线-固定视角", "生长路线-环绕视角", "生长路线-跟随视角", "节段路线-环绕视角", "节段路线-跟随视角"])
        self.right_bar_widget_point_line_tour_type_input.setObjectName('right_bar_widget_combobox_point_input')



        # self.right_bar_widget_point_line_kmlname_input = QtWidgets.QLineEdit()
        # self.right_bar_widget_point_line_kmlname_input.setText('上海东方明珠')
        # self.right_bar_widget_point_line_kmlname_input.setPlaceholderText("输入要保存的文件名")
        # self.right_bar_widget_point_line_kmlname_input.setObjectName('right_bar_widget_qlinedit_point_input')

        # 线路浏览 线路浏览 环绕时间
        self.right_bar_tour_point_line_tour_time = QtWidgets.QLabel('环绕时间')
        self.right_bar_tour_point_line_tour_time.setObjectName("right_bar_tour_point_label")
        self.right_bar_widget_point_line_tour_time_input = QtWidgets.QLineEdit()
        self.right_bar_widget_point_line_tour_time_input.setText('30')
        self.right_bar_widget_point_line_tour_time_input.setObjectName('right_bar_widget_qlinedit_point_input')
        self.right_bar_widget_point_line_tour_time_input_holder = QtWidgets.QLabel("")  # 提示文字
        self.right_bar_widget_point_line_tour_time_input_holder.setObjectName("right_bar_widget_point_input_holder")


        self.right_bar_point_line_layout.addWidget(self.right_bar_tour_point_line, 0, 0, 1, 1)  # (跨行的控件，起始行，起始列，跨越的行数，跨越列数)
        self.right_bar_point_line_layout.addWidget(self.right_bar_tour_point_line_kmlname, 0, 0, 4, 1)            # 线路浏览 文件名 文字
        self.right_bar_point_line_layout.addWidget(self.right_bar_widget_point_line_kmlname_input, 0, 1, 4, 3)    # 线路浏览 文件名 输入框

        self.right_bar_point_line_layout.addWidget(self.right_bar_tour_point_line_tour_type, 1, 0, 4, 1)          # 线路浏览 浏览样式 文字
        self.right_bar_point_line_layout.addWidget(self.right_bar_widget_point_line_tour_type_input, 1, 1, 4, 3)  # 线路浏览 浏览样式 输入框

        self.right_bar_point_line_layout.addWidget(self.right_bar_tour_point_line_tour_time, 2, 0, 4, 1)          # 线路浏览 时间 文字
        self.right_bar_point_line_layout.addWidget(self.right_bar_widget_point_line_tour_time_input, 2, 1, 4, 3)  # 线路浏览 时间 输入框
        self.right_bar_point_line_layout.addWidget(self.right_bar_widget_point_line_tour_time_input_holder, 2, 4, 4, 3)   # 环绕半径 提示文字


        # ======================右侧点击-圆环饼图====================================================
        self.right_bar_point_ring_widget = QtWidgets.QWidget()  # 右侧顶部搜索框部件
        self.right_bar_point_ring_layout = QtWidgets.QGridLayout()  # 右侧顶部搜索框网格布局
        self.right_bar_point_ring_widget.setLayout(self.right_bar_point_ring_layout)

        self.right_bar_tour_point_ring = QtWidgets.QPushButton("圆环饼图")
        self.right_bar_tour_point_ring.setObjectName("right_lable_title")

        # 坐标浏览 圆环饼图 名称输入框
        self.right_bar_tour_point_ring_kmlname = QtWidgets.QLabel('名称  Kmlname')
        self.right_bar_tour_point_ring_kmlname.setObjectName("right_bar_tour_point_label")
        self.right_bar_widget_point_ring_kmlname_input = QtWidgets.QLineEdit()
        self.right_bar_widget_point_ring_kmlname_input.setText('上海东方明珠')
        self.right_bar_widget_point_ring_kmlname_input.setPlaceholderText("输入要保存的文件名")
        self.right_bar_widget_point_ring_kmlname_input.setObjectName('right_bar_widget_qlinedit_point_input')

        # 坐标浏览 圆环饼图 经度输入框
        self.right_bar_tour_point_ring_longitude = QtWidgets.QLabel('经度  Longitude')  # 文字栏
        self.right_bar_tour_point_ring_longitude.setObjectName("right_bar_tour_point_label")
        self.right_bar_widget_point_ring_longitude_input = QtWidgets.QLineEdit()  # 输入框栏
        self.right_bar_widget_point_ring_longitude_input.setText('121.4952627807584')
        self.right_bar_widget_point_ring_longitude_input.setPlaceholderText("输入经度 十进制度小数")
        self.right_bar_widget_point_ring_longitude_input.setObjectName('right_bar_widget_qlinedit_point_input')
        self.right_bar_widget_point_ring_longitude_input_holder = QtWidgets.QLabel("输入经度 十进制度小数")  # 提示栏
        self.right_bar_widget_point_ring_longitude_input_holder.setObjectName("right_bar_widget_point_input_holder")

        # 坐标浏览 圆环饼图 纬度输入框
        self.right_bar_tour_point_ring_latitude = QtWidgets.QLabel('纬度  Latitude')  # 文字栏
        self.right_bar_tour_point_ring_latitude.setObjectName("right_bar_tour_point_label")
        self.right_bar_widget_point_ring_latitude_input = QtWidgets.QLineEdit()  # 输入框栏
        self.right_bar_widget_point_ring_latitude_input.setText('31.24188370156092')
        self.right_bar_widget_point_ring_latitude_input.setPlaceholderText("输入纬度 十进制度小数")
        self.right_bar_widget_point_ring_latitude_input.setObjectName('right_bar_widget_qlinedit_point_input')
        self.right_bar_widget_point_ring_latitude_input_holder = QtWidgets.QLabel("输入纬度 十进制度小数")  # 提示栏
        self.right_bar_widget_point_ring_latitude_input_holder.setObjectName("right_bar_widget_point_input_holder")

        # 坐标浏览 圆环饼图 圆外半径   outer_radius
        self.right_bar_tour_point_ring_outer_radius = QtWidgets.QLabel('外圆半径  Radius')        # 文字栏
        self.right_bar_tour_point_ring_outer_radius.setObjectName("right_bar_tour_point_label")
        self.right_bar_widget_point_ring_outer_radius_input = QtWidgets.QLineEdit()              # 输入框栏
        self.right_bar_widget_point_ring_outer_radius_input.setText('468')
        self.right_bar_widget_point_ring_outer_radius_input.setPlaceholderText("外圆半径")
        self.right_bar_widget_point_ring_outer_radius_input.setObjectName('right_bar_widget_qlinedit_point_input')


        # 坐标浏览 圆环饼图 环宽 inner_radius
        self.right_bar_tour_point_ring_inner_radius = QtWidgets.QLabel('内圆半径  Radius')        # 文字栏
        self.right_bar_tour_point_ring_inner_radius.setObjectName("right_bar_tour_point_label")
        self.right_bar_widget_point_ring_inner_radius_input = QtWidgets.QLineEdit()              # 输入框栏
        self.right_bar_widget_point_ring_inner_radius_input.setText('0')
        self.right_bar_widget_point_ring_inner_radius_input.setPlaceholderText("内圆半径")

        self.right_bar_widget_point_ring_inner_radius_input.setObjectName('right_bar_widget_qlinedit_point_input')
        self.right_bar_widget_point_ring_inner_radius_input_holder_value = QtWidgets.QLabel("0则实心圆")  # 提示文字

        # 坐标浏览 圆环饼图 下载
        self.right_bar_widget_point_ring_button_download = QtWidgets.QPushButton()
        self.right_bar_widget_point_ring_button_download.setText("确定")
        self.right_bar_widget_point_ring_button_download.setObjectName('right_bar_tour_point_button_download')
        self.right_bar_widget_point_ring_placeholder = QtWidgets.QLabel("")  # 占位符


        self.right_bar_point_ring_layout.addWidget(self.right_bar_tour_point_ring, 0, 0, 1, 1)  # (跨行的控件，起始行，起始列，跨越的行数，跨越列数)
        self.right_bar_point_ring_layout.addWidget(self.right_bar_tour_point_ring_kmlname, 0, 0, 4, 1)
        self.right_bar_point_ring_layout.addWidget(self.right_bar_widget_point_ring_kmlname_input, 0, 1, 4, 3)
        self.right_bar_point_ring_layout.addWidget(self.right_bar_tour_point_ring_longitude, 1, 0, 4, 1)                       # 圆环饼图 经度 文字
        self.right_bar_point_ring_layout.addWidget(self.right_bar_widget_point_ring_longitude_input, 1, 1, 4, 3)               # 圆环饼图 经度 输入框
        self.right_bar_point_ring_layout.addWidget(self.right_bar_widget_point_ring_longitude_input_holder, 1, 4, 4, 2)        # 圆环饼图 经度 提示文字
        self.right_bar_point_ring_layout.addWidget(self.right_bar_tour_point_ring_latitude, 2, 0, 4, 1)                        # 圆环饼图 纬度 文字
        self.right_bar_point_ring_layout.addWidget(self.right_bar_widget_point_ring_latitude_input, 2, 1, 4, 3)                # 圆环饼图 纬度 输入框
        self.right_bar_point_ring_layout.addWidget(self.right_bar_widget_point_ring_latitude_input_holder, 2, 4, 4, 3)         # 圆环饼图 纬度 提示文字
        self.right_bar_point_ring_layout.addWidget(self.right_bar_tour_point_ring_outer_radius, 3, 0, 4, 1)                    # 圆环饼图 圆外半径 文字
        self.right_bar_point_ring_layout.addWidget(self.right_bar_widget_point_ring_outer_radius_input, 3, 1, 4,3)             # 圆环饼图 圆外半径 输入框
        self.right_bar_point_ring_layout.addWidget(self.right_bar_tour_point_ring_inner_radius, 4, 0, 4, 1)                      # 圆环饼图 环绕宽度 文字
        self.right_bar_point_ring_layout.addWidget(self.right_bar_widget_point_ring_inner_radius_input, 4, 1, 4, 3)              # 圆环饼图 环绕宽度 输入框
        self.right_bar_point_ring_layout.addWidget(self.right_bar_widget_point_ring_inner_radius_input_holder_value, 4, 4, 4, 1) # 圆环饼图 环绕宽度 当前值
        self.right_bar_point_ring_layout.addWidget(self.right_bar_widget_point_ring_button_download, 5, 1, 4, 2)               # (跨行的控件，起始行，起始列，跨越的行数，跨越列数)
        self.right_bar_point_ring_layout.addWidget(self.right_bar_widget_point_ring_placeholder, 18, 2, 4, 2)                   # 圆环饼图 环绕宽度 占位符

        # ======================右侧表格的样式=== ========================================================
        # 主界面 - 左侧导航栏样式
        self.left_widget.setStyleSheet(
            '''
                QPushButton{border:none;color:white;}
                QPushButton#left_label{
                    border:none;
                    border-bottom:1px solid white;
                    font-size:18px;
                    font-weight:700;
                    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                }
                QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}
                QWidget#left_widget{
                    background:gray;
                    border-top:1px solid white;
                    border-bottom:1px solid white;
                    border-left:1px solid white;
                    border-top-left-radius:10px;
                    border-bottom-left-radius:10px;
                }
            '''
        )

        self.right_widget.setStyleSheet(
            '''
                QWidget#right_widget{
                    color:#232C51;
                    background:white;
                    border-top:1px solid darkGray;
                    border-bottom:1px solid darkGray;
                    border-right:1px solid darkGray;
                    border-top-right-radius:10px;
                    border-bottom-right-radius:10px;
                }
                QPushButton#right_lable_title{
                    border:none;
                    font-size:28px;
                    font-weight:700;
                    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                }
            '''
        )

        # 坐标环绕  四顾浏览样式
        self.right_bar_widget.setStyleSheet(
            '''
                QLineEdit#right_bar_widget_qlinedit_point_input{
                    border-radius: 4px;
                    border: 1px solid gray;  
                    height:30px;
                    font-size:16px;
                    font-weight:200;
                    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                }
                QLabel#right_bar_tour_point_label{
                    height:30px;
                    font-size:16px;
                    font-weight:400;
                    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                }
                QPushButton#right_bar_tour_point_button{
                    height:30px;
                    border-radius: 4px;
                    border: 1px solid gray;  
                    font-size:16px;
                    font-weight:200;
                    background-color: white;
                    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                }
                QProgressBar::chunk {
                    background-color: #F76677;
                }
                QPushButton#right_bar_tour_point_button_download{
                    height:30px;
                    border-radius: 4px;
                    border: 1px solid gray;  
                    background-color: gray;
                    font-size:16px;
                    font-weight:500;
                    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                }
            '''
        )

        # 坐标环绕  环绕浏览样式
        self.right_bar_point_around_widget.setStyleSheet(
            '''
                QLineEdit#right_bar_widget_qlinedit_point_input{
                    height:30px;
                    border-radius: 4px;
                    border: 1px solid gray;
                    font-size:16px;
                    font-weight:200;
                    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                }
                QLabel#right_bar_tour_point_label{
                    height:30px;
                    font-size:16px;
                    font-weight:400;
                    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                }
                QPushButton#right_bar_tour_point_button{
                    height:30px;
                    border-radius: 4px;
                    border: 1px solid gray;
                    font-size:16px;
                    font-weight:200;
                    background-color: white;
                    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                }
                QProgressBar::chunk {
                    background-color: #F76677;
                }
                QPushButton#right_bar_tour_point_button_download{
                    height:30px;
                    border-radius: 4px;
                    border: 1px solid gray;
                    background-color: gray;
                    font-size:16px;
                    font-weight:500;
                    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                }
            '''
        )
        # 坐标环绕  圆环饼图样式
        self.right_bar_point_ring_widget.setStyleSheet(
            '''
                QLineEdit#right_bar_widget_qlinedit_point_input{
                    height:30px;
                    border-radius: 4px;
                    border: 1px solid gray;
                    font-size:16px;
                    font-weight:200;
                    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                }
                QLabel#right_bar_tour_point_label{
                    height:30px;
                    font-size:16px;
                    font-weight:400;
                    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                }
                QPushButton#right_bar_tour_point_button{
                    height:30px;
                    border-radius: 4px;
                    border: 1px solid gray;
                    font-size:16px;
                    font-weight:200;
                    background-color: white;
                    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                }
                QPushButton#right_bar_tour_point_button_download{
                    height:30px;
                    border-radius: 4px;
                    border: 1px solid gray;
                    background-color: gray;
                    font-size:16px;
                    font-weight:500;
                    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                }
            '''
        )

        # 坐标环绕  圆环饼图样式
        self.right_bar_point_line_widget.setStyleSheet(
            '''
                QLineEdit#right_bar_widget_qlinedit_point_input{
                    height:30px;
                    border-radius: 4px;
                    border: 1px solid gray;
                    font-size:16px;
                    font-weight:200;
                    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                }
                QLabel#right_bar_tour_point_label{
                    height:30px;
                    font-size:16px;
                    font-weight:400;
                    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                }
                QPushButton#right_bar_tour_point_button{
                    height:30px;
                    border-radius: 4px;
                    border: 1px solid gray;
                    font-size:16px;
                    font-weight:200;
                    background-color: white;
                    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                }
                QPushButton#right_bar_tour_point_button_download{
                    height:30px;
                    border-radius: 4px;
                    border: 1px solid gray;
                    background-color: gray;
                    font-size:16px;
                    font-weight:500;
                    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                }
                
                QComboBox#right_bar_widget_combobox_point_input{
                    height:30px;
                    border-radius: 4px;
                    border: 1px solid gray;
                    font-size:16px;
                    font-weight:200;
                    font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                }
            '''
        )

        # ======================设置网格布局层中部件的间隙=== ========================================================
        self.right_layout.addWidget(self.right_bar_widget, 2, 0, 1, 9)               # 注册右侧 中心浏览
        self.right_layout.addWidget(self.right_bar_point_around_widget, 2, 0, 1, 9)  # 注册右侧 环绕浏览
        self.right_layout.addWidget(self.right_bar_point_ring_widget, 2, 0, 1, 9)    # 注册右侧 圆环饼图
        self.right_layout.addWidget(self.right_bar_point_line_widget, 2, 0, 1, 9)    # 注册右侧 圆环饼图
        self.right_bar_point_around_widget.hide()
        self.right_bar_point_ring_widget.hide()
        self.right_bar_point_line_widget.hide()
        self.right_bar_widget.show()


        self.main_layout.setSpacing(0)  # 设置网格布局层中部件的间隙

        # ======================左侧导航栏被点击===========================================================
        self.left_close.clicked.connect(self.on_left_widget_button_clicked)   # 关闭按钮
        self.left_mini.clicked.connect(self.on_left_widget_button_clicked)    # 最小化按钮
        self.left_button_1.clicked.connect(self.on_left_widget_button_clicked)   # 四顾浏览
        self.left_button_2.clicked.connect(self.on_left_widget_button_clicked)   # 环绕浏览
        self.left_button_3.clicked.connect(self.on_left_widget_button_clicked)   # 圆饼环图
        self.left_button_4.clicked.connect(self.on_left_widget_button_clicked)   # 圆饼环图

        # ======================坐标浏览 圆环饼图 下载====================================================
        self.right_bar_widget_point_ring_button_download.clicked.connect(self.on_tour_point_ring_kmlname_push_button_clicked)

        # ======================环绕浏览 由中心向周围 观看====================================================
        # 事件监听 环绕浏览 高度 Altitude 環繞半徑 Radius 環繞視點高度 Height
        self.right_bar_widget_point_around_height_input.textChanged.connect(self.right_bar_widget_point_around_height_slider_connect)
        # 事件监听 环绕浏览 環繞視野角度 horizfov 提示
        self.right_bar_widget_point_around_horizfov_slider.valueChanged.connect(self.right_bar_widget_point_around_horizfov_slider_connect)
        # 事件监听 环绕浏览  環繞傾斜角度 Tilt 提示
        self.right_bar_widget_point_around_tilt_slider.valueChanged.connect(self.right_bar_widget_point_around_tilt_slider_connect)
        # 事件监听 环绕浏览  環繞啟始方向 heading 提示
        self.right_bar_widget_point_around_heading_slider.valueChanged.connect(self.right_bar_widget_point_around_heading_slider_connect)
        self.right_bar_widget_point_around_button_download.clicked.connect(self.on_tour_point_around_kmlname_push_button_clicked)

        # ======================四顾浏览 由中心向周围 观看====================================================
        # 事件监听 四顾浏览 高度 Altitude 環繞半徑 Radius 環繞視點高度 Height
        self.right_bar_widget_point_height_input.textChanged.connect(self.right_bar_widget_point_height_slider_connect)
        # 事件监听 四顾浏览 環繞視野角度 horizfov 提示
        self.right_bar_widget_point_horizfov_slider.valueChanged.connect(self.right_bar_widget_point_horizfov_slider_connect)
        # 事件监听 四顾浏览  環繞傾斜角度 Tilt 提示
        self.right_bar_widget_point_tilt_slider.valueChanged.connect(self.right_bar_widget_point_tilt_slider_connect)
        # 事件监听 四顾浏览  環繞啟始方向 heading 提示
        self.right_bar_widget_point_heading_slider.valueChanged.connect(self.right_bar_widget_point_heading_slider_connect)
        self.right_bar_widget_point_button_download.clicked.connect(self.on_tour_point_kmlname_push_button_clicked)

        # ======================主控件  观看====================================================
        self.setCentralWidget(self.main_widget)                # 设置窗口主部件
        self.setWindowOpacity(0.9) # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) # 设置窗口背景透明
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint) # 隐藏边框

    def on_left_widget_button_clicked(self, value):

        left_sender = self.sender().text()
        print(left_sender)
        if left_sender == 'x':
            self.close()
        if left_sender == '-':
            self.showMinimized()
        if left_sender == '四顾浏览':
            self.right_bar_point_ring_widget.hide()
            self.right_bar_point_around_widget.hide()
            self.right_bar_point_line_widget.hide()
            self.right_bar_widget.show()
        if left_sender == '环绕浏览':
            self.right_bar_widget.hide()
            self.right_bar_point_ring_widget.hide()
            self.right_bar_point_line_widget.hide()
            self.right_bar_point_around_widget.show()
        if left_sender == "圆饼环图":
            self.right_bar_widget.hide()
            self.right_bar_point_around_widget.hide()
            self.right_bar_point_line_widget.hide()
            self.right_bar_point_ring_widget.show()
        if left_sender == "线路浏览":
            self.right_bar_widget.hide()
            self.right_bar_point_around_widget.hide()
            self.right_bar_point_ring_widget.hide()
            self.right_bar_point_line_widget.show()

    # =========point===========圆环饼图=================================================
    def on_tour_point_ring_kmlname_push_button_clicked(self):
        """
        环绕浏览 啟始方向 当前值
        :param value:
        :return:
        """
        data = {
            'kmlname': self.right_bar_widget_point_ring_kmlname_input.text(),
            'latitude': float(self.right_bar_widget_point_ring_latitude_input.text()),
            'longitude' : float(self.right_bar_widget_point_ring_longitude_input.text()),
            'outer_radius': int(self.right_bar_widget_point_ring_outer_radius_input.text()),
            'inner_radius' : int(self.right_bar_widget_point_ring_inner_radius_input.text())
        }
        print(data)
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

    # =========point===========环绕浏览=================================================
    def right_bar_widget_point_around_horizfov_slider_connect(self, value):
        """
        环绕浏览 環繞視野角度 提示
        :return:
        """
        slider_horizfov_value = self.right_bar_widget_point_around_horizfov_slider.value()  # 获取当前滑块值
        self.right_bar_widget_point_around_horizfov_slider_value.setText('%s°' % slider_horizfov_value)

    def right_bar_widget_point_around_tilt_slider_connect(self, value):
        """
        环绕浏览 啟始方向 当前值
        :param value:
        :return:
        """
        slider_tilt_value = self.right_bar_widget_point_around_tilt_slider.value()  # 获取当前滑块值
        self.right_bar_widget_point_around_tilt_slider_value.setText('%s°' % slider_tilt_value)

    def right_bar_widget_point_around_heading_slider_connect(self, value):
        """
        环绕浏览 啟始方向 当前值
        :param value:
        :return:
        """
        slider_heading_value = self.right_bar_widget_point_around_heading_slider.value()  # 获取当前滑块值
        self.right_bar_widget_point_around_heading_slider_value.setText('%s°' % slider_heading_value)

    def right_bar_widget_point_around_height_slider_connect(self):
        """
        环绕浏览 建筑物高度 当前值
        :param value:
        :return:
        """
        try:
            height = self.right_bar_widget_point_around_height_input.text()
            self.right_bar_widget_point_around_radius_input.setText(str(int(int(height) * 1.67)))
            self.right_bar_widget_point_around_altitude_input.setText(str(int(int(height) * 1.5)))
        except:
            self.toast = Toast(text='你输入有误', duration=1, parent=self)
            self.toast.setBackgroundColor(QtGui.QColor(255, 0, 0, 127))
            self.toast.show()

    # 下载按钮事件
    def on_tour_point_around_kmlname_push_button_clicked(self):
        """
        环绕浏览  下载按钮事件
        :return:
        """
        try:
            TourPointAround().tour_point_around(
                kmlname=self.right_bar_widget_point_around_kmlname_input.text(),
                longitude=float(self.right_bar_widget_point_around_longitude_input.text()),  # 经度
                latitude=float(self.right_bar_widget_point_around_latitude_input.text()),    # 纬度
                altitude=self.right_bar_widget_point_around_altitude_input.text(),    # 实际:467.9   高度 1.67 倍
                horizfov=self.right_bar_widget_point_around_horizfov_slider.value(),
                tilt=self.right_bar_widget_point_around_tilt_slider.value(),          # 环绕倾斜角度
                heading=int(self.right_bar_widget_point_around_heading_slider.value()),
                radius=int(self.right_bar_widget_point_around_radius_input.text()),
                roll=0,
                tour_time=int(self.right_bar_widget_point_around_tour_time_input.text()),  # 环绕一圈時間,
                clock=1 if self.right_bar_tour_point_around_clock_wise_button.isChecked() else 0
            )
            QtWidgets.QMessageBox.information(self, "提示", "下载成功！")
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(e)
            QtWidgets.QMessageBox.warning(self, "提示", "输入的数据有误!")


    # =========point===========四顾浏览=================================================
    def right_bar_widget_point_horizfov_slider_connect(self, value):
        """
        四顾浏览 環繞視野角度 提示
        :return:
        """
        slider_horizfov_value = self.right_bar_widget_point_horizfov_slider.value()   # 获取当前滑块值
        self.right_bar_widget_point_horizfov_slider_value.setText('%s°' % slider_horizfov_value)

    def right_bar_widget_point_tilt_slider_connect(self, value):
        """
        环绕浏览 啟始方向 当前值
        :param value:
        :return:
        """
        slider_tilt_value = self.right_bar_widget_point_tilt_slider.value()   # 获取当前滑块值
        self.right_bar_widget_point_tilt_slider_value.setText('%s°' % slider_tilt_value)

    def right_bar_widget_point_heading_slider_connect(self, value):
        """
        环绕浏览 啟始方向 当前值
        :param value:
        :return:
        """
        slider_heading_value = self.right_bar_widget_point_heading_slider.value()   # 获取当前滑块值
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

        data = {
            "kmlname": self.right_bar_widget_point_kmlname_input.text(),
            "longitude": self.right_bar_widget_point_longitude_input.text(),
            "latitude": self.right_bar_widget_point_latitude_input.text(),
            "height": self.right_bar_widget_point_height_input.text(),
            "radius": self.right_bar_widget_point_radius_input.text(),
            "altitude": self.right_bar_widget_point_altitude_input.text(),
            "horizfov": self.right_bar_widget_point_horizfov_slider.value(),
            "tilt": self.right_bar_widget_point_tilt_slider.value(),
            "heading": self.right_bar_widget_point_tilt_slider.value(),
            "tour_time": self.right_bar_widget_point_tour_time_input.text(),
            "clock": 1 if self.right_bar_tour_point_clock_wise_button.isChecked() else 0
        }
        print(data)


        try:
            TourPointCentre().tour_point_centre(
                kmlname=self.right_bar_widget_point_kmlname_input.text(),
                longitude=self.right_bar_widget_point_longitude_input.text(),       # 经度
                latitude=self.right_bar_widget_point_latitude_input.text(),         # 纬度
                altitude=self.right_bar_widget_point_altitude_input.text(),         # 实际:467.9   高度 1.67 倍
                tilt=self.right_bar_widget_point_tilt_slider.value(),               # 环绕倾斜角度
                tour_time=int(self.right_bar_widget_point_tour_time_input.text()),  # 环绕一圈時間,
                clock=1 if self.right_bar_tour_point_clock_wise_button.isChecked() else 0
            )
            QtWidgets.QMessageBox.information(self, "提示", "下载成功！")
        except:
            QtWidgets.QMessageBox.warning(self, "提示", "输入的数据有误!")

    # 重写三个方法使我们的Example窗口支持拖动,上面参数window就是拖动对象
    def mousePressEvent(self, event): # 鼠标长按事件
        if event.button() == QtCore.Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))

    def mouseMoveEvent(self, QMouseEvent): # 鼠标移动事件
        if QtCore.Qt.LeftButton and self.m_drag:
            self.move(QMouseEvent.globalPos() - self.m_DragPosition)
            QMouseEvent.accept()
        pass

    def mouseReleaseEvent(self, QMouseEvent): # 鼠标释放事件
        self.m_drag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def paintEvent(self, ev): # 重绘窗口边框线条
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