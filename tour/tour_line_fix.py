# -*- coding: utf-8 -*-
from datetime import datetime

import simplekml
from simplekml import Kml, Snippet, Types, Style
from settings.constant import FILEPATH

'''
固定视角-线路的生长路线
1. 仅仅支持1条线路的变化
2. 默认的颜色为黄色
'''

class TourLineFixGenerator(object):

    def __init__(self, kmlname):
        # 创建一个 Kml 对象，指定地图名称为 kmlname，并设置默认展开状态
        self.kml = Kml(name=kmlname, open=1)

        # 白色路线样式
        self.route = Style()
        self.route.linestyle.color = 'ffdfdfdf'  # 白色
        self.route.linestyle.width = 3

        # 黄色路线样式
        self.path = Style()  # 创建一个 Style 对象用于定义路线样式
        self.path.labelstyle.scale = 0  # 不显示标签
        self.path.linestyle.color = 'ff0055ff'  # 路线的颜色为黄色（16进制表示） # 黄色 ff0055ff 99ffac59
        self.path.linestyle.width = 1  # 路线的宽度为1个单位

        # 移动图标样式
        self.dot = Style()  # dot
        self.dot.iconstyle.color = 'ff00d5ff'  # 移动图标的颜色（蓝色）
        self.dot.iconstyle.scale = 0  # 移动图标的缩放比例（0表示不显示图标）
        self.dot.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png"  # 移动图标的图像链接
        self.dot.labelstyle.scale = 0  # 移动图标标签的缩放比例（0表示不显示标签）

        # 创建一个 gx:Tour 对象，，用于定义地图浏览
        self.tour = self.kml.newgxtour(name="play me")
        # 在 gx:Tour 对象下创建 gx:Playlist 对象，用于存储浏览的动画序列
        self.playlist = self.tour.newgxplaylist()

    def update_move_point_icon_style(self, dot_pnt, next_coord, duration, delay_duration):
        """
        球形状坐标的移动
        :param dot_pnt:
        :param target_coord:
        :param duration:
        :param delay_duration:
        :return:
        """
        altitude = next_coord[2] if len(next_coord) == 3 else 0
        # 创建一个新的GXAnimatedUpdate对象 GXAnimatedUpdate对象用于在KML播放列表中插入带动画效果的更新
        animatedupdate = self.playlist.newgxanimatedupdate()

        # 设置动画的持续时间 'gxduration'属性用于定义动画效果的持续时间，以秒为单位
        animatedupdate.gxduration = duration

        # 设置动画的延迟开始时间 'gxdelayedstart'属性用于定义动画效果开始前的延迟时间，以秒为单位
        animatedupdate.gxdelayedstart = delay_duration

        # 仅支持 单个点的坐标
        animatedupdate.update.change = f"""
                      <Point targetId="{dot_pnt.id}">
                          <coordinates>{next_coord[0]},{next_coord[1]},{altitude}</coordinates>
                      </Point>
              """
        # 支持Placemark的所有信息
        # animatedupdate.update.change = f"""
        #     <Placemark targetId="{dot_pnt.placemark.id}">
        #         <Point>
        #             <coordinates>{target_coord[0]},{target_coord[1]},{altitude}</coordinates>
        #         </Point>
        #     </Placemark>
        # """

    def animate_start_change_style(self):
        # 在动画中插入一个等待时长为1秒的暂停
        self.playlist.newgxwait(gxduration=2)

        # 更新动画：将移动的小球（标记）显示出来
        # IconStyle 指定要修改的IconStyle的ID  设置图标的缩放比例为1，使其显示在地图上
        # LineStyle 指定要修改的LineStyle的ID  修改线的颜色为50dfdfdf
        animatedupdate = self.playlist.newgxanimatedupdate()  # dot_s     50dfdfdf
        animatedupdate.update.change = f"""
                <IconStyle targetId="{self.dot.iconstyle.id}">
                        <scale>1</scale> 
                    </IconStyle>
                <LineStyle targetId="{self.route.linestyle.id}">
                        <color>50dfdfdf</color>
                </LineStyle>
            """

        # 在动画中插入一个等待时长为1秒的暂停
        self.playlist.newgxwait(gxduration=1)

        # 更新动画：改变名为self.path的线的宽度  指定要修改的LineStyle的ID   修改线的宽度为5
        animatedupdate = self.playlist.newgxanimatedupdate()  # path_w
        animatedupdate.update.change = f"""
                <LineStyle targetId="{self.path.linestyle.id}">   
                    <width>5</width>                        
                </LineStyle>
            """
        self.playlist.newgxwait(gxduration=1)

    def update_line_color_style(self, d_ls, coord, next_coord, duration, delay_duration):
        """
        播放过程中修改线段的颜色
        :param d_ls:
        :param coord:
        :param next_coord:
        :param duration:
        :param delay_duration:
        :return:
        """
        animatedupdate = self.playlist.newgxanimatedupdate()
        animatedupdate.gxduration = duration
        animatedupdate.gxdelayedstart = delay_duration
        alt1 = coord[2] if len(coord) == 3 else 0
        alt2 = next_coord[2] if len(next_coord) == 3 else 0
        coordinates = f"{coord[0]},{coord[1]},{alt1} {next_coord[0]},{next_coord[1]},{alt2}"

        animatedupdate.update.change = f"""
                <LineString targetId="{d_ls.id}">
                    <coordinates>{coordinates}</coordinates>
                </LineString>
            """  # <IconStyle targetId="{d_ls.id}"><coordinates>{update_line}</coordinates></IconStyle>

    def tour_generator(self, kmlname, tour_time, coordinates):
        # 创建一个文件夹（子项样式设置） 创建一个名为 'data' 的文件夹，初始时展开
        fol = self.kml.newfolder(name='data', open=1)

        # 设置列表项类型为 checkhidechildren 设置列表项类型，可以控制列表项前面的图标，checkhidechildren 表示可勾选，点击时隐藏子项
        fol.style.liststyle.listitemtype = simplekml.ListItemType.checkhidechildren
        fol.liststyle.bgcolor = '00ffffff'  # 设置背景颜色为透明白色（16进制表示）

        # 创建并设置白色底图
        ls = fol.newlinestring(name='route')  # 创建一个新的 LineString 对象，表示路线
        ls.coords = coordinates  # 设置 LineString 对象的坐标，即路线的经纬度点
        ls.style = self.route  # 设置 LineString 对象的样式为白色路线样式
        ls.tessellate = 1  # 设置 LineString 对象是否跟随地形进行渲染，1 表示跟随地形

        # 创建并设置白色地图
        dot_pnt = self.kml.newpoint(name=f'image', coords=[coordinates[0]])  # 创建一个新的 Point 对象，表示地图上的点
        dot_pnt.style = self.dot  # 设置 Point 对象的样式为移动图标样式

        # 初始化延迟启动时间为0
        delay_duration = 0
        # 计算每个坐标点的时间间隔 将总浏览时间除以坐标点数量，得到每个坐标点的时间间隔
        duration = tour_time / len(coordinates)

        # 开始包播放相机时，修改样式播放的初始化
        self.animate_start_change_style()

        for idx, coord in enumerate(coordinates[:-1]):
            line = [coord, coord]
            d_ls = fol.newlinestring(name=f'path_{idx}')
            d_ls.coords = line
            d_ls.style = self.path
            d_ls.tessellate = 1

            next_coord = coordinates[idx + 1]

            # 线段颜色的变化
            self.update_line_color_style(d_ls, coord, next_coord, duration, delay_duration)

            # 球形坐标的移动
            self.update_move_point_icon_style(dot_pnt, next_coord, duration, delay_duration)
            delay_duration += duration

        self.playlist.newgxwait(gxduration=tour_time + 1)
        animatedupdate = self.playlist.newgxanimatedupdate()  # dot_s     50dfdfdf
        animatedupdate.update.change = f"""
            <IconStyle targetId="{self.dot.iconstyle.id}">
                    <scale>0</scale>
                    <href></href>
                </IconStyle>
                <LineString targetId="{self.dot.labelstyle.id}">
                    <scale>0</scale>
                </LineString>
            """
        wono = datetime.now().strftime('%Y%m%d%H%M%S')
        self.kml.save(f"{FILEPATH}{wono}{kmlname}.kml")

    def run(self):
        kmlname = 'xxxxxxxx'
        tour_time = 30
        # coordinates = [coordinates for item in aaaa for coordinates in item.values()]
        # print(coordinates)
        # self.tour_generator(kmlname, tour_time, coordinates)


if __name__ == '__main__':
    yy = TourLineFixGenerator('台风')
    yy.run()











