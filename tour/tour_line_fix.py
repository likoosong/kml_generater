# -*- coding: utf-8 -*-
from datetime import datetime

import simplekml
from simplekml import Kml, Snippet, Types, Style

from settings.constant import FILEPATH


from utlis.parser_line_coords import parser_line_coords

class TourLineFix(object):

    def __init__(self, kmlname):
        self.kml = Kml(name=kmlname, open=1)
        # 白色路线 样式
        self.route = Style()
        self.route.linestyle.color = 'ffdfdfdf'  # 白色
        self.route.linestyle.width = 3

        # 黄色路线 样式
        self.path = Style()
        self.path.labelstyle.scale = 0
        self.path.linestyle.color = 'ff0055ff'  # 黄色 ff0055ff 99ffac59
        self.path.linestyle.width = 1

        # 移动图标 样式
        self.dot = Style()  # dot
        self.dot.iconstyle.color = 'ff00d5ff'  # dot-s
        self.dot.iconstyle.scale = 0
        self.dot.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/shapes/shaded_dot.png"
        self.dot.labelstyle.scale = 0


    def tour_line_costom(self, kmlname, coords, tour_time=30):

        # 子项样式 设置列表项类型
        fol = self.kml.newfolder(name='data', open=1)
        fol.style.liststyle.listitemtype = simplekml.ListItemType.checkhidechildren  # 列表项是否展开
        fol.liststyle.bgcolor = '00ffffff'  # 背景颜色 00ffffff

        # 创建并设置-白的的底图
        ls = fol.newlinestring(name='route')
        ls.coords = coords
        ls.style = self.route
        ls.tessellate = 1          # 是否跟随地形

        # 创建并设置-白的的地图
        dot_pnt = self.kml.newpoint(name=f'image', coords=[coords[0]])  # dot
        dot_pnt.style = self.dot

        # 创建浏览对象
        tour = self.kml.newgxtour(name="play me")
        playlist = tour.newgxplaylist()
        delay_duration = 0

        # 每个坐标的时间
        duration = tour_time / len(coords)

        for idx, coord in enumerate(coords):
            print(coord)
            line = [coord, coord]
            d_ls = fol.newlinestring(name=f'path_{idx}')
            d_ls.coords = line
            d_ls.style = self.path
            d_ls.tessellate = 1
            if idx == 0:
                playlist.newgxwait(gxduration=2)

                # 更新  将移动小球显示出来
                animatedupdate = playlist.newgxanimatedupdate()  # dot_s     50dfdfdf
                animatedupdate.update.change = f"""
                    <IconStyle targetId="{self.dot.iconstyle.id}">
                            <scale>1</scale>
                        </IconStyle>
                    <LineStyle targetId="{self.route.linestyle.id}">
                            <color>50dfdfdf</color>
                    </LineStyle>
                """

                # animatedupdate = playlist.newgxanimatedupdate()  # o_route     50dfdfdf
                # animatedupdate.update.change = f"""
                #     <LineStyle targetId="{self.route.linestyle.id}">
                #         <color>50dfdfdf</color>
                #     </LineStyle>
                # """
                playlist.newgxwait(gxduration=1)
                animatedupdate = playlist.newgxanimatedupdate()  # path_w

                animatedupdate.update.change = f"""
                    <LineStyle targetId="{self.path.linestyle.id}">
                        <width>5</width>
                    </LineStyle>
                """
                playlist.newgxwait(gxduration=1)

            animatedupdate = playlist.newgxanimatedupdate()
            animatedupdate.gxduration = duration
            animatedupdate.gxdelayedstart = delay_duration

            if idx + 1 == len(coords):
                continue
            update_line = ','.join(coord) + ' ' + ','.join(coords[idx + 1])

            animatedupdate.update.change = f"""
                <LineString targetId="{d_ls.id}">
                    <coordinates>{update_line}</coordinates>
                </LineString>
                <IconStyle targetId="{d_ls.id}">
                    <coordinates>{update_line}</coordinates>
                </IconStyle>
            """

            image_pnt = ','.join(coords[idx + 1])

            animatedupdate = playlist.newgxanimatedupdate()
            animatedupdate.gxduration = duration
            animatedupdate.gxdelayedstart = delay_duration
            animatedupdate.update.change = f"""
                    <Point targetId="{dot_pnt.id}">
                        <coordinates>{image_pnt}</coordinates>
                    </Point>
            """
            delay_duration += duration

        playlist.newgxwait(gxduration=tour_time + 1)
        animatedupdate = playlist.newgxanimatedupdate()  # dot_s     50dfdfdf
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


if __name__ == '__main__':

    xml_name = '/Users/python/Desktop/maps/kmlname_generater/utlis/Route22.kml'
    coords = parser_line_coords(xml_name)
    kmlname = 'sss'

    TourLineFix().tour_line_costom(kmlname, coords, tour_time=30)




"""
倾斜角表示坐标系Z轴的值，也称为俯仰、高或垂直轴。方向角主要用术语“航向”表示。“方位角”。
俯仰角表示坐标系中Y轴的值。您也可以使用术语 pitch resp 而不是俯仰角。横轴。
滚动角 resp。倾斜角度表示坐标系中Y轴的值。在这种情况下，滚动角 resp。倾斜角也称为滚动、倾斜或纵轴。
"""











