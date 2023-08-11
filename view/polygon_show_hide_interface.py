import traceback
from PyQt5 import QtCore, QtGui, QtWidgets
import simplekml
from settings.model import LuckyAreas
from tour.tour_polygon_change import TourChangePolygon
from tour.tour_polygon_show_hide import TourPolygonShow, TourPolygonHide

from utlis.parser_line_coords import parser_polygon_coords, parser_polygon_show_hide_coords
from settings.constant import UPLOAD_PATH

class PolygonShowHideView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        # ======================右侧点击-区域渐显====================================================
        self.right_bar_polygon_show_widget = QtWidgets.QWidget()  # 右侧顶部搜索框部件
        self.right_bar_polygon_show_layout = QtWidgets.QGridLayout()  # 右侧顶部搜索框网格布局
        self.right_bar_polygon_show_widget.setLayout(self.right_bar_polygon_show_layout)

        self.right_bar_tour_show_polygon = QtWidgets.QPushButton("渐隐渐藏")
        self.right_bar_tour_show_polygon.setObjectName("right_lable_title")

        # 区域渐显 动画方式 - 区域动画&形状变化动画
        self.right_bar_tour_show_polygon_type = QtWidgets.QLabel('动画方式')
        self.right_bar_tour_show_polygon_type.setObjectName("right_bar_tour_label")
        self.right_bar_tour_show_polygon_type_group_button = QtWidgets.QButtonGroup()  # 按钮分组
        self.right_bar_tour_show_polygon_type_yes_button = QtWidgets.QRadioButton("区域渐显")
        self.right_bar_tour_show_polygon_type_yes_button.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_tour_show_polygon_type_yes_button.setChecked(True)
        self.right_bar_tour_show_polygon_type_no_button = QtWidgets.QRadioButton("区域渐隐")
        self.right_bar_tour_show_polygon_type_no_button.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_tour_show_polygon_type_group_button.addButton(self.right_bar_tour_show_polygon_type_yes_button, 1)  # 设置ID为1
        self.right_bar_tour_show_polygon_type_group_button.addButton(self.right_bar_tour_show_polygon_type_no_button, 0)

        self.right_bar_tour_show_polygon_color = QtWidgets.QLabel('颜色透明度')  # transparent
        self.right_bar_tour_show_polygon_color.setObjectName("right_bar_tour_label")
        self.right_bar_tour_show_polygon_color_input = QtWidgets.QPushButton("")
        self.right_bar_tour_show_polygon_color_input.setStyleSheet(f"""background-color: rgba(255, 0, 0, 150); border-style: outset;border-radius: 5px;""")
        self.right_bar_tour_show_polygon_color_transparent_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)  # 滑块框栏
        self.right_bar_tour_show_polygon_color_transparent_slider.setMinimum(0)  # 设置最小值
        self.right_bar_tour_show_polygon_color_transparent_slider.setMaximum(255)  # 设置最大值
        self.right_bar_tour_show_polygon_color_transparent_slider.setSingleStep(1)  # 设置滑动步长
        self.right_bar_tour_show_polygon_color_transparent_slider.setValue(150)
        self.right_bar_tour_show_polygon_color_transparent_slider_holder_value = QtWidgets.QLabel("150")  # 提示文字

        self.right_bar_tour_show_polygon_time = QtWidgets.QLabel('时间')
        self.right_bar_tour_show_polygon_time.setObjectName("right_bar_tour_label")
        self.right_bar_widget_show_polygon_time_input = QtWidgets.QLineEdit()
        self.right_bar_widget_show_polygon_time_input.setText('3')
        self.right_bar_widget_show_polygon_time_input.setPlaceholderText("单个polygon时间")
        self.right_bar_widget_show_polygon_time_input.setObjectName('right_bar_widget_qlinedit_input')
        self.right_bar_widget_show_polygon_time_input_holder = QtWidgets.QLabel("单个polygon时间")  # 提示栏
        self.right_bar_widget_show_polygon_time_input_holder.setObjectName("right_bar_widget_holder")

        # 线路浏览 线路浏览 线路文件
        self.right_bar_tour_show_polygon_file_label = QtWidgets.QLabel('上传文件')                # transparent
        self.right_bar_tour_show_polygon_file_label.setObjectName("right_bar_tour_label")
        self.right_bar_tour_show_polygon_file = QtWidgets.QPushButton('点击上传')
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
        self.right_bar_polygon_show_layout.addWidget(self.right_bar_tour_show_polygon_type, 1, 0, 1, 1)
        self.right_bar_polygon_show_layout.addWidget(self.right_bar_tour_show_polygon_type_yes_button, 1, 1, 1, 2)
        self.right_bar_polygon_show_layout.addWidget(self.right_bar_tour_show_polygon_type_no_button, 1, 3, 1, 1)

        self.right_bar_polygon_show_layout.addWidget(self.right_bar_tour_show_polygon_color, 2, 0, 1, 1)
        self.right_bar_polygon_show_layout.addWidget(self.right_bar_tour_show_polygon_color_input, 2, 1, 1, 1)
        self.right_bar_polygon_show_layout.addWidget(self.right_bar_tour_show_polygon_color_transparent_slider, 2, 2, 1, 4)
        self.right_bar_polygon_show_layout.addWidget(self.right_bar_tour_show_polygon_color_transparent_slider_holder_value, 2, 6, 1, 6)

        self.right_bar_polygon_show_layout.addWidget(self.right_bar_tour_show_polygon_time, 3, 0, 1, 1)
        self.right_bar_polygon_show_layout.addWidget(self.right_bar_widget_show_polygon_time_input, 3, 1, 1, 2)
        self.right_bar_polygon_show_layout.addWidget(self.right_bar_widget_show_polygon_time_input_holder, 3, 3, 1, 6)

        self.right_bar_polygon_show_layout.addWidget(self.right_bar_tour_show_polygon_file_label, 4, 0, 1, 1)
        self.right_bar_polygon_show_layout.addWidget(self.right_bar_tour_show_polygon_file, 4, 1, 1, 2)  # 修改列索引为0
        self.right_bar_polygon_show_layout.addWidget(self.right_bar_tour_show_polygon_file_holder, 4, 3, 1, 2)  # 修改列索引为1，跨越列数为2
        self.right_bar_polygon_show_layout.addWidget(self.right_bar_tour_show_polygon_file_button_download, 6, 1, 1, 2)  # 修改列索引为3

        self.right_bar_tour_show_polygon_file.clicked.connect(self.right_bar_tour_show_polygon_file_slider_connect)
        self.right_bar_tour_show_polygon_file_button_download.clicked.connect(self.on_tour_show_polygon_push_button_clicked)
        self.right_bar_tour_show_polygon_color_transparent_slider.valueChanged.connect(self.right_bar_tour_show_polygon_color_transparent_slider_holder_connect)

        self.right_bar_tour_show_polygon_color.hide()  # 隐藏 "热门歌单" 标签
        self.right_bar_tour_show_polygon_color_input.hide()  # 隐藏热门歌单部件
        self.right_bar_tour_show_polygon_color_transparent_slider.hide()  # 隐藏 "热门歌单" 标签
        self.right_bar_tour_show_polygon_color_transparent_slider_holder_value.hide()  # 隐藏热门歌单部件

        self.setLayout(self.right_bar_polygon_show_layout)

    def right_bar_tour_show_polygon_color_transparent_slider_holder_connect(self):

        slider_transparent_value = self.right_bar_tour_show_polygon_color_transparent_slider.value()  # 获取当前滑块值
        self.right_bar_tour_show_polygon_color_transparent_slider_holder_value.setText('%s°' % slider_transparent_value)
        self.right_bar_tour_show_polygon_color_input.setStyleSheet(f"""background-color: rgba(255, 0, 0, {self.right_bar_tour_show_polygon_color_transparent_slider.value()}); border-style: outset;border-radius: 5px;""")

    def right_bar_tour_show_polygon_file_slider_connect(self):
        try:
            filename = QtWidgets.QFileDialog.getOpenFileNames(self, '选择图像', UPLOAD_PATH, "All Files(*);;Text Files(*.txt)")
            self.polygon_show_hide_file_name = filename[0][0].split('/')[-1]
            self.right_bar_tour_show_polygon_file_holder.setText(self.polygon_show_hide_file_name)
            self.right_bar_tour_show_polygon_filepath_coords = parser_polygon_show_hide_coords(filename[0][0])
        except Exception as e:
            traceback.print_exc()
            QtWidgets.QMessageBox.warning(self, "提示", "上传文件不正确!")

    def on_tour_show_polygon_push_button_clicked(self):

        try:
            selected_id = self.right_bar_tour_show_polygon_type_group_button.checkedId()
            kmlname = self.polygon_show_hide_file_name.split('.')[0]
            if selected_id == 1:
                TourPolygonShow(kmlname).tour_polygon_linear(
                    kmlname=kmlname if kmlname else '',
                    tour_time=float(self.right_bar_widget_show_polygon_time_input.text()),
                    polygon_coords=self.right_bar_tour_show_polygon_filepath_coords
                )
            elif selected_id == 0:
                TourPolygonHide(kmlname).tour_polygon_linear(
                    kmlname=kmlname if kmlname else '',
                    tour_time=float(self.right_bar_widget_show_polygon_time_input.text()),
                    polygon_coords=self.right_bar_tour_show_polygon_filepath_coords
                )

            QtWidgets.QMessageBox.information(self, "提示", "下载成功！")
        except Exception as e:
            import traceback
            traceback.print_exc()
            QtWidgets.QMessageBox.warning(self, "提示", "输入的数据有误!")