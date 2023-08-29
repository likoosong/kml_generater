import traceback
from PyQt5 import QtCore, QtGui, QtWidgets

from utlis.util import random_content
from utlis.show_toast_interface import Toast, AlertLevel
from tour.tour_polygon_change import TourChangePolygon
from utlis.parser_line_coords import parser_polygon_coords
from settings.constant import UPLOAD_PATH

class PolygonChangeView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        # ======================右侧点击-区域渐显====================================================
        self.right_bar_polygon_change_widget = QtWidgets.QWidget()  # 右侧顶部搜索框部件
        self.right_bar_polygon_change_layout = QtWidgets.QGridLayout()  # 右侧顶部搜索框网格布局
        self.right_bar_polygon_change_widget.setLayout(self.right_bar_polygon_change_layout)

        self.right_bar_tour_change_polygon = QtWidgets.QPushButton("形状变化")
        self.right_bar_tour_change_polygon.setObjectName("right_lable_title")

        # 名称输入框
        self.right_bar_tour_change_polygon_kmlname_lable = QtWidgets.QLabel('名称  Kmlname')
        self.right_bar_tour_change_polygon_kmlname_lable.setObjectName("right_bar_tour_label")
        self.right_bar_widget_change_polygon_kmlname_input = QtWidgets.QLineEdit()
        self.right_bar_widget_change_polygon_kmlname_input.setText('形状变化')
        self.right_bar_widget_change_polygon_kmlname_input.setPlaceholderText("输入要保存的文件名")
        self.right_bar_widget_change_polygon_kmlname_input.setObjectName('right_bar_widget_qlinedit_input')

        self.right_bar_tour_change_polygon_time = QtWidgets.QLabel('时间')
        self.right_bar_tour_change_polygon_time.setObjectName("right_bar_tour_label")
        self.right_bar_widget_change_polygon_time_input = QtWidgets.QLineEdit()
        self.right_bar_widget_change_polygon_time_input.setText('3')
        self.right_bar_widget_change_polygon_time_input.setPlaceholderText("单个polygon时间")
        self.right_bar_widget_change_polygon_time_input.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_widget_change_polygon_time_input_holder = QtWidgets.QLabel("单个polygon时间")  # 提示栏
        self.right_bar_widget_change_polygon_time_input_holder.setObjectName("right_bar_widget_holder")

        # 线路浏览 线路浏览 线路文件
        self.right_bar_tour_change_polygon_file = QtWidgets.QPushButton('上传文件')
        self.right_bar_tour_change_polygon_file.setObjectName("right_bar_tour_line_tour_file_button")
        self.right_bar_tour_change_polygon_file_holder = QtWidgets.QLabel('请选择上传的文件')
        self.right_bar_tour_change_polygon_file_holder.setObjectName("right_bar_widget_holder")
        self.right_bar_tour_change_polygon_filepath_coords = None  # 下载实际路径页面不展示

        # 线路浏览 线路浏览 下载
        self.right_bar_tour_change_polygon_file_button_download = QtWidgets.QPushButton()
        self.right_bar_tour_change_polygon_file_button_download.setText("确定")
        self.right_bar_tour_change_polygon_file_button_download.setObjectName('right_bar_tour_button_download')
        self.right_bar_widget_change_polygon_file_placeholder = QtWidgets.QLabel("")  # 占位符

        # 第0行，第0列，添加一个标签小部件，不跨行，跨1列
        self.right_bar_polygon_change_layout.addWidget(self.right_bar_tour_change_polygon, 0, 0, 1, 1)
        # 第1行，第0列，添加一个标签小部件，不跨行，跨1列
        self.right_bar_polygon_change_layout.addWidget(self.right_bar_tour_change_polygon_kmlname_lable, 1, 0, 1, 1)
        # 第1行，第1列，添加一个输入框小部件，不跨行，跨5列
        self.right_bar_polygon_change_layout.addWidget(self.right_bar_widget_change_polygon_kmlname_input, 1, 1, 1, 5)
        # 第2行，第0列，添加一个标签小部件，不跨行，跨1列
        self.right_bar_polygon_change_layout.addWidget(self.right_bar_tour_change_polygon_time, 2, 0, 1, 1)
        # 第2行，第1列，添加一个输入框小部件，不跨行，跨2列
        self.right_bar_polygon_change_layout.addWidget(self.right_bar_widget_change_polygon_time_input, 2, 1, 1, 2)
        # 第2行，第3列，添加另一个输入框小部件，不跨行，跨6列
        self.right_bar_polygon_change_layout.addWidget(self.right_bar_widget_change_polygon_time_input_holder, 2, 3, 1, 6)
        # 第3行，第1列，添加一个标签小部件，不跨行，跨2列
        self.right_bar_polygon_change_layout.addWidget(self.right_bar_tour_change_polygon_file, 3, 1, 1, 2)
        # 第3行，第3列，添加一个用于展示文件路径的标签或输入框小部件，不跨行，跨2列
        self.right_bar_polygon_change_layout.addWidget(self.right_bar_tour_change_polygon_file_holder, 3, 3, 1, 2)
        # 第4行，第1列，添加一个下载按钮小部件，不跨行，跨2列
        self.right_bar_polygon_change_layout.addWidget(self.right_bar_tour_change_polygon_file_button_download, 4, 1, 1, 2)

        self.right_bar_tour_change_polygon_file.clicked.connect(self.right_bar_tour_change_polygon_file_slider_connect)
        self.right_bar_tour_change_polygon_file_button_download.clicked.connect(self.on_tour_change_polygon_push_button_clicked)

        self.setLayout(self.right_bar_polygon_change_layout)

    def right_bar_tour_change_polygon_file_slider_connect(self):
        try:
            filename = QtWidgets.QFileDialog.getOpenFileNames(self, '选择图像', UPLOAD_PATH, "All Files(*);;Text Files(*.txt)")
            change_file_name = filename[0][0].split('/')[-1]
            self.right_bar_tour_change_polygon_file_holder.setText(change_file_name)
            self.right_bar_tour_change_polygon_filepath_coords = parser_polygon_coords(filename[0][0])

        except Exception as e:
            toast = Toast(title="提示", content="上传文件不正确!", level=AlertLevel.ERROR, parent=self)
            # 获取Demo窗口的顶部中心位置
            top_center_point = self.mapToGlobal(QtCore.QPoint(self.rect().width() // 2, 0))
            x_position = top_center_point.x() - toast.width() // 2
            y_position = top_center_point.y()
            toast.showToast(x_position, y_position)

    def on_tour_change_polygon_push_button_clicked(self):

        try:
            kmlname = self.right_bar_widget_change_polygon_kmlname_input.text()
            TourChangePolygon().tour_polygon_change(
                kmlname=kmlname if kmlname else '',
                tour_time=float(self.right_bar_widget_change_polygon_time_input.text()),
                poly_coords=self.right_bar_tour_change_polygon_filepath_coords
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