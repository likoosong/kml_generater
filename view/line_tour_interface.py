import traceback
from PyQt5 import QtCore, QtGui, QtWidgets

from settings.constant import UPLOAD_PATH, EXPIRED_DATE, EXPIRED_WARN
from utlis.my_thread import ThreadLine, ThreadPolygon
from utlis.parser_line_coords import parser_line_coords, parser_line_distance, parser_polygon_coords

class LineTourView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
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
        self.right_bar_widget_line_tour_type_input.addItems(
            ["生长路线-固定视角", "生长路线-环绕视角", "生长路线-跟随视角"])  # "节段路线-环绕视角", "节段路线-跟随视角"
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
        self.right_bar_line_layout.addWidget(self.right_bar_tour_line_flag, 2, 0, 4, 1)  # 图片模型
        self.right_bar_line_layout.addWidget(self.right_bar_tour_line_flag_no_button, 2, 1, 4, 3)  # 模型
        self.right_bar_line_layout.addWidget(self.right_bar_tour_line_flag_yes_button, 2, 2, 4, 3)  # 图片
        self.right_bar_line_layout.addWidget(self.right_bar_tour_line_tour_time, 3, 0, 4, 1)  # 线路浏览 时间 文字
        self.right_bar_line_layout.addWidget(self.right_bar_widget_line_tour_time_input, 3, 1, 4, 3)  # 线路浏览 时间 输入框
        self.right_bar_line_layout.addWidget(self.right_bar_widget_line_tour_time_input_holder, 3, 4, 4,
                                             3)  # 线路浏览 时间 提示文字

        self.right_bar_line_layout.addWidget(self.right_bar_tour_line_file, 4, 1, 4, 1)  # 线路浏览 上传文件 输入框
        self.right_bar_line_layout.addWidget(self.right_bar_tour_line_file_holder, 4, 2, 4, 2)  # 线路浏览 上传文件 提示文字
        self.right_bar_line_layout.addWidget(self.right_bar_tour_line_file_button_download, 5, 1, 4,
                                             3)  # 线路浏览 上传文件 下载按钮
        self.right_bar_line_layout.addWidget(self.right_bar_widget_line_file_placeholder, 10, 2, 4, 3)  # 线路浏览 上传文件 占位符

        self.right_bar_tour_line_file.clicked.connect(self.right_bar_tour_line_file_slider_connect)
        self.right_bar_tour_line_file_button_download.clicked.connect(self.on_tour_line_file_push_button_clicked)

        self.setLayout(self.right_bar_line_layout)

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

    def right_bar_tour_line_download_success(self, status):
        if status:
            QtWidgets.QMessageBox.information(self, "提示", "下载成功！")
        else:
            QtWidgets.QMessageBox.warning(self, "提示", "下载失败！")
        self.right_bar_tour_line_file_button_download.setEnabled(True)  # 按钮可点击
