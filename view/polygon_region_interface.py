from PyQt5 import QtCore, QtGui, QtWidgets

from settings.model import LuckyAreas
from utlis.my_thread import ThreadLine, ThreadPolygon

class PolygonRegionView(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
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

        self.right_bar_widget_polygon_province_input.activated.connect(self.on_tour_province_city_button_clicked)
        self.right_bar_widget_polygon_city_input.activated.connect(self.on_tour_city_town_button_clicked)
        self.right_bar_widget_polygon_button_download.clicked.connect(self.on_tour_polygon_push_button_clicked)

        self.setLayout(self.right_bar_polygon_layout)

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

