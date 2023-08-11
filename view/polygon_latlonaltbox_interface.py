import traceback
from PyQt5 import QtCore, QtGui, QtWidgets
import simplekml
from settings.model import LuckyAreas
from tour.tour_polygon_change import TourChangePolygon
from tour.polygon_latlonalt_box import PolygonLatLonAltBoxGenerator

class PolygonLatLonaltBoxView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        # ======================右侧点击-区域渐显====================================================
        self.right_bar_polygon_latlonaltbox_widget = QtWidgets.QWidget()  # 右侧顶部搜索框部件
        self.right_bar_polygon_latlonaltbox_layout = QtWidgets.QGridLayout()  # 右侧顶部搜索框网格布局
        self.right_bar_polygon_latlonaltbox_widget.setLayout(self.right_bar_polygon_latlonaltbox_layout)

        self.right_bar_tour_latlonaltbox_polygon = QtWidgets.QPushButton("区域显示")
        self.right_bar_tour_latlonaltbox_polygon.setObjectName("right_lable_title")

        # 名称输入框
        self.right_bar_tour_latlonaltbox_polygon_kmlname = QtWidgets.QLabel('名称  Kmlname')
        self.right_bar_tour_latlonaltbox_polygon_kmlname.setObjectName("right_bar_tour_label")
        self.right_bar_widget_latlonaltbox_polygon_kmlname_input = QtWidgets.QLineEdit()
        self.right_bar_widget_latlonaltbox_polygon_kmlname_input.setText('区域显示')
        self.right_bar_widget_latlonaltbox_polygon_kmlname_input.setPlaceholderText("输入要保存的文件名")
        self.right_bar_widget_latlonaltbox_polygon_kmlname_input.setObjectName('right_bar_widget_qlinedit_input')

        # minLodPixels 和 maxLodPixels： 控制不同缩放级别下的显示和隐藏
        self.right_bar_widget_latlonaltbox_polygon_min_lod_pixels = QtWidgets.QLabel('minLodPixels')  # 文字栏
        self.right_bar_widget_latlonaltbox_polygon_min_lod_pixels.setObjectName("right_bar_tour_label")
        self.right_bar_widget_latlonaltbox_polygon_min_lod_pixels_input = QtWidgets.QLineEdit()
        self.right_bar_widget_latlonaltbox_polygon_min_lod_pixels_input.setText('128')
        self.right_bar_widget_latlonaltbox_polygon_min_lod_pixels_input.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_widget_latlonaltbox_polygon_min_lod_pixels_input_holder = QtWidgets.QLabel("此像素大小以下的缩放级别将始终可见")  # 提示栏
        self.right_bar_widget_latlonaltbox_polygon_min_lod_pixels_input_holder.setObjectName("right_bar_widget_holder")

        self.right_bar_widget_latlonaltbox_polygon_max_lod_pixels = QtWidgets.QLabel('maxLodPixels')  # 文字栏
        self.right_bar_widget_latlonaltbox_polygon_max_lod_pixels.setObjectName("right_bar_tour_label")
        self.right_bar_widget_latlonaltbox_polygon_max_lod_pixels_input = QtWidgets.QLineEdit()
        self.right_bar_widget_latlonaltbox_polygon_max_lod_pixels_input.setText('512')
        self.right_bar_widget_latlonaltbox_polygon_max_lod_pixels_input.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_widget_latlonaltbox_polygon_max_lod_pixels_input_holder = QtWidgets.QLabel("此像素大小以上的缩放级别元素将始终隐藏")  # 提示栏
        self.right_bar_widget_latlonaltbox_polygon_max_lod_pixels_input_holder.setObjectName("right_bar_widget_holder")

        # minFadeExtent 和 maxFadeExtent 过渡范围内的渐变效果，从完全可见到完全隐藏或从完全隐藏到完全可见
        self.right_bar_widget_latlonaltbox_polygon_min_fade_extent= QtWidgets.QLabel('minFadeExtent')  # 文字栏
        self.right_bar_widget_latlonaltbox_polygon_min_fade_extent.setObjectName("right_bar_tour_label")
        self.right_bar_widget_latlonaltbox_polygon_min_fade_extent_input = QtWidgets.QLineEdit()
        self.right_bar_widget_latlonaltbox_polygon_min_fade_extent_input.setText('64')
        self.right_bar_widget_latlonaltbox_polygon_min_fade_extent_input.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_widget_latlonaltbox_polygon_min_fade_extent_input_holder = QtWidgets.QLabel("从完全可见到完全隐藏的过渡范围的最小像素值")  # 提示栏
        self.right_bar_widget_latlonaltbox_polygon_min_fade_extent_input_holder.setObjectName("right_bar_widget_holder")

        self.right_bar_widget_latlonaltbox_polygon_max_fade_extent= QtWidgets.QLabel('maxFadeExtent')  # 文字栏
        self.right_bar_widget_latlonaltbox_polygon_max_fade_extent.setObjectName("right_bar_tour_label")
        self.right_bar_widget_latlonaltbox_polygon_max_fade_extent_input = QtWidgets.QLineEdit()
        self.right_bar_widget_latlonaltbox_polygon_max_fade_extent_input.setText('256')
        self.right_bar_widget_latlonaltbox_polygon_max_fade_extent_input.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_widget_latlonaltbox_polygon_max_fade_extent_input_holder = QtWidgets.QLabel("从完全隐藏到完全可见的过渡范围的最大像素值")  # 提示栏
        self.right_bar_widget_latlonaltbox_polygon_max_fade_extent_input_holder.setObjectName("right_bar_widget_holder")

        self.right_bar_tour_latlonaltbox_polygon_color = QtWidgets.QLabel('颜色&透明度')                # transparent
        self.right_bar_tour_latlonaltbox_polygon_color.setObjectName("right_bar_tour_label")
        self.right_bar_tour_latlonaltbox_polygon_color_input = QtWidgets.QPushButton("选择颜色")
        self.right_bar_tour_latlonaltbox_polygon_color_transparent_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)  # 滑块框栏
        self.right_bar_tour_latlonaltbox_polygon_color_transparent_slider.setMinimum(0)  # 设置最小值
        self.right_bar_tour_latlonaltbox_polygon_color_transparent_slider.setMaximum(255)  # 设置最大值
        self.right_bar_tour_latlonaltbox_polygon_color_transparent_slider.setSingleStep(1)  # 设置滑动步长
        self.right_bar_tour_latlonaltbox_polygon_color_transparent_slider.setValue(150)
        self.right_bar_tour_latlonaltbox_polygon_color_transparent_slider_holder_value = QtWidgets.QLabel("150")  # 提示文字
        self.right_bar_tour_latlonaltbox_polygon_color_name = ''  # 颜色

        # 线路浏览 线路浏览 线路文件
        self.right_bar_tour_latlonaltbox_polygon_file = QtWidgets.QPushButton('上传文件')
        self.right_bar_tour_latlonaltbox_polygon_file.setObjectName("right_bar_tour_line_tour_file_button")
        self.right_bar_tour_latlonaltbox_polygon_file_holder = QtWidgets.QLabel('请选择上传的文件')
        self.right_bar_tour_latlonaltbox_polygon_file_holder.setObjectName("right_bar_widget_holder")
        self.right_bar_tour_latlonaltbox_polygon_filepath_coords = None  # 下载实际路径页面不展示

        # 线路浏览 线路浏览 下载
        self.right_bar_tour_latlonaltbox_polygon_file_button_download = QtWidgets.QPushButton()
        self.right_bar_tour_latlonaltbox_polygon_file_button_download.setText("确定")
        self.right_bar_tour_latlonaltbox_polygon_file_button_download.setObjectName('right_bar_tour_button_download')

        self.right_newsong_label = QtWidgets.QLabel("最新歌曲")
        self.right_newsong_label.setObjectName('right_label')
        self.right_newsong_widget = QtWidgets.QWidget()  # 最新歌曲部件
        self.right_newsong_layout = QtWidgets.QGridLayout()  # 最新歌曲部件网格布局
        self.right_newsong_widget.setLayout(self.right_newsong_layout)
        self.right_newsong_widget.setStyleSheet('''
            QPushButton{border:none;color:gray;font-size:12px;height:40px;padding-left:5px;padding-right:10px;text-align:left;}
            QPushButton:hover{color:black;border:1px solid #F3F3F5;border-radius:10px;background:LightGray;}
            '''
        )  # 去除边框，修改字体和颜色等

        self.newsong_button1 = QtWidgets.QPushButton("夜机 陈慧娴 永远的朋友 03::29")
        self.newsong_button2 = QtWidgets.QPushButton("夜机 陈慧娴 永远的朋友 03::29")
        self.newsong_button3 = QtWidgets.QPushButton("夜机 陈慧娴 永远的朋友 03::29")
        self.newsong_button4 = QtWidgets.QPushButton("夜机 陈慧娴 永远的朋友 03::29")
        self.newsong_button5 = QtWidgets.QPushButton("夜机 陈慧娴 永远的朋友 03::29")
        self.newsong_button6 = QtWidgets.QPushButton("夜机 陈慧娴 永远的朋友 03::29")

        self.right_newsong_layout.addWidget(self.newsong_button1, 0, 0)
        self.right_newsong_layout.addWidget(self.newsong_button2, 1, 0)
        self.right_newsong_layout.addWidget(self.newsong_button3, 2, 0)
        self.right_newsong_layout.addWidget(self.newsong_button4, 3, 0)
        self.right_newsong_layout.addWidget(self.newsong_button5, 4, 0)
        self.right_newsong_layout.addWidget(self.newsong_button6, 5, 0)

        self.right_hotsong_label = QtWidgets.QLabel("热门歌单")
        self.right_hotsong_label.setObjectName('right_label')

        self.right_hotsong_widget = QtWidgets.QWidget()  # 热门歌单部件
        self.right_hotsong_layout = QtWidgets.QGridLayout()  # 热门歌单网格布局
        self.right_hotsong_widget.setLayout(self.right_hotsong_layout)
        self.right_hotsong_widget.setStyleSheet('''
            QToolButton{border:none;}QToolButton:hover{border-bottom:2px solid #F76677;}''')  # 去除边框

        self.hotsong_buttton1 = QtWidgets.QToolButton()
        self.hotsong_buttton1.setText('可馨HANM')
        self.hotsong_buttton1.setIcon(QtGui.QIcon('./ri.jpg'))
        self.hotsong_buttton1.setIconSize(QtCore.QSize(100, 100))
        self.hotsong_buttton1.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.hotsong_buttton2 = QtWidgets.QToolButton()
        self.hotsong_buttton2.setText('可馨HANM')
        self.hotsong_buttton2.setIcon(QtGui.QIcon('./ri.jpg'))
        self.hotsong_buttton2.setIconSize(QtCore.QSize(100, 100))
        self.hotsong_buttton2.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.hotsong_buttton3 = QtWidgets.QToolButton()
        self.hotsong_buttton3.setText('可馨HANM')
        self.hotsong_buttton3.setIcon(QtGui.QIcon('./ri.jpg'))
        self.hotsong_buttton3.setIconSize(QtCore.QSize(100, 100))
        self.hotsong_buttton3.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.hotsong_buttton4 = QtWidgets.QToolButton()
        self.hotsong_buttton4.setText('可馨HANM')
        self.hotsong_buttton4.setIcon(QtGui.QIcon('./ri.jpg'))
        self.hotsong_buttton4.setIconSize(QtCore.QSize(100, 100))
        self.hotsong_buttton4.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.right_hotsong_layout.addWidget(self.hotsong_buttton1, 0, 0)
        self.right_hotsong_layout.addWidget(self.hotsong_buttton2, 0, 1)
        self.right_hotsong_layout.addWidget(self.hotsong_buttton3, 1, 0)
        self.right_hotsong_layout.addWidget(self.hotsong_buttton4, 1, 1)


        self.right_bar_polygon_latlonaltbox_layout.addWidget(self.right_bar_tour_latlonaltbox_polygon, 0, 0, 1, 1)  # 单独水平线
        self.right_bar_polygon_latlonaltbox_layout.addWidget(self.right_bar_tour_latlonaltbox_polygon_kmlname, 1, 0, 1, 1)
        self.right_bar_polygon_latlonaltbox_layout.addWidget(self.right_bar_widget_latlonaltbox_polygon_kmlname_input, 1, 1, 1, 5)

        self.right_bar_polygon_latlonaltbox_layout.addWidget(self.right_bar_widget_latlonaltbox_polygon_min_lod_pixels, 2, 0, 1, 1)
        self.right_bar_polygon_latlonaltbox_layout.addWidget(self.right_bar_widget_latlonaltbox_polygon_min_lod_pixels_input, 2, 1, 1, 2)
        self.right_bar_polygon_latlonaltbox_layout.addWidget(self.right_bar_widget_latlonaltbox_polygon_min_lod_pixels_input_holder, 2, 3, 1, 1)

        self.right_bar_polygon_latlonaltbox_layout.addWidget(self.right_bar_widget_latlonaltbox_polygon_max_lod_pixels, 3, 0, 1, 1)
        self.right_bar_polygon_latlonaltbox_layout.addWidget(self.right_bar_widget_latlonaltbox_polygon_max_lod_pixels_input, 3, 1, 1, 2)
        self.right_bar_polygon_latlonaltbox_layout.addWidget(self.right_bar_widget_latlonaltbox_polygon_max_lod_pixels_input_holder, 3, 3, 1, 1)

        self.right_bar_polygon_latlonaltbox_layout.addWidget(self.right_bar_widget_latlonaltbox_polygon_max_lod_pixels, 3, 0, 1, 1)
        self.right_bar_polygon_latlonaltbox_layout.addWidget(self.right_bar_widget_latlonaltbox_polygon_max_lod_pixels_input, 3, 1, 1, 2)
        self.right_bar_polygon_latlonaltbox_layout.addWidget(self.right_bar_widget_latlonaltbox_polygon_max_lod_pixels_input_holder, 3, 3, 1, 1)

        self.right_bar_polygon_latlonaltbox_layout.addWidget(self.right_bar_widget_latlonaltbox_polygon_min_fade_extent, 4, 0, 1, 1)
        self.right_bar_polygon_latlonaltbox_layout.addWidget(self.right_bar_widget_latlonaltbox_polygon_min_fade_extent_input, 4, 1, 1, 2)
        self.right_bar_polygon_latlonaltbox_layout.addWidget(self.right_bar_widget_latlonaltbox_polygon_min_fade_extent_input_holder, 4, 3, 1, 1)

        self.right_bar_polygon_latlonaltbox_layout.addWidget(self.right_bar_widget_latlonaltbox_polygon_max_fade_extent, 5, 0, 1, 1)
        self.right_bar_polygon_latlonaltbox_layout.addWidget(self.right_bar_widget_latlonaltbox_polygon_max_fade_extent_input, 5, 1, 1, 2)
        self.right_bar_polygon_latlonaltbox_layout.addWidget(self.right_bar_widget_latlonaltbox_polygon_max_fade_extent_input_holder, 5, 3, 1, 1)

        self.right_bar_polygon_latlonaltbox_layout.addWidget(self.right_bar_tour_latlonaltbox_polygon_color, 6, 0, 1, 1)
        self.right_bar_polygon_latlonaltbox_layout.addWidget(self.right_bar_tour_latlonaltbox_polygon_color_input, 6, 1, 1, 1)
        self.right_bar_polygon_latlonaltbox_layout.addWidget(self.right_bar_tour_latlonaltbox_polygon_color_transparent_slider, 6, 2, 1, 4)
        self.right_bar_polygon_latlonaltbox_layout.addWidget(self.right_bar_tour_latlonaltbox_polygon_color_transparent_slider_holder_value, 6, 6, 1, 6)

        self.right_bar_polygon_latlonaltbox_layout.addWidget(self.right_bar_tour_latlonaltbox_polygon_file, 7, 1, 1, 2)  # 修改列索引为0
        self.right_bar_polygon_latlonaltbox_layout.addWidget(self.right_bar_tour_latlonaltbox_polygon_file_holder, 7, 3, 1, 2)  # 修改列索引为1，跨越列数为2
        self.right_bar_polygon_latlonaltbox_layout.addWidget(self.right_bar_tour_latlonaltbox_polygon_file_button_download, 8, 1, 1, 2)  # 修改列索引为3

        self.right_bar_polygon_latlonaltbox_layout.addWidget(self.right_newsong_label, 9, 0, 1, 5)
        self.right_bar_polygon_latlonaltbox_layout.addWidget(self.right_hotsong_label, 9, 5, 1, 4)
        self.right_bar_polygon_latlonaltbox_layout.addWidget(self.right_newsong_widget, 10, 0, 1, 5)
        self.right_bar_polygon_latlonaltbox_layout.addWidget(self.right_hotsong_widget, 10, 5, 1, 4)

        self.right_newsong_label.hide()  # 隐藏 "热门歌单" 标签
        self.right_hotsong_label.hide()  # 隐藏热门歌单部件
        self.right_newsong_widget.hide()  # 隐藏 "热门歌单" 标签
        self.right_hotsong_widget.hide()  # 隐藏热门歌单部件

        # self.right_bar_tour_latlonaltbox_polygon_file.clicked.connect(self.right_bar_tour_latlonaltbox_polygon_file_slider_connect)
        # self.right_bar_tour_latlonaltbox_polygon_color_input.clicked.connect(self.right_bar_tour_latlonaltbox_polygon_color_input_connect)
        # self.right_bar_tour_latlonaltbox_polygon_file_button_download.clicked.connect(self.on_tour_latlonaltbox_polygon_push_button_clicked)
        # self.right_bar_tour_latlonaltbox_polygon_color_transparent_slider.valueChanged.connect(self.right_bar_tour_latlonaltbox_polygon_color_transparent_slider_holder_connect)

        self.setLayout(self.right_bar_polygon_latlonaltbox_layout)

