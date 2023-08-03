import traceback

import requests
from PyQt5.QtCore import QThread, pyqtSignal

from tour.tour_line_fix import TourLineFix
from tour.tour_line_arount import TourLineArount
from tour.tour_line_follow import TourLineFollow
from tour.tour_line_follow_mode import TourLineFollowMode
from tour.tour_polygon import TourPolygon
from settings.model import LuckyAreas

class ThreadLine(QThread):    # 建立一个任务线程类
    signal = pyqtSignal(bool) #设置触发信号传递的参数数据类型,这里是字符串
    def __init__(self, kmlname, tour_type, tour_time, length, distance, coords, is_mode=False):
        super(ThreadLine, self).__init__()
        self.kmlname = kmlname
        self.is_mode = is_mode
        self.tour_type = tour_type
        self.tour_time = tour_time
        self.coords = coords
        self.length = length
        self.distance = distance

    def run(self): # 在启动线程后任务从这个函数里面开始执行

        try:
            self.download_tour_line()
            self.signal.emit(True) #任务线程发射信号用于与图形化界面进行交互
        except Exception as e:
            self.signal.emit(False) #任务线程发射信号用于与图形化界面进行交互

    def download_tour_line(self):
        """
        :param kmlname: 文件名
        :param tour_type: 浏览方式 生长路线-固定视角 生长路线-环绕视角 生长路线-跟随视角 节段路线-环绕视角 节段路线-跟随视角
        :param tour_time: 浏览时间
        :param coords: 坐标集合
        :return:
        """
        if self.tour_type == "生长路线-固定视角":  # 生长路线-固定视角
            TourLineFix(self.kmlname).tour_line_costom(self.kmlname, self.coords, tour_time=self.tour_time)
        elif self.tour_type == "生长路线-环绕视角":  # 生长路线-固定视角
            TourLineArount(self.kmlname).tour_line_arount(
                self.kmlname, self.coords,
                length=self.length,
                distance= self.distance,
                tour_time=self.tour_time
            )
        elif self.tour_type == "生长路线-跟随视角" and self.is_mode is True:  # 生长路线-固定视角
            TourLineFollowMode(self.kmlname).tour_line_follow(
                self.kmlname,
                coords=self.coords,
                length=self.length*1,
                distance=self.distance,
                tour_time=self.tour_time
            )
            print(f'+++++++++++++++++++++++++{len(self.coords)}')
        elif self.tour_type == "生长路线-跟随视角":
            print('==============================================================')
            TourLineFollow(self.kmlname).tour_line_follow(
                self.kmlname, self.coords,
                length=self.length,
                distance= self.distance,
                tour_time=self.tour_time
            )


class ThreadPolygon(QThread):    # 建立一个任务线程类
    signal = pyqtSignal(bool) #设置触发信号传递的参数数据类型,这里是字符串
    def __init__(self, country, province, city, town, children, color):
        super(ThreadPolygon, self).__init__()
        self.country = country
        self.province = province
        self.city = city
        self.town = town
        self.children = children
        self.color = color

    def run(self): # 在启动线程后任务从这个函数里面开始执行

        try:
            self.download_tour_polygon()
            self.signal.emit(True) #任务线程发射信号用于与图形化界面进行交互
        except Exception as e:
            traceback.print_exc()
            self.signal.emit(False) #任务线程发射信号用于与图形化界面进行交互

    def download_tour_polygon(self):
        """
        :param kmlname: 文件名
        :param tour_type: 浏览方式 生长路线-固定视角 生长路线-环绕视角 生长路线-跟随视角 节段路线-环绕视角 节段路线-跟随视角
        :param tour_time: 浏览时间
        :param coords: 坐标集合
        :return:
        """

        kmlname = self.country

        if self.province != '请选择':
            kmlname = self.province

        if self.city != '请选择':
            kmlname = self.city

        if self.town != '请选择':
            kmlname = self.town

        print(kmlname,'children',  self.children, 'color', self.color)

        area = LuckyAreas.get(area_name=kmlname)
        tour = TourPolygon()
        if self.province == '请选择' and self.color == 0:
            print("没有填充的中国边界包含省界(页面不点击 全部是请选择)")
            url = 'https://geo.datav.aliyun.com/areas_v3/bound/100000_boundary.json'
            boundary = requests.get(url).json()
            tour.china_polygon_boundary(kmlname, boundary, children=self.children)
        # elif (self.children == 0 and level == 'district') or (self.town != '请选择' and area.level == 'district') or (self.children == 1 and area.level == 'district'):
        elif self.children == 0:
            print("不包含子区域或者没有子区域  即单个地区的kml ")
            url = f'https://geo.datav.aliyun.com/areas_v3/bound/{area.adcode}.json'  # 141081
            boundary = requests.get(url).json()
            TourPolygon().china_single_polygon(kmlname, boundary, color=self.color)
        elif self.children == 1:
            # 生成包含自取的kml 即多个地区的kml
            url = f'https://geo.datav.aliyun.com/areas_v3/bound/{area.adcode}_full.json'
            boundary = requests.get(url).json()
            tour.china_full_polygon(kmlname, boundary, color=self.color)
