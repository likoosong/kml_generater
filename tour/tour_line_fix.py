# -*- coding: utf-8 -*-
from datetime import datetime

import simplekml
from simplekml import Kml, Snippet, Types, Style

from settings.constant import FILEPATH


from utlis.parser_line_coords import parser_line_coords

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
        animatedupdate = self.playlist.newgxanimatedupdate()  # dot_s     50dfdfdf
        animatedupdate.update.change = f"""
                <IconStyle targetId="{self.dot.iconstyle.id}">    # 指定要修改的IconStyle的ID
                        <scale>1</scale>                          # 设置图标的缩放比例为1，使其显示在地图上
                    </IconStyle>
                <LineStyle targetId="{self.route.linestyle.id}">  # 指定要修改的LineStyle的ID
                        <color>50dfdfdf</color>                   # # 修改线的颜色为50dfdfdf
                </LineStyle>
            """

        # 在动画中插入一个等待时长为1秒的暂停
        self.playlist.newgxwait(gxduration=1)

        # 更新动画：改变名为self.path的线的宽度
        animatedupdate = self.playlist.newgxanimatedupdate()  # path_w
        animatedupdate.update.change = f"""
                <LineStyle targetId="{self.path.linestyle.id}">   # 指定要修改的LineStyle的ID
                    <width>5</width>                              # 修改线的宽度为5
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
        # aaaa = [{'202307210800': [132.8, 13.9]}, {'202307211400': [132.7, 13.9]}, {'202307211700': [132.7, 13.9]},
        #         {'202307212000': [132.5, 13.9]}, {'202307220200': [132.2, 14]}, {'202307220500': [132.2, 14.1]},
        #         {'202307220800': [131.8, 14.2]}, {'202307221400': [130.7, 14.4]}, {'202307221700': [130.5, 14.4]},
        #         {'202307222000': [130.4, 14.4]}, {'202307222300': [130.1, 14.5]}, {'202307230200': [129.9, 14.6]},
        #         {'202307230500': [129.5, 14.7]}, {'202307230800': [128.8, 14.8]}, {'202307231100': [128.5, 14.8]},
        #         {'202307231400': [128.2, 14.8]}, {'202307231700': [128, 14.8]}, {'202307232000': [127.8, 15]},
        #         {'202307232300': [127.4, 15.2]}, {'202307240200': [127.1, 15.2]}, {'202307240500': [127, 15.4]},
        #         {'202307240800': [126.6, 15.4]}, {'202307241100': [126.5, 15.5]}, {'202307241400': [126.3, 15.7]},
        #         {'202307241700': [126.1, 16.2]}, {'202307242000': [125.8, 16.5]}, {'202307242300': [125.3, 16.7]},
        #         {'202307250200': [125.1, 16.9]}, {'202307250500': [124.9, 17.2]}, {'202307250800': [124.6, 17.6]},
        #         {'202307251100': [124, 18]}, {'202307251400': [123.8, 18.2]}, {'202307251700': [123.3, 18.6]},
        #         {'202307252000': [122.8, 18.8]}, {'202307252300': [122.2, 18.9]}, {'202307260200': [121.6, 19]},
        #         {'202307260500': [121.3, 18.8]}, {'202307260800': [121.3, 18.8]}, {'202307261100': [121.1, 19]},
        #         {'202307261400': [121, 19.3]}, {'202307261500': [120.9, 19.4]}, {'202307261600': [120.8, 19.4]},
        #         {'202307261700': [120.7, 19.4]}, {'202307261800': [120.6, 19.4]}, {'202307261900': [120.6, 19.5]},
        #         {'202307262000': [120.6, 19.6]}, {'202307262100': [120.6, 19.7]}, {'202307262200': [120.6, 19.8]},
        #         {'202307262300': [120.4, 19.9]}, {'202307270000': [120.3, 20]}, {'202307270100': [120.1, 20]},
        #         {'202307270200': [120, 20]}, {'202307270300': [120, 20]}, {'202307270400': [120, 20.1]},
        #         {'202307270500': [120, 20.1]}, {'202307270600': [120, 20.1]}, {'202307270700': [120, 20.2]},
        #         {'202307270800': [119.9, 20.5]}, {'202307270900': [119.8, 20.7]}, {'202307271000': [119.7, 20.8]},
        #         {'202307271100': [119.5, 20.9]}, {'202307271200': [119.3, 20.9]}, {'202307271300': [119.3, 21]},
        #         {'202307271400': [119.3, 21.1]}, {'202307271500': [119.3, 21.2]}, {'202307271600': [119.3, 21.3]},
        #         {'202307271700': [119.2, 21.4]}, {'202307271800': [119.2, 21.5]}, {'202307271900': [119.2, 21.6]},
        #         {'202307272000': [119.2, 21.7]}, {'202307272100': [119.1, 21.9]}, {'202307272200': [119.1, 22]},
        #         {'202307272300': [119.1, 22.2]}, {'202307280000': [119.1, 22.4]}, {'202307280100': [119, 22.6]},
        #         {'202307280200': [119, 22.8]}, {'202307280300': [119, 23]}, {'202307280400': [119, 23.2]},
        #         {'202307280500': [118.9, 23.4]}, {'202307280600': [118.9, 23.6]}, {'202307280700': [118.9, 23.9]},
        #         {'202307280800': [118.8, 24.1]}, {'202307280900': [118.7, 24.3]}, {'202307281000': [118.6, 24.7]},
        #         {'202307281100': [118.5, 24.9]}, {'202307281200': [118.4, 25]}, {'202307281300': [118.3, 25.4]},
        #         {'202307281400': [118.1, 25.5]}, {'202307281500': [118, 25.8]}, {'202307281600': [117.9, 26]},
        #         {'202307281700': [117.9, 26.2]}, {'202307281800': [117.8, 26.4]}, {'202307281900': [117.7, 26.7]},
        #         {'202307282000': [117.4, 27]}, {'202307282100': [117.3, 27.1]}, {'202307282200': [117, 27.4]},
        #         {'202307282300': [116.9, 27.6]}, {'202307290000': [116.9, 28.1]}, {'202307290100': [117.2, 28.2]},
        #         {'202307290200': [117.2, 28.5]}, {'202307290300': [117.2, 28.8]}, {'202307290400': [117.1, 29.1]},
        #         {'202307290500': [116.7, 29.3]}, {'202307290600': [116.6, 29.8]}, {'202307290700': [116.6, 29.9]},
        #         {'202307290800': [116.5, 30]}]
        # coordinates = [coordinates for item in aaaa for coordinates in item.values()]
        # print(coordinates)
        # self.tour_generator(kmlname, tour_time, coordinates)


if __name__ == '__main__':
    yy = TourLineFixGenerator('台风')
    yy.run()

"""
倾斜角表示坐标系Z轴的值，也称为俯仰、高或垂直轴。方向角主要用术语“航向”表示。“方位角”。
俯仰角表示坐标系中Y轴的值。您也可以使用术语 pitch resp 而不是俯仰角。横轴。
滚动角 resp。倾斜角度表示坐标系中Y轴的值。在这种情况下，滚动角 resp。倾斜角也称为滚动、倾斜或纵轴。
"""











