import os
import sys
import time
import traceback

import simplekml
import qtawesome
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor
from pyqt_toast import Toast

from tour.tour_point_centre import TourPointCentre
from tour.tour_point_around import TourPointAround
from tour.tour_point_ring import TourPointRing
from tour.tour_point_day24 import TourPointDay24
from tour.tour_polygon_show import TourPolygonShow
from tour.tour_polygon_change import TourChangePolygon

from settings.constant import UPLOAD_PATH, EXPIRED_DATE, EXPIRED_WARN
from settings.qss_style import LEFT_WIDGET_STYLE_SHEET, RIGHT_WIDGET_STYLE_SHEET
from utlis.parser_line_coords import parser_line_coords, parser_line_distance, parser_polygon_coords
from utlis.my_thread import ThreadLine, ThreadPolygon
from settings.model import LuckyAreas

class MainUi(QtWidgets.QMainWindow):

    def __init__(self):

        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(960, 700)
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout)  # 设置左侧部件布局为网格

        # ======================右侧点击-中心浏览====================================================
        self.right_widget = QtWidgets.QWidget()  # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout)  # 设置右侧部件布局为网格

        # 右侧先在此注册 - 然后默认隐藏
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

        self.left_button_1 = QtWidgets.QPushButton(qtawesome.icon('fa.music', color='white'), "四顾浏览")
        self.left_button_1.setObjectName('left_button')
        self.left_button_2 = QtWidgets.QPushButton(qtawesome.icon('fa.sellsy', color='white'), "环绕浏览")
        self.left_button_2.setObjectName('left_button')
        self.left_button_10 = QtWidgets.QPushButton(qtawesome.icon('fa.sellsy', color='white'), "缩时环景")
        self.left_button_10.setObjectName('left_button')
        self.left_button_3 = QtWidgets.QPushButton(qtawesome.icon('fa.film', color='white'), "圆饼环图")
        self.left_button_3.setObjectName('left_button')
        self.left_button_4 = QtWidgets.QPushButton(qtawesome.icon('fa.home', color='white'), "线路浏览")
        self.left_button_4.setObjectName('left_button')
        self.left_button_6 = QtWidgets.QPushButton(qtawesome.icon('fa.heart', color='white'), "地铁线路")
        self.left_button_6.setObjectName('left_button')
        self.left_button_7 = QtWidgets.QPushButton(qtawesome.icon('fa.comment', color='white'), "省市县区")
        self.left_button_7.setObjectName('left_button')
        self.left_button_5 = QtWidgets.QPushButton(qtawesome.icon('fa.download', color='white'), "区域动画")
        self.left_button_5.setObjectName('left_button')
        self.left_button_8 = QtWidgets.QPushButton(qtawesome.icon('fa.star', color='white'), "关注我们")
        self.left_button_8.setObjectName('left_button')
        self.left_button_9 = QtWidgets.QPushButton(qtawesome.icon('fa.question', color='white'), "遇到问题")
        self.left_button_9.setObjectName('left_button')

        self.left_layout.addWidget(self.left_mini, 0, 0, 1, 1)  # 最小化
        self.left_layout.addWidget(self.left_visit, 0, 1, 1, 1)  # 浏览
        self.left_layout.addWidget(self.left_close, 0, 2, 1, 1)  # 关闭
        self.left_layout.addWidget(self.left_label_1, 1, 0, 1, 3)  # 一级标题 坐标浏览
        self.left_layout.addWidget(self.left_button_1, 3, 0, 1, 3)  # 二级标题 环绕浏览
        self.left_layout.addWidget(self.left_button_2, 2, 0, 1, 3)  # 二级标题 四顾浏览

        self.left_layout.addWidget(self.left_button_10, 4, 0, 1, 3)  # 二级标题 缩时环景
        self.left_layout.addWidget(self.left_button_3, 5, 0, 1, 3)  # 二级标题 圆环饼图
        self.left_layout.addWidget(self.left_label_2, 6, 0, 1, 3)  # 一级标题 线路浏览
        self.left_layout.addWidget(self.left_button_4, 7, 0, 1, 3)  # 二级标题 线路浏览

        self.left_layout.addWidget(self.left_label_3, 8, 0, 1, 3)  # 一级标题 多变区域
        self.left_layout.addWidget(self.left_button_7, 9, 0, 1, 3)  # 二级标题 省市县区
        self.left_layout.addWidget(self.left_button_5, 10, 0, 1, 3)  # 二级标题 区域渐显

        self.left_layout.addWidget(self.left_label_4, 11, 0, 1, 3)  # 一级标题 联系与帮助
        self.left_layout.addWidget(self.left_button_8, 12, 0, 1, 3)  # 二级标题 省市县区
        self.left_layout.addWidget(self.left_button_9, 13, 0, 1, 3)  # 二级标题 省市县区

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
        self.right_bar_widget_point_radius_input_holder = QtWidgets.QLabel("建議值為高度的1.67倍 , 0 表為環景")  # 提示文字
        self.right_bar_widget_point_radius_input_holder.setObjectName("right_bar_widget_holder")

        # 環繞視點高度 Height
        self.right_bar_tour_point_altitude = QtWidgets.QLabel('视点高度  Altitude')  # 文字栏
        self.right_bar_tour_point_altitude.setObjectName("right_bar_tour_label")
        self.right_bar_widget_point_altitude_input = QtWidgets.QLineEdit()  # 输入框栏
        self.right_bar_widget_point_altitude_input.setText('702')
        self.right_bar_widget_point_altitude_input.setPlaceholderText("建議值為高度的1.5倍")
        self.right_bar_widget_point_altitude_input.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_widget_point_altitude_input_holder = QtWidgets.QLabel("建議值為高度的1.5倍")  # 提示文字
        self.right_bar_widget_point_altitude_input_holder.setObjectName("right_bar_widget_holder")

        # 環繞視野角度
        self.right_bar_tour_point_horizfov = QtWidgets.QLabel('視野角度  Horizfov')  # 文字栏
        self.right_bar_tour_point_horizfov.setObjectName("right_bar_tour_label")
        self.right_bar_widget_point_horizfov_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)  # 滑块框栏
        # self.right_bar_widget_point_horizfov_slider.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_widget_point_horizfov_slider.setMinimum(30)  # 设置最小值
        self.right_bar_widget_point_horizfov_slider.setMaximum(120)  # 设置最大值
        self.right_bar_widget_point_horizfov_slider.setSingleStep(1)  # 设置滑动步长
        self.right_bar_widget_point_horizfov_slider.setValue(60)  # 设置当前值
        self.right_bar_widget_point_horizfov_slider_value = QtWidgets.QLabel("60°")  # 提示文字

        # 環繞傾斜角度 Tilt
        self.right_bar_tour_point_tilt = QtWidgets.QLabel('傾斜角度  Tilt')
        self.right_bar_tour_point_tilt.setObjectName("right_bar_tour_label")
        self.right_bar_widget_point_tilt_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)  # 滑块框栏
        self.right_bar_widget_point_tilt_slider.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_widget_point_tilt_slider.setMinimum(0)  # 设置最小值
        self.right_bar_widget_point_tilt_slider.setMaximum(90)  # 设置最大值
        self.right_bar_widget_point_tilt_slider.setSingleStep(1)  # 设置滑动步长
        self.right_bar_widget_point_tilt_slider.setValue(60)  # 设置当前值
        self.right_bar_widget_point_tilt_slider_value = QtWidgets.QLabel("60°")  # 提示文字
        self.right_bar_widget_point_tilt_slider_holder = QtWidgets.QLabel("0°為正射，90°為水平")  # 提示文字
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

        # ======================右侧点击-环绕浏览====================================================
        # right_tour_point_ring_around
        self.right_bar_point_around_widget = QtWidgets.QWidget()  # 右侧顶部搜索框部件
        self.right_bar_point_around_layout = QtWidgets.QGridLayout()  # 右侧顶部搜索框网格布局
        self.right_bar_point_around_widget.setLayout(self.right_bar_point_around_layout)

        self.right_bar_tour_point_around = QtWidgets.QPushButton("环绕浏览")
        self.right_bar_tour_point_around.setObjectName("right_lable_title")

        # 名称输入框
        self.right_bar_tour_point_around_kmlname = QtWidgets.QLabel('名称  Kmlname')
        self.right_bar_tour_point_around_kmlname.setObjectName("right_bar_tour_label")
        self.right_bar_widget_point_around_kmlname_input = QtWidgets.QLineEdit()
        self.right_bar_widget_point_around_kmlname_input.setText('上海东方明珠')
        self.right_bar_widget_point_around_kmlname_input.setPlaceholderText("输入要保存的文件名")
        self.right_bar_widget_point_around_kmlname_input.setObjectName('right_bar_widget_qlinedit_input')

        # 经度输入框
        self.right_bar_tour_point_around_longitude = QtWidgets.QLabel('经度  Longitude')  # 文字栏
        self.right_bar_tour_point_around_longitude.setObjectName("right_bar_tour_label")
        self.right_bar_widget_point_around_longitude_input = QtWidgets.QLineEdit()  # 输入框栏
        self.right_bar_widget_point_around_longitude_input.setText('121.4952627807584')
        # self.right_bar_widget_point_around_longitude_input.setPlaceholderText("输入经度 十进制度小数")
        self.right_bar_widget_point_around_longitude_input.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_widget_point_around_longitude_input_holder = QtWidgets.QLabel("输入经度 十进制度小数")  # 提示栏
        self.right_bar_widget_point_around_longitude_input_holder.setObjectName("right_bar_widget_holder")

        # 纬度输入框
        self.right_bar_tour_point_around_latitude = QtWidgets.QLabel('纬度  Latitude')  # 文字栏
        self.right_bar_tour_point_around_latitude.setObjectName("right_bar_tour_label")
        self.right_bar_widget_point_around_latitude_input = QtWidgets.QLineEdit()  # 输入框栏
        self.right_bar_widget_point_around_latitude_input.setText('31.24188370156092')
        # self.right_bar_widget_point_around_latitude_input.setPlaceholderText("输入纬度 十进制度小数")
        self.right_bar_widget_point_around_latitude_input.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_widget_point_around_latitude_input_holder = QtWidgets.QLabel("输入纬度 十进制度小数")  # 提示栏
        self.right_bar_widget_point_around_latitude_input_holder.setObjectName("right_bar_widget_holder")

        # 高度输入框
        self.right_bar_tour_point_around_height = QtWidgets.QLabel('高度  Height')  # 文字栏
        self.right_bar_tour_point_around_height.setObjectName("right_bar_tour_label")
        self.right_bar_widget_point_around_height_input = QtWidgets.QLineEdit()  # 输入框栏
        self.right_bar_widget_point_around_height_input.setText('468')
        # self.right_bar_widget_point_around_height_input.setPlaceholderText("建筑、山体高度")
        self.right_bar_widget_point_around_height_input.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_widget_point_around_height_input_holder = QtWidgets.QLabel("建筑、山体高度")  # 提示栏
        self.right_bar_widget_point_around_height_input_holder.setObjectName("right_bar_widget_holder")

        # 环绕半径输入框
        self.right_bar_tour_point_around_radius = QtWidgets.QLabel('环绕半径  Radius')  # 文字栏
        self.right_bar_tour_point_around_radius.setObjectName("right_bar_tour_label")
        self.right_bar_widget_point_around_radius_input = QtWidgets.QLineEdit()  # 输入框栏
        self.right_bar_widget_point_around_radius_input.setText('781')
        # self.right_bar_widget_point_around_radius_input.setPlaceholderText("环绕半径  Radius")
        self.right_bar_widget_point_around_radius_input.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_widget_point_around_radius_input_holder = QtWidgets.QLabel("建議值為高度的1.67倍 , 0 表為環景")  # 提示文字
        self.right_bar_widget_point_around_radius_input_holder.setObjectName("right_bar_widget_holder")

        # 環繞視點高度 Height
        self.right_bar_tour_point_around_altitude = QtWidgets.QLabel('视点高度  Altitude')  # 文字栏
        self.right_bar_tour_point_around_altitude.setObjectName("right_bar_tour_label")
        self.right_bar_widget_point_around_altitude_input = QtWidgets.QLineEdit()  # 输入框栏
        self.right_bar_widget_point_around_altitude_input.setText('702')
        self.right_bar_widget_point_around_altitude_input.setPlaceholderText("建議值為高度的1.5倍")
        self.right_bar_widget_point_around_altitude_input.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_widget_point_around_altitude_input_holder = QtWidgets.QLabel("建議值為高度的1.5倍")  # 提示文字
        self.right_bar_widget_point_around_altitude_input_holder.setObjectName("right_bar_widget_holder")

        # 環繞視野角度
        self.right_bar_tour_point_around_horizfov = QtWidgets.QLabel('視野角度  Horizfov')  # 文字栏
        self.right_bar_tour_point_around_horizfov.setObjectName("right_bar_tour_label")
        self.right_bar_widget_point_around_horizfov_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)  # 滑块框栏
        self.right_bar_widget_point_around_horizfov_slider.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_widget_point_around_horizfov_slider.setMinimum(30)  # 设置最小值
        self.right_bar_widget_point_around_horizfov_slider.setMaximum(120)  # 设置最大值
        self.right_bar_widget_point_around_horizfov_slider.setSingleStep(1)  # 设置滑动步长
        self.right_bar_widget_point_around_horizfov_slider.setValue(60)  # 设置当前值
        self.right_bar_widget_point_around_horizfov_slider_value = QtWidgets.QLabel("60°")  # 提示文字

        # 環繞傾斜角度 Tilt
        self.right_bar_tour_point_around_tilt = QtWidgets.QLabel('傾斜角度  Tilt')
        self.right_bar_tour_point_around_tilt.setObjectName("right_bar_tour_label")
        self.right_bar_widget_point_around_tilt_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)  # 滑块框栏
        self.right_bar_widget_point_around_tilt_slider.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_widget_point_around_tilt_slider.setMinimum(0)  # 设置最小值
        self.right_bar_widget_point_around_tilt_slider.setMaximum(90)  # 设置最大值
        self.right_bar_widget_point_around_tilt_slider.setSingleStep(1)  # 设置滑动步长
        self.right_bar_widget_point_around_tilt_slider.setValue(60)  # 设置当前值
        self.right_bar_widget_point_around_tilt_slider_value = QtWidgets.QLabel("60°")  # 提示文字
        self.right_bar_widget_point_around_tilt_slider_holder = QtWidgets.QLabel("0°為正射，90°為水平")  # 提示文字
        self.right_bar_widget_point_around_tilt_slider_holder.setObjectName("right_bar_widget_holder")

        # 環繞 啟始方向 Ring Around Start Direction: -180° <--> 180°
        self.right_bar_tour_point_around_heading = QtWidgets.QLabel('开启方向')
        self.right_bar_tour_point_around_heading.setObjectName("right_bar_tour_label")
        self.right_bar_widget_point_around_heading_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)  # 滑块框栏
        self.right_bar_widget_point_around_heading_slider.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_widget_point_around_heading_slider.setMinimum(-180)  # 设置最小值
        self.right_bar_widget_point_around_heading_slider.setMaximum(180)  # 设置最大值
        self.right_bar_widget_point_around_heading_slider.setSingleStep(1)  # 设置滑动步长
        self.right_bar_widget_point_around_heading_slider.setValue(0)  # 设置当前值
        self.right_bar_widget_point_around_heading_slider_value = QtWidgets.QLabel("0°")  # 提示文字

        # 環繞 环绕时间
        self.right_bar_tour_point_around_tour_time = QtWidgets.QLabel('环绕时间')
        self.right_bar_tour_point_around_tour_time.setObjectName("right_bar_tour_label")
        self.right_bar_widget_point_around_tour_time_input = QtWidgets.QLineEdit()
        # self.right_bar_widget_point_tour_time_input.setPlaceholderText("建议20 ~ 30秒")
        self.right_bar_widget_point_around_tour_time_input.setText('30')
        self.right_bar_widget_point_around_tour_time_input.setObjectName('right_bar_widget_qlinedit_input')

        # 環繞 方向 clockwise:
        self.right_bar_tour_point_around_clock = QtWidgets.QLabel('环绕方向')
        self.right_bar_tour_point_around_clock.setObjectName("right_bar_tour_label")
        self.right_bar_tour_point_around_clock_wise_group_button = QtWidgets.QButtonGroup()  # 按钮分组
        self.right_bar_tour_point_around_clock_wise_button = QtWidgets.QRadioButton("顺时针")
        self.right_bar_tour_point_around_clock_wise_button.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_tour_point_around_clock_wise_button.setChecked(True)
        self.right_bar_tour_point_around_counter_clock_wise_button = QtWidgets.QRadioButton("逆时针")
        self.right_bar_tour_point_around_counter_clock_wise_button.setObjectName(
            'right_bar_widget_qlinedit_input')
        self.right_bar_tour_point_around_clock_wise_group_button.addButton(
            self.right_bar_tour_point_around_clock_wise_button, 1)  # 设置ID为1
        self.right_bar_tour_point_around_clock_wise_group_button.addButton(
            self.right_bar_tour_point_around_counter_clock_wise_button, 2)

        self.right_bar_widget_point_around_button_download = QtWidgets.QPushButton()
        self.right_bar_widget_point_around_button_download.setText("确定")
        self.right_bar_widget_point_around_button_download.setObjectName('right_bar_tour_button_download')

        self.right_bar_point_around_layout.addWidget(self.right_bar_tour_point_around, 0, 0, 1,
                                                     1)  # (跨行的控件，起始行，起始列，跨越的行数，跨越列数)
        self.right_bar_point_around_layout.addWidget(self.right_bar_tour_point_around_kmlname, 0, 0, 4, 1)
        self.right_bar_point_around_layout.addWidget(self.right_bar_widget_point_around_kmlname_input, 0, 1, 4, 3)
        self.right_bar_point_around_layout.addWidget(self.right_bar_tour_point_around_longitude, 1, 0, 4, 1)  # 经度 文字
        self.right_bar_point_around_layout.addWidget(self.right_bar_widget_point_around_longitude_input, 1, 1, 4,
                                                     3)  # 经度 输入框
        self.right_bar_point_around_layout.addWidget(self.right_bar_widget_point_around_longitude_input_holder, 1, 4, 4,
                                                     2)  # 经度 提示文字
        self.right_bar_point_around_layout.addWidget(self.right_bar_tour_point_around_latitude, 2, 0, 4, 1)  # 纬度 文字
        self.right_bar_point_around_layout.addWidget(self.right_bar_widget_point_around_latitude_input, 2, 1, 4,
                                                     3)  # 纬度 输入框
        self.right_bar_point_around_layout.addWidget(self.right_bar_widget_point_around_latitude_input_holder, 2, 4, 4,
                                                     3)  # 纬度 提示文字
        self.right_bar_point_around_layout.addWidget(self.right_bar_tour_point_around_height, 3, 0, 4, 1)  # 高度 文字
        self.right_bar_point_around_layout.addWidget(self.right_bar_widget_point_around_height_input, 3, 1, 4,
                                                     3)  # 高度 输入框
        self.right_bar_point_around_layout.addWidget(self.right_bar_widget_point_around_height_input_holder, 3, 4, 4,
                                                     3)  # 高度 提示文字
        self.right_bar_point_around_layout.addWidget(self.right_bar_tour_point_around_radius, 4, 0, 4, 1)  # 环绕半径 文字
        self.right_bar_point_around_layout.addWidget(self.right_bar_widget_point_around_radius_input, 4, 1, 4,
                                                     3)  # 环绕半径 输入框
        self.right_bar_point_around_layout.addWidget(self.right_bar_widget_point_around_radius_input_holder, 4, 4, 4,
                                                     3)  # 环绕半径 提示文字
        self.right_bar_point_around_layout.addWidget(self.right_bar_tour_point_around_altitude, 5, 0, 4, 1)  # 视点高度 文字
        self.right_bar_point_around_layout.addWidget(self.right_bar_widget_point_around_altitude_input, 5, 1, 4,
                                                     3)  # 视点高度 输入框
        self.right_bar_point_around_layout.addWidget(self.right_bar_widget_point_around_altitude_input_holder, 5, 4, 4,
                                                     3)  # 视点高度 提示文字
        self.right_bar_point_around_layout.addWidget(self.right_bar_tour_point_around_horizfov, 6, 0, 4, 1)  # 視野角度 文字
        self.right_bar_point_around_layout.addWidget(self.right_bar_widget_point_around_horizfov_slider, 6, 1, 4,
                                                     3)  # 視野角度 滑块
        self.right_bar_point_around_layout.addWidget(self.right_bar_widget_point_around_horizfov_slider_value, 6, 4, 4,
                                                     1)  # 視野角度 当前值
        self.right_bar_point_around_layout.addWidget(self.right_bar_tour_point_around_tilt, 7, 0, 4, 1)  # 傾斜角度 文字
        self.right_bar_point_around_layout.addWidget(self.right_bar_widget_point_around_tilt_slider, 7, 1, 4,
                                                     3)  # 傾斜角度 滑块
        self.right_bar_point_around_layout.addWidget(self.right_bar_widget_point_around_tilt_slider_value, 7, 4, 4,
                                                     1)  # 傾斜角度 当前值
        self.right_bar_point_around_layout.addWidget(self.right_bar_widget_point_around_tilt_slider_holder, 7, 5, 4,
                                                     1)  # 傾斜角度 提示文字
        self.right_bar_point_around_layout.addWidget(self.right_bar_tour_point_around_heading, 8, 0, 4, 1)  # 啟始方向 文字
        self.right_bar_point_around_layout.addWidget(self.right_bar_widget_point_around_heading_slider, 8, 1, 4,
                                                     3)  # 啟始方向 滑块
        self.right_bar_point_around_layout.addWidget(self.right_bar_widget_point_around_heading_slider_value, 8, 4, 4,
                                                     1)  # 啟始方向 当前值
        self.right_bar_point_around_layout.addWidget(self.right_bar_tour_point_around_tour_time, 9, 0, 4, 1)  # 環繞方向 文字
        self.right_bar_point_around_layout.addWidget(self.right_bar_widget_point_around_tour_time_input, 9, 1, 4,
                                                     3)  # 環繞方向 当前值

        self.right_bar_point_around_layout.addWidget(self.right_bar_tour_point_around_clock, 10, 0, 4, 1)
        self.right_bar_point_around_layout.addWidget(self.right_bar_tour_point_around_clock_wise_button, 10, 1, 4, 3)
        self.right_bar_point_around_layout.addWidget(self.right_bar_tour_point_around_counter_clock_wise_button, 10, 2,
                                                     4, 3)
        self.right_bar_point_around_layout.addWidget(self.right_bar_widget_point_around_button_download, 12, 2, 3,
                                                     2)  # (跨行的控件，起始行，起始列，跨越的行数，跨越列数)

        # ======================右侧点击-线路浏览====================================================
        self.right_bar_line_widget = QtWidgets.QWidget()  # 右侧顶部搜索框部件
        self.right_bar_line_layout = QtWidgets.QGridLayout()  # 右侧顶部搜索框网格布局
        self.right_bar_line_widget.setLayout(self.right_bar_line_layout)

        self.right_bar_tour_line = QtWidgets.QPushButton("线路浏览")
        self.right_bar_tour_line.setObjectName("right_lable_title")

        # 线路浏览 线路浏览  名称输入框
        self.right_bar_tour_line_kmlname = QtWidgets.QLabel('名称  Kmlname')
        self.right_bar_tour_line_kmlname.setObjectName("right_bar_tour_label")
        self.right_bar_widget_line_kmlname_input = QtWidgets.QLineEdit()
        self.right_bar_widget_line_kmlname_input.setPlaceholderText("输入要保存的文件名")
        self.right_bar_widget_line_kmlname_input.setObjectName('right_bar_widget_qlinedit_input')

        # 线路浏览 线路浏览  浏览样式
        self.right_bar_tour_line_tour_type = QtWidgets.QLabel('浏览方式')
        self.right_bar_tour_line_tour_type.setObjectName("right_bar_tour_label")
        self.right_bar_widget_line_tour_type_input = QtWidgets.QComboBox()
        self.right_bar_widget_line_tour_type_input.addItems(["生长路线-固定视角", "生长路线-环绕视角", "生长路线-跟随视角"])   #  "节段路线-环绕视角", "节段路线-跟随视角"
        self.right_bar_widget_line_tour_type_input.setObjectName('right_bar_widget_combobox_input')

        # 线路浏览 线路浏览 环绕时间
        self.right_bar_tour_line_tour_time = QtWidgets.QLabel('移动时间')
        self.right_bar_tour_line_tour_time.setObjectName("right_bar_tour_label")
        self.right_bar_widget_line_tour_time_input = QtWidgets.QLineEdit()
        self.right_bar_widget_line_tour_time_input.setText('30')
        self.right_bar_widget_line_tour_time_input.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_widget_line_tour_time_input_holder = QtWidgets.QLabel("")  # 提示文字
        self.right_bar_widget_line_tour_time_input_holder.setObjectName("right_bar_widget_holder")

        # 线路浏览 图片模型
        self.right_bar_tour_line_flag = QtWidgets.QLabel('图片模型')
        self.right_bar_tour_line_flag.setObjectName("right_bar_tour_label")
        self.right_bar_tour_line_flag_group_button = QtWidgets.QButtonGroup()  # 按钮分组
        self.right_bar_tour_line_flag_yes_button = QtWidgets.QRadioButton("模型")
        self.right_bar_tour_line_flag_yes_button.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_tour_line_flag_yes_button.setChecked(True)
        self.right_bar_tour_line_flag_no_button = QtWidgets.QRadioButton('图片')
        self.right_bar_tour_line_flag_no_button.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_tour_line_flag_group_button.addButton(self.right_bar_tour_line_flag_yes_button, 1)  # 设置ID为1
        self.right_bar_tour_line_flag_group_button.addButton(self.right_bar_tour_line_flag_no_button, 2)
        # 线路浏览 线路浏览 线路文件
        self.right_bar_tour_line_file = QtWidgets.QPushButton('上传文件')
        # self.right_bar_tour_line_file.setObjectName("right_bar_tour_file_button")
        self.right_bar_tour_line_file_holder = QtWidgets.QLabel('请选择上传的文件')
        self.right_bar_tour_line_file_holder.setObjectName("right_bar_widget_holder")
        self.right_bar_tour_line_filepath_coords = None  # 下载实际路径页面不展示

        # 线路浏览 线路浏览 下载
        self.right_bar_tour_line_file_button_download = QtWidgets.QPushButton()
        self.right_bar_tour_line_file_button_download.setText("确定")
        self.right_bar_tour_line_file_button_download.setObjectName('right_bar_tour_button_download')
        self.right_bar_widget_line_file_placeholder = QtWidgets.QLabel("")  # 占位符

        self.right_bar_line_layout.addWidget(self.right_bar_tour_line, 0, 0, 1, 1)  # (跨行的控件，起始行，起始列，跨越的行数，跨越列数)
        self.right_bar_line_layout.addWidget(self.right_bar_tour_line_kmlname, 0, 0, 4, 1)  # 线路浏览 文件名 文字
        self.right_bar_line_layout.addWidget(self.right_bar_widget_line_kmlname_input, 0, 1, 4, 3)  # 线路浏览 文件名 输入框
        self.right_bar_line_layout.addWidget(self.right_bar_tour_line_tour_type, 1, 0, 4, 1)  # 线路浏览 浏览样式 文字
        self.right_bar_line_layout.addWidget(self.right_bar_widget_line_tour_type_input, 1, 1, 4, 3)  # 线路浏览 浏览样式 输入框
        self.right_bar_line_layout.addWidget(self.right_bar_tour_line_flag, 2, 0, 4, 1)             #    图片模型
        self.right_bar_line_layout.addWidget(self.right_bar_tour_line_flag_no_button, 2, 1, 4, 3)   #    模型
        self.right_bar_line_layout.addWidget(self.right_bar_tour_line_flag_yes_button, 2, 2, 4, 3)  #    图片
        self.right_bar_line_layout.addWidget(self.right_bar_tour_line_tour_time, 3, 0, 4, 1)  # 线路浏览 时间 文字
        self.right_bar_line_layout.addWidget(self.right_bar_widget_line_tour_time_input, 3, 1, 4, 3)  # 线路浏览 时间 输入框
        self.right_bar_line_layout.addWidget(self.right_bar_widget_line_tour_time_input_holder, 3, 4, 4, 3)  # 线路浏览 时间 提示文字

        self.right_bar_line_layout.addWidget(self.right_bar_tour_line_file, 4, 1, 4, 1)  # 线路浏览 上传文件 输入框
        self.right_bar_line_layout.addWidget(self.right_bar_tour_line_file_holder, 4, 2, 4, 2)  # 线路浏览 上传文件 提示文字
        self.right_bar_line_layout.addWidget(self.right_bar_tour_line_file_button_download, 5, 1, 4, 3)  # 线路浏览 上传文件 下载按钮
        self.right_bar_line_layout.addWidget(self.right_bar_widget_line_file_placeholder, 10, 2, 4, 3)  # 线路浏览 上传文件 占位符

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


        self.right_bar_point_day24_layout.addWidget(self.right_bar_tour_point_day24, 0, 0, 1, 1)  # (跨行的控件，起始行，起始列，跨越的行数，跨越列数)
        self.right_bar_point_day24_layout.addWidget(self.right_bar_tour_point_day24_kmlname, 0, 0, 4, 1)
        self.right_bar_point_day24_layout.addWidget(self.right_bar_widget_point_day24_kmlname_input, 0, 1, 4, 3)
        self.right_bar_point_day24_layout.addWidget(self.right_bar_tour_point_day24_longitude, 1, 0, 4, 1)  # 圆环饼图 经度 文字
        self.right_bar_point_day24_layout.addWidget(self.right_bar_widget_point_day24_longitude_input, 1, 1, 4, 3)  # 圆环饼图 经度 输入框
        self.right_bar_point_day24_layout.addWidget(self.right_bar_widget_point_day24_longitude_input_holder, 1, 4, 4, 2)  # 圆环饼图 经度 提示文字
        self.right_bar_point_day24_layout.addWidget(self.right_bar_tour_point_day24_latitude, 2, 0, 4, 1)  # 圆环饼图 纬度 文字
        self.right_bar_point_day24_layout.addWidget(self.right_bar_widget_point_day24_latitude_input, 2, 1, 4, 3)  # 圆环饼图 纬度 输入框
        self.right_bar_point_day24_layout.addWidget(self.right_bar_widget_point_day24_latitude_input_holder, 2, 4, 4, 3)  # 圆环饼图 纬度 提示文字

        self.right_bar_point_day24_layout.addWidget(self.right_bar_tour_point_day24_altitude, 3, 0, 4, 1)  # 圆环饼图 纬度 文字
        self.right_bar_point_day24_layout.addWidget(self.right_bar_widget_point_day24_altitude_input, 3, 1, 4,3)  # 圆环饼图 环绕宽度 输入框
        self.right_bar_point_day24_layout.addWidget(self.right_bar_widget_point_day24_altitude_input_holder, 3, 4, 4, 3)  # 圆环饼图 环绕宽度 当前值

        self.right_bar_point_day24_layout.addWidget(self.right_bar_widget_point_day24_button_download, 4, 1, 4, 2)  # (跨行的控件，起始行，起始列，跨越的行数，跨越列数)
        self.right_bar_point_day24_layout.addWidget(self.right_bar_widget_point_day24_placeholder, 18, 2, 4, 2)  # 圆环饼图 环绕宽度 占位符

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

        # ======================右侧点击-区域渐显====================================================
        self.right_bar_polygon_show_widget = QtWidgets.QWidget()  # 右侧顶部搜索框部件
        self.right_bar_polygon_show_layout = QtWidgets.QGridLayout()  # 右侧顶部搜索框网格布局
        self.right_bar_polygon_show_widget.setLayout(self.right_bar_polygon_show_layout)

        self.right_bar_tour_show_polygon = QtWidgets.QPushButton("区域动画")
        self.right_bar_tour_show_polygon.setObjectName("right_lable_title")

        # 名称输入框
        self.right_bar_tour_show_polygon_kmlname = QtWidgets.QLabel('名称  Kmlname')
        self.right_bar_tour_show_polygon_kmlname.setObjectName("right_bar_tour_label")
        self.right_bar_widget_show_polygon_kmlname_input = QtWidgets.QLineEdit()
        self.right_bar_widget_show_polygon_kmlname_input.setText('区域动画')
        self.right_bar_widget_show_polygon_kmlname_input.setPlaceholderText("输入要保存的文件名")
        self.right_bar_widget_show_polygon_kmlname_input.setObjectName('right_bar_widget_qlinedit_input')

        # 区域渐显 动画方式 - 区域动画&形状变化动画
        self.right_bar_tour_show_polygon_type = QtWidgets.QLabel('动画方式')
        self.right_bar_tour_show_polygon_type.setObjectName("right_bar_tour_label")
        self.right_bar_tour_show_polygon_type_group_button = QtWidgets.QButtonGroup()  # 按钮分组
        self.right_bar_tour_show_polygon_type_yes_button = QtWidgets.QRadioButton("区域渐显")
        self.right_bar_tour_show_polygon_type_yes_button.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_tour_show_polygon_type_yes_button.setChecked(True)
        self.right_bar_tour_show_polygon_type_no_button = QtWidgets.QRadioButton("形状变化")
        self.right_bar_tour_show_polygon_type_no_button.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_tour_show_polygon_type_group_button.addButton(self.right_bar_tour_show_polygon_type_yes_button, 1)  # 设置ID为1
        self.right_bar_tour_show_polygon_type_group_button.addButton(self.right_bar_tour_show_polygon_type_no_button, 0)

        self.right_bar_tour_show_polygon_time = QtWidgets.QLabel('时间')
        self.right_bar_tour_show_polygon_time.setObjectName("right_bar_tour_label")
        self.right_bar_widget_show_polygon_time_input = QtWidgets.QLineEdit()
        self.right_bar_widget_show_polygon_time_input.setText('3')
        self.right_bar_widget_show_polygon_time_input.setPlaceholderText("单个polygon时间")
        self.right_bar_widget_show_polygon_time_input.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_widget_show_polygon_time_input_holder = QtWidgets.QLabel("单个polygon时间")  # 提示栏
        self.right_bar_widget_show_polygon_time_input_holder.setObjectName("right_bar_widget_holder")

        self.right_bar_tour_show_polygon_color = QtWidgets.QLabel('颜色&透明度')                # transparent
        self.right_bar_tour_show_polygon_color.setObjectName("right_bar_tour_label")
        self.right_bar_tour_show_polygon_color_input = QtWidgets.QPushButton("选择颜色")
        self.right_bar_tour_show_polygon_color_transparent_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)  # 滑块框栏
        self.right_bar_tour_show_polygon_color_transparent_slider.setMinimum(0)  # 设置最小值
        self.right_bar_tour_show_polygon_color_transparent_slider.setMaximum(255)  # 设置最大值
        self.right_bar_tour_show_polygon_color_transparent_slider.setSingleStep(1)  # 设置滑动步长
        self.right_bar_tour_show_polygon_color_transparent_slider.setValue(150)
        self.right_bar_tour_show_polygon_color_transparent_slider_holder_value = QtWidgets.QLabel("150")  # 提示文字
        self.right_bar_tour_show_polygon_color_name = ''  # 颜色

        # 线路浏览 线路浏览 线路文件
        self.right_bar_tour_show_polygon_file = QtWidgets.QPushButton('上传文件')
        self.right_bar_tour_show_polygon_file.setObjectName("right_bar_tour_line_tour_file_button")
        self.right_bar_tour_show_polygon_file_holder = QtWidgets.QLabel('请选择上传的文件')
        self.right_bar_tour_show_polygon_file_holder.setObjectName("right_bar_widget_holder")
        self.right_bar_tour_show_polygon_filepath_coords = None  # 下载实际路径页面不展示


        # 线路浏览 线路浏览 下载
        self.right_bar_tour_show_polygon_file_button_download = QtWidgets.QPushButton()
        self.right_bar_tour_show_polygon_file_button_download.setText("确定")
        self.right_bar_tour_show_polygon_file_button_download.setObjectName('right_bar_tour_button_download')
        self.right_bar_widget_show_polygon_file_placeholder = QtWidgets.QLabel("")  # 占位符

        self.right_bar_polygon_show_layout.addWidget(self.right_bar_tour_show_polygon, 0, 0, 1, 1)  # 单独水平线
        self.right_bar_polygon_show_layout.addWidget(self.right_bar_tour_show_polygon_kmlname, 1, 0, 1, 1)
        self.right_bar_polygon_show_layout.addWidget(self.right_bar_widget_show_polygon_kmlname_input, 1, 1, 1, 5)

        self.right_bar_polygon_show_layout.addWidget(self.right_bar_tour_show_polygon_type, 2, 0, 1, 1)
        self.right_bar_polygon_show_layout.addWidget(self.right_bar_tour_show_polygon_type_yes_button, 2, 1, 1, 2)
        self.right_bar_polygon_show_layout.addWidget(self.right_bar_tour_show_polygon_type_no_button, 2, 3, 1, 1)

        self.right_bar_polygon_show_layout.addWidget(self.right_bar_tour_show_polygon_color, 3, 0, 1, 1)
        self.right_bar_polygon_show_layout.addWidget(self.right_bar_tour_show_polygon_color_input, 3, 1, 1, 1)
        self.right_bar_polygon_show_layout.addWidget(self.right_bar_tour_show_polygon_color_transparent_slider, 3, 2, 1, 4)
        self.right_bar_polygon_show_layout.addWidget(self.right_bar_tour_show_polygon_color_transparent_slider_holder_value,3, 6, 1, 6)

        self.right_bar_polygon_show_layout.addWidget(self.right_bar_tour_show_polygon_time, 4, 0, 1, 1)
        self.right_bar_polygon_show_layout.addWidget(self.right_bar_widget_show_polygon_time_input, 4, 1, 1, 2)
        self.right_bar_polygon_show_layout.addWidget(self.right_bar_widget_show_polygon_time_input_holder, 4, 3, 1, 6)

        self.right_bar_polygon_show_layout.addWidget(self.right_bar_tour_show_polygon_file, 5, 1, 1, 2)  # 修改列索引为0
        self.right_bar_polygon_show_layout.addWidget(self.right_bar_tour_show_polygon_file_holder, 5, 3, 1, 2)  # 修改列索引为1，跨越列数为2
        self.right_bar_polygon_show_layout.addWidget(self.right_bar_tour_show_polygon_file_button_download, 6, 1, 1, 2)  # 修改列索引为3

        # ======================右侧点击-省市县====================================================
        self.right_bar_polygon_widget = QtWidgets.QWidget()  # 右侧顶部搜索框部件
        self.right_bar_polygon_layout = QtWidgets.QGridLayout()  # 右侧顶部搜索框网格布局
        self.right_bar_polygon_widget.setLayout(self.right_bar_polygon_layout)

        self.right_bar_tour_polygon = QtWidgets.QPushButton("省市县区")
        self.right_bar_tour_polygon.setObjectName("right_lable_title")

        #省市区 选择国家
        self.right_bar_tour_polygon_country = QtWidgets.QLabel('CHINA')
        self.right_bar_tour_polygon_country.setObjectName("right_bar_tour_label")
        self.right_bar_widget_polygon_country_input = QtWidgets.QComboBox()
        self.right_bar_widget_polygon_country_input.addItems(['中华人民共和国'])
        self.right_bar_widget_polygon_country_input.setObjectName('right_bar_widget_combobox_enabled_input')
        # self.right_bar_widget_polygon_country_input.setEnabled(False)  # 按钮可点击

        #省市区 选择省份
        self.right_bar_tour_polygon_province = QtWidgets.QLabel('选择省份')
        self.right_bar_tour_polygon_province.setObjectName("right_bar_tour_label")
        self.right_bar_widget_polygon_province_input = QtWidgets.QComboBox()
        self.right_bar_widget_polygon_province_input.addItem("请选择")

        provinces = LuckyAreas.select(LuckyAreas.adcode, LuckyAreas.area_name).where(LuckyAreas.level=='province')
        for province in provinces:
            self.right_bar_widget_polygon_province_input.addItem(province.area_name)

        self.right_bar_widget_polygon_province_input.setObjectName('right_bar_widget_combobox_input')
        self.right_bar_widget_polygon_province_input_holder = QtWidgets.QLabel("空表示所有")  # 提示栏
        self.right_bar_widget_polygon_province_input_holder.setObjectName("right_bar_widget_holder")
        # 省市区 选择城市
        self.right_bar_tour_polygon_city = QtWidgets.QLabel('选择市区')
        self.right_bar_tour_polygon_city.setObjectName("right_bar_tour_label")
        self.right_bar_widget_polygon_city_input = QtWidgets.QComboBox()
        self.right_bar_widget_polygon_city_input.addItem("请选择")
        self.right_bar_widget_polygon_city_input.setObjectName('right_bar_widget_combobox_input')
        # 省市区 县区
        self.right_bar_tour_polygon_town = QtWidgets.QLabel('选择区县')
        self.right_bar_tour_polygon_town.setObjectName("right_bar_tour_label")
        self.right_bar_widget_polygon_town_input = QtWidgets.QComboBox()
        self.right_bar_widget_polygon_town_input.addItem("请选择")
        self.right_bar_widget_polygon_town_input.setObjectName('right_bar_widget_combobox_input')
        # self.right_bar_widget_polygon_town_placeholder = QtWidgets.QLabel("")  # 占位符

        # 省市区 是否子区域
        self.right_bar_tour_polygon_children = QtWidgets.QLabel('子区域')
        self.right_bar_tour_polygon_children.setObjectName("right_bar_tour_label")
        self.right_bar_tour_polygon_children_group_button = QtWidgets.QButtonGroup()  # 按钮分组
        self.right_bar_tour_polygon_children_yes_button = QtWidgets.QRadioButton("包含")
        self.right_bar_tour_polygon_children_yes_button.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_tour_polygon_children_yes_button.setChecked(True)
        self.right_bar_tour_polygon_children_no_button = QtWidgets.QRadioButton("不包含")
        self.right_bar_tour_polygon_children_no_button.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_tour_polygon_children_group_button.addButton(self.right_bar_tour_polygon_children_yes_button, 1)  # 设置ID为1
        self.right_bar_tour_polygon_children_group_button.addButton(self.right_bar_tour_polygon_children_no_button, 0)

        # 省市区 是否子区域
        self.right_bar_tour_polygon_color = QtWidgets.QLabel('颜色填充')
        self.right_bar_tour_polygon_color.setObjectName("right_bar_tour_label")
        self.right_bar_tour_polygon_color_group_button = QtWidgets.QButtonGroup()  # 按钮分组
        self.right_bar_tour_polygon_color_yes_button = QtWidgets.QRadioButton("包含")
        self.right_bar_tour_polygon_color_yes_button.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_tour_polygon_color_yes_button.setChecked(True)
        self.right_bar_tour_polygon_color_no_button = QtWidgets.QRadioButton("不包含")
        self.right_bar_tour_polygon_color_no_button.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_tour_polygon_color_group_button.addButton(self.right_bar_tour_polygon_color_yes_button, 1)  # 设置ID为1
        self.right_bar_tour_polygon_color_group_button.addButton(self.right_bar_tour_polygon_color_no_button, 0)

        # 坐标浏览 圆环饼图 下载
        self.right_bar_widget_polygon_button_download = QtWidgets.QPushButton()
        self.right_bar_widget_polygon_button_download.setText("确定")
        self.right_bar_widget_polygon_button_download.setObjectName('right_bar_tour_button_download')
        self.right_bar_widget_polygon_placeholder = QtWidgets.QLabel("")  # 占位符

        self.right_bar_polygon_layout.addWidget(self.right_bar_tour_polygon, 0, 0, 1, 1)  # (跨行的控件，起始行，起始列，跨越的行数，跨越列数)
        self.right_bar_polygon_layout.addWidget(self.right_bar_tour_polygon_country, 0, 0, 4, 1)             #    省份   文字
        self.right_bar_polygon_layout.addWidget(self.right_bar_widget_polygon_country_input,  0, 1, 4, 3)    #    省份   选择框

        self.right_bar_polygon_layout.addWidget(self.right_bar_tour_polygon_province, 1, 0, 4, 1)             #    省份   文字
        self.right_bar_polygon_layout.addWidget(self.right_bar_widget_polygon_province_input,  1, 1, 4, 3)    #    省份   选择框
        self.right_bar_polygon_layout.addWidget(self.right_bar_widget_polygon_province_input_holder, 1, 4, 4, 2)   # 省份 提示文字
        self.right_bar_polygon_layout.addWidget(self.right_bar_tour_polygon_city, 2, 0, 4, 1)                 #    城市   文字
        self.right_bar_polygon_layout.addWidget(self.right_bar_widget_polygon_city_input,  2, 1, 4, 3)        #    城市   选择框
        self.right_bar_polygon_layout.addWidget(self.right_bar_tour_polygon_town,  3, 0, 4, 1)                #    县区   文字
        self.right_bar_polygon_layout.addWidget(self.right_bar_widget_polygon_town_input,  3, 1, 4, 3)        #    县区   选择框
        self.right_bar_polygon_layout.addWidget(self.right_bar_tour_polygon_children, 4, 0, 4, 1)             #    是否包含子区域
        self.right_bar_polygon_layout.addWidget(self.right_bar_tour_polygon_children_yes_button, 4, 1, 4, 3)  #    包含子区域
        self.right_bar_polygon_layout.addWidget(self.right_bar_tour_polygon_children_no_button, 4, 2, 4, 3)   #    不包含子区域
        self.right_bar_polygon_layout.addWidget(self.right_bar_tour_polygon_color, 5, 0, 4, 1)                #    是否填充颜色
        self.right_bar_polygon_layout.addWidget(self.right_bar_tour_polygon_color_yes_button, 5, 1, 4, 3)     #    是填充颜色
        self.right_bar_polygon_layout.addWidget(self.right_bar_tour_polygon_color_no_button, 5, 2, 4, 3)      #    否填充颜色
        self.right_bar_polygon_layout.addWidget(self.right_bar_widget_polygon_button_download, 6, 1, 4, 2)    #  下载
        self.right_bar_polygon_layout.addWidget(self.right_bar_widget_polygon_placeholder, 18, 2, 4,   2)     #  占位符

        # ======================右侧表格的样式=== ========================================================
        self.left_widget.setStyleSheet(LEFT_WIDGET_STYLE_SHEET)                               # 主界面 - 左侧导航栏样式
        self.right_widget.setStyleSheet(RIGHT_WIDGET_STYLE_SHEET)
        self.right_bar_widget.setStyleSheet(RIGHT_WIDGET_STYLE_SHEET)                          # 坐标环绕  四顾浏览样式
        self.right_bar_point_around_widget.setStyleSheet(RIGHT_WIDGET_STYLE_SHEET)             # 坐标环绕  环绕浏览样式
        self.right_bar_point_ring_widget.setStyleSheet(RIGHT_WIDGET_STYLE_SHEET)               # 坐标环绕  圆环饼图样式
        self.right_bar_point_day24_widget.setStyleSheet(RIGHT_WIDGET_STYLE_SHEET)              # 坐标环绕  缩小时环图
        self.right_bar_line_widget.setStyleSheet(RIGHT_WIDGET_STYLE_SHEET)                     # 线路浏览
        self.right_bar_polygon_widget.setStyleSheet(RIGHT_WIDGET_STYLE_SHEET)                  # 省市县的生成
        self.right_bar_polygon_show_widget.setStyleSheet(RIGHT_WIDGET_STYLE_SHEET)             # 地图浏览

        # ======================设置网格布局层中部件的间隙=== ========================================================
        self.right_layout.addWidget(self.right_bar_widget, 2, 0, 1, 9)               # 注册右侧 中心浏览
        self.right_layout.addWidget(self.right_bar_point_around_widget, 2, 0, 1, 9)  # 注册右侧 环绕浏览
        self.right_layout.addWidget(self.right_bar_point_ring_widget, 2, 0, 1, 9)    # 注册右侧 圆环饼图
        self.right_layout.addWidget(self.right_bar_point_day24_widget, 2, 0, 1, 9)  # 注册右侧 圆环饼图
        # self.right_layout.addWidget(self.right_bar_filing_widget, 2, 0, 1, 9)        # 注册右侧 视频文案 ===========
        self.right_layout.addWidget(self.right_bar_line_widget, 2, 0, 1, 9)          # 注册右侧 圆环饼图
        self.right_layout.addWidget(self.right_bar_polygon_widget, 2, 0, 1, 9)       # 注册右侧 圆环饼图
        self.right_layout.addWidget(self.right_bar_polygon_show_widget, 2, 0, 1, 9)  # 注册右侧 区域渐显
        self.right_bar_point_around_widget.hide()
        self.right_bar_point_ring_widget.hide()
        self.right_bar_line_widget.hide()
        self.right_bar_polygon_widget.hide()
        self.right_bar_point_day24_widget.hide()
        self.right_bar_polygon_show_widget.show()
        self.right_bar_widget.hide() # show

        self.main_layout.setSpacing(0)  # 设置网格布局层中部件的间隙

        # ======================左侧导航栏被点击===========================================================
        self.left_close.clicked.connect(self.on_left_widget_button_clicked)  # 关闭按钮
        self.left_mini.clicked.connect(self.on_left_widget_button_clicked)  # 最小化按钮
        self.left_button_1.clicked.connect(self.on_left_widget_button_clicked)  # 四顾浏览
        self.left_button_2.clicked.connect(self.on_left_widget_button_clicked)  # 环绕浏览
        self.left_button_3.clicked.connect(self.on_left_widget_button_clicked)  # 圆饼环图
        self.left_button_4.clicked.connect(self.on_left_widget_button_clicked)  # 圆饼环图
        self.left_button_7.clicked.connect(self.on_left_widget_button_clicked)  # 圆饼环图
        self.left_button_10.clicked.connect(self.on_left_widget_button_clicked)  # 缩时环景
        self.left_button_5.clicked.connect(self.on_left_widget_button_clicked)   # 区域渐显

        # ======================区域浮现 下载====================================================
        self.right_bar_tour_show_polygon_file.clicked.connect(self.right_bar_tour_show_polygon_file_slider_connect)
        self.right_bar_tour_show_polygon_color_input.clicked.connect(self.right_bar_tour_show_polygon_color_input_connect)
        self.right_bar_tour_show_polygon_file_button_download.clicked.connect(self.on_tour_show_polygon_push_button_clicked)
        self.right_bar_tour_show_polygon_color_transparent_slider.valueChanged.connect(self.right_bar_tour_show_polygon_color_transparent_slider_holder_connect)


        # ======================省市县区 下载====================================================
        self.right_bar_widget_polygon_province_input.activated.connect(self.on_tour_province_city_button_clicked)
        self.right_bar_widget_polygon_city_input.activated.connect(self.on_tour_city_town_button_clicked)
        self.right_bar_widget_polygon_button_download.clicked.connect(self.on_tour_polygon_push_button_clicked)

        # ======================线路浏览 下载====================================================
        self.right_bar_tour_line_file.clicked.connect(self.right_bar_tour_line_file_slider_connect)
        self.right_bar_tour_line_file_button_download.clicked.connect(self.on_tour_line_file_push_button_clicked)

        # ======================坐标浏览 圆环饼图 下载====================================================
        self.right_bar_widget_point_ring_button_download.clicked.connect(self.on_tour_point_ring_kmlname_push_button_clicked)
        self.right_bar_widget_point_day24_button_download.clicked.connect(self.on_tour_point_day24_kmlname_push_button_clicked)

        # ======================环绕浏览 由中心向周围 观看====================================================
        # 事件监听 环绕浏览 高度 Altitude 環繞半徑 Radius 環繞視點高度 Height
        self.right_bar_widget_point_around_height_input.textChanged.connect(
            self.right_bar_widget_point_around_height_slider_connect)
        # 事件监听 环绕浏览 環繞視野角度 horizfov 提示
        self.right_bar_widget_point_around_horizfov_slider.valueChanged.connect(
            self.right_bar_widget_point_around_horizfov_slider_connect)
        # 事件监听 环绕浏览  環繞傾斜角度 Tilt 提示
        self.right_bar_widget_point_around_tilt_slider.valueChanged.connect(
            self.right_bar_widget_point_around_tilt_slider_connect)
        # 事件监听 环绕浏览  環繞啟始方向 heading 提示
        self.right_bar_widget_point_around_heading_slider.valueChanged.connect(
            self.right_bar_widget_point_around_heading_slider_connect)
        self.right_bar_widget_point_around_button_download.clicked.connect(
            self.on_tour_point_around_kmlname_push_button_clicked)

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
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件
        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框

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
            self.right_bar_line_widget.hide()
            self.right_bar_polygon_widget.hide()
            self.right_bar_point_day24_widget.hide()
            self.right_bar_polygon_show_widget.hide()
            self.right_bar_widget.show()
        if left_sender == '环绕浏览':
            self.right_bar_widget.hide()
            self.right_bar_point_ring_widget.hide()
            self.right_bar_line_widget.hide()
            self.right_bar_polygon_widget.hide()
            self.right_bar_point_day24_widget.hide()
            self.right_bar_polygon_show_widget.hide()
            self.right_bar_point_around_widget.show()
        if left_sender == "圆饼环图":
            self.right_bar_widget.hide()
            self.right_bar_point_around_widget.hide()
            self.right_bar_line_widget.hide()
            self.right_bar_polygon_widget.hide()
            self.right_bar_point_day24_widget.hide()
            self.right_bar_polygon_show_widget.hide()
            self.right_bar_point_ring_widget.show()
        if left_sender == "缩时环景":
            self.right_bar_widget.hide()
            self.right_bar_point_around_widget.hide()
            self.right_bar_line_widget.hide()
            self.right_bar_polygon_widget.hide()
            self.right_bar_point_ring_widget.hide()
            self.right_bar_polygon_show_widget.hide()
            self.right_bar_point_day24_widget.show()
        if left_sender == "线路浏览":
            self.right_bar_widget.hide()
            self.right_bar_point_around_widget.hide()
            self.right_bar_point_ring_widget.hide()
            self.right_bar_polygon_widget.hide()
            self.right_bar_polygon_show_widget.hide()
            self.right_bar_line_widget.show()
        if left_sender == "省市县区":
            self.right_bar_widget.hide()
            self.right_bar_point_around_widget.hide()
            self.right_bar_point_ring_widget.hide()
            self.right_bar_line_widget.hide()
            self.right_bar_polygon_show_widget.hide()
            self.right_bar_polygon_widget.show()
        if left_sender == "区域动画":
            self.right_bar_widget.hide()
            self.right_bar_point_around_widget.hide()
            self.right_bar_point_ring_widget.hide()
            self.right_bar_line_widget.hide()
            self.right_bar_polygon_widget.hide()
            self.right_bar_polygon_show_widget.show()

    # =========line===========区域变化=================================================

    def right_bar_tour_show_polygon_color_input_connect(self):

        colorDialog = QtWidgets.QColorDialog()
        colorDialog.setOption(QtWidgets.QColorDialog.ShowAlphaChannel)  # 启用透明度选项
        self.transparent_color = colorDialog.getColor()

        if self.transparent_color.isValid():
            # 处理选择的颜色
            self.right_bar_tour_show_polygon_color_input.setStyleSheet(f"background-color: {self.transparent_color.name()};")
            self.right_bar_tour_show_polygon_color_input.setText("")
            self.right_bar_tour_show_polygon_color_name = self.transparent_color.name()
            # 将8位颜色和透明度应用于按钮的背景颜色
            self.right_bar_tour_show_polygon_color_input.setStyleSheet(f"background-color: rgba({self.transparent_color.red()}, {self.transparent_color.green()}, {self.transparent_color.blue()}, {self.right_bar_tour_show_polygon_color_transparent_slider.value()});")
            print(f"background-color: rgba({self.transparent_color.red()}, {self.transparent_color.green()}, {self.transparent_color.blue()}, {self.right_bar_tour_show_polygon_color_transparent_slider.value()});")
            self.right_bar_tour_show_polygon_color_name = simplekml.Color.changealphaint(self.right_bar_tour_show_polygon_color_transparent_slider.value(), simplekml.Color.rgb(self.transparent_color.red(), self.transparent_color.green(), self.transparent_color.blue()))


    def right_bar_tour_show_polygon_color_transparent_slider_holder_connect(self):
        try:
            slider_transparent_value = self.right_bar_tour_show_polygon_color_transparent_slider.value()  # 获取当前滑块值
            self.right_bar_tour_show_polygon_color_transparent_slider_holder_value.setText('%s°' % slider_transparent_value)
            self.right_bar_tour_show_polygon_color_input.setStyleSheet(f"background-color: rgba({self.transparent_color.red()}, {self.transparent_color.green()}, {self.transparent_color.blue()}, {self.right_bar_tour_show_polygon_color_transparent_slider.value()});")
            self.right_bar_tour_show_polygon_color_name = simplekml.Color.changealphaint(
                self.right_bar_tour_show_polygon_color_transparent_slider.value(),
                simplekml.Color.rgb(self.transparent_color.red(), self.transparent_color.green(), self.transparent_color.blue())
            )
        except Exception as e:
            traceback.print_exc()
            QtWidgets.QMessageBox.warning(self, "提示", "请先选择颜色!")

    def right_bar_tour_show_polygon_file_slider_connect(self):
        try:
            filename = QtWidgets.QFileDialog.getOpenFileNames(self, '选择图像', UPLOAD_PATH, "All Files(*);;Text Files(*.txt)")
            show_file_name = filename[0][0].split('/')[-1]
            self.right_bar_tour_show_polygon_file_holder.setText(show_file_name)
            self.right_bar_tour_show_polygon_filepath_coords = parser_polygon_coords(filename[0][0])

        except Exception as e:
            traceback.print_exc()
            QtWidgets.QMessageBox.warning(self, "提示", "上传文件不正确!")

    def on_tour_show_polygon_push_button_clicked(self):

        try:

            selected_id = self.right_bar_tour_show_polygon_type_group_button.checkedId()
            kmlname = self.right_bar_widget_show_polygon_kmlname_input.text()
            if selected_id == 1:
                TourPolygonShow(kmlname).tour_polygon_linear(
                    kmlname=kmlname if kmlname else '',
                    tour_time=float(self.right_bar_widget_show_polygon_time_input.text()),
                    poly_color=self.right_bar_tour_show_polygon_color_name,
                    polygon_coords=self.right_bar_tour_show_polygon_filepath_coords
                )
            elif selected_id == 0:
                TourChangePolygon().tour_polygon_change(
                    kmlname=kmlname if kmlname else '',
                    tour_time=float(self.right_bar_widget_show_polygon_time_input.text()),
                    poly_coords=self.right_bar_tour_show_polygon_filepath_coords
                )

            QtWidgets.QMessageBox.information(self, "提示", "下载成功！")
        except Exception as e:
            import traceback
            traceback.print_exc()
            QtWidgets.QMessageBox.warning(self, "提示", "输入的数据有误!")

    # ======================================省市县区============================================================
    # 省份-城市-联动
    def on_tour_province_city_button_clicked(self):
        self.right_bar_widget_polygon_city_input.clear()
        self.right_bar_widget_polygon_city_input.addItem(u'请选择')
        self.right_bar_widget_polygon_town_input.clear()
        self.right_bar_widget_polygon_town_input.addItem(u'请选择')

        province_name = self.right_bar_widget_polygon_province_input.currentText()
        province = LuckyAreas.get_or_none(area_name=province_name)
        if province:
            self.ad_code_province = province.adcode
            citys = LuckyAreas.select(LuckyAreas.adcode, LuckyAreas.area_name).where(LuckyAreas.parent_code==province.adcode)
            for city in citys:
                self.right_bar_widget_polygon_city_input.addItem(city.area_name)

    # 市区-县区-联动
    def on_tour_city_town_button_clicked(self):
        self.right_bar_widget_polygon_town_input.clear()
        self.right_bar_widget_polygon_town_input.addItem(u'请选择')

        city_name = self.right_bar_widget_polygon_city_input.currentText()
        city = LuckyAreas.get_or_none(area_name=city_name)
        if city:
            self.ad_code_city = city.adcode
            citys = LuckyAreas.select(LuckyAreas.adcode, LuckyAreas.area_name).where(LuckyAreas.parent_code==city.adcode)
            for city in citys:
                self.right_bar_widget_polygon_town_input.addItem(city.area_name)

    def on_tour_polygon_push_button_clicked(self):
        """
        省市县区 下载文件
        :return:
        """
        self.right_bar_widget_polygon_button_download.setEnabled(False)  # 按钮不可点击
        self.thread_polygon = ThreadPolygon(                   # 实例化自己建立的任务线程类
            country=self.right_bar_widget_polygon_country_input.currentText(),
            province=self.right_bar_widget_polygon_province_input.currentText(),
            city=self.right_bar_widget_polygon_city_input.currentText(),
            town=self.right_bar_widget_polygon_town_input.currentText(),
            children=self.right_bar_tour_polygon_children_group_button.checkedId(),  # 返回选中按钮的id
            color=self.right_bar_tour_polygon_color_group_button.checkedId()
        )  # 实例化自己建立的任务线程类
        self.thread_polygon.signal.connect(self.right_bar_tour_polygon_download_success)  # 设置任务线程发射信号触发的函数
        self.thread_polygon.start()

    def right_bar_tour_polygon_download_success(self, status):
        if status:
            QtWidgets.QMessageBox.information(self, "提示", "下载成功！")
        else:
            QtWidgets.QMessageBox.warning(self, "提示", "下载失败！")
        self.right_bar_widget_polygon_button_download.setEnabled(True)  # 按钮可点击

    # =========line===========线路浏览=================================================
    def right_bar_tour_line_file_slider_connect(self):
        try:
            filename = QtWidgets.QFileDialog.getOpenFileNames(self, '选择图像', UPLOAD_PATH, "All Files(*);;Text Files(*.txt)")
            show_file_name = filename[0][0].split('/')[-1]
            self.right_bar_tour_line_file_holder.setText(show_file_name)
            self.right_bar_tour_line_filepath_coords = parser_line_coords(filename[0][0])

            # 路线的坐标数量， 路线的距离
            self.right_bar_tour_line_filepath_length, self.right_bar_tour_line_filepath_distance = parser_line_distance(self.right_bar_tour_line_filepath_coords)

        except Exception as e:
            traceback.print_exc()
            QtWidgets.QMessageBox.warning(self, "提示", "上传文件不正确!")

    def right_bar_tour_line_download_success(self, status):
        if status:
            QtWidgets.QMessageBox.information(self, "提示", "下载成功！")
        else:
            QtWidgets.QMessageBox.warning(self, "提示", "下载失败！")
        self.right_bar_tour_line_file_button_download.setEnabled(True)  # 按钮可点击

    def on_tour_line_file_push_button_clicked(self):
        """
        :return:
        """
        print(self.right_bar_tour_line_flag_yes_button.isChecked())
        if self.right_bar_tour_line_filepath_coords is None:
            QtWidgets.QMessageBox.warning(self, "提示", "请选择上传文件!")
        else:
            self.right_bar_tour_line_file_button_download.setEnabled(False)  # 按钮不可点击
            self.thread_line = ThreadLine(
                kmlname=self.right_bar_widget_line_kmlname_input.text(),
                is_mode=self.right_bar_tour_line_flag_yes_button.isChecked(),
                tour_type=self.right_bar_widget_line_tour_type_input.currentText(),
                tour_time=int(self.right_bar_widget_line_tour_time_input.text()),
                coords=self.right_bar_tour_line_filepath_coords,
                length=self.right_bar_tour_line_filepath_length,
                distance=self.right_bar_tour_line_filepath_distance
            )  # 实例化自己建立的任务线程类
            self.thread_line.signal.connect(self.right_bar_tour_line_download_success)  # 设置任务线程发射信号触发的函数
            self.thread_line.start()

    # =========point===========缩时环景=================================================
    def on_tour_point_day24_kmlname_push_button_clicked(self):
        """
        环绕浏览 啟始方向 当前值
        :param value:
        :return:
        """
        data = {
            'kmlname': self.right_bar_widget_point_day24_kmlname_input.text(),
            'latitude': float(self.right_bar_widget_point_day24_latitude_input.text()),
            'longitude': float(self.right_bar_widget_point_day24_longitude_input.text()),
            'altitude': int(self.right_bar_widget_point_day24_altitude_input.text())
        }
        kmlname = self.right_bar_widget_point_day24_kmlname_input.text()
        kmlname = kmlname if kmlname else ''
        print(data)
        try:
            TourPointDay24(kmlname).tour_point_day_neight_change(
                kmlname=self.right_bar_widget_point_day24_kmlname_input.text(),
                latitude=float(self.right_bar_widget_point_day24_latitude_input.text()),
                longitude=float(self.right_bar_widget_point_day24_longitude_input.text()),
                altitude=int(self.right_bar_widget_point_day24_altitude_input.text())
            )
            QtWidgets.QMessageBox.information(self, "提示", "下载成功！")
        except Exception as e:
            import traceback
            traceback.print_exc()
            QtWidgets.QMessageBox.warning(self, "提示", "输入的数据有误!")

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
            'longitude': float(self.right_bar_widget_point_ring_longitude_input.text()),
            'outer_radius': int(self.right_bar_widget_point_ring_outer_radius_input.text()),
            'inner_radius': int(self.right_bar_widget_point_ring_inner_radius_input.text())
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
            kmlname = self.right_bar_widget_point_around_kmlname_input.text()
            TourPointAround(kmlname).tour_point_around(
                kmlname=kmlname,
                longitude=float(self.right_bar_widget_point_around_longitude_input.text()),  # 经度
                latitude=float(self.right_bar_widget_point_around_latitude_input.text()),  # 纬度
                altitude=self.right_bar_widget_point_around_altitude_input.text(),  # 实际:467.9   高度 1.67 倍
                horizfov=self.right_bar_widget_point_around_horizfov_slider.value(),
                tilt=self.right_bar_widget_point_around_tilt_slider.value(),  # 环绕倾斜角度
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

    # 重写三个方法使我们的Example窗口支持拖动,上面参数window就是拖动对象
    def mousePressEvent(self, event):  # 鼠标长按事件

        if event.buttons() == QtCore.Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))

    def enterEvent (self, event):   # =鼠标进入控件事件
        print("========鼠标进入控件事件==================")
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        if now > EXPIRED_DATE:
            QtWidgets.QMessageBox.warning(self, "提示", EXPIRED_WARN)
            self.close()

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
    try:
        app = QtWidgets.QApplication(sys.argv)
        gui = MainUi()
        gui.show()
        sys.exit(app.exec_())
    except Exception as e:
        from settings.constant import FILEPATH
        l = FILEPATH + '/a.log'
        with open(l, 'w') as f:
            f.write(str(e))
        print(e)


if __name__ == '__main__':
    main()