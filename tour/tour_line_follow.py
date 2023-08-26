# -*- coding: utf-8 -*-
from datetime import datetime

import simplekml
from simplekml import Kml, Snippet, Types, Style

from settings.constant import FILEPATH
from utlis.parser_line_coords import parser_line_coords, location_great_circle


class TourLineFollow(object):

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

        self.tour = self.kml.newgxtour(name="play me")
        self.playlist = self.tour.newgxplaylist()

    def tour_line_follow_play(self, kmlname, coords, length=0, distance=0, tour_time=30):

        point_idx = int(length / 18)  # 划分段
        fly_duration = tour_time / 16           # 单位飞行时间

        for idx, coord in enumerate(coords):
            longitude, latitude, altitude = coord
            if point_idx * 2 == idx:  # 第三次
                flyto = self.playlist.newgxflyto(gxduration=fly_duration * 2)
                flyto.gxflytomode = 'smooth'
                flyto.lookat.longitude = longitude
                flyto.lookat.latitude = latitude
                flyto.lookat.altitude = 0
                flyto.lookat.tilt = 45
                flyto.lookat.heading = 0
                flyto.lookat.range = distance / 3
                # flyto.lookat.AltitudeMode = 'relativeToGround'

            if point_idx * 3 == idx:
                flyto = self.playlist.newgxflyto(gxduration=fly_duration * 1)
                flyto.gxflytomode = 'smooth'
                flyto.lookat.longitude = longitude
                flyto.lookat.latitude = latitude
                flyto.lookat.altitude = 0
                flyto.lookat.tilt = 45
                flyto.lookat.heading = 0
                flyto.lookat.range = distance / 3
                # flyto.lookat.AltitudeMode = 'relativeToGround'

            if point_idx * 5 == idx:
                flyto = self.playlist.newgxflyto(gxduration=fly_duration * 2)
                flyto.gxflytomode = 'smooth'
                flyto.lookat.longitude = longitude
                flyto.lookat.latitude = latitude
                flyto.lookat.altitude = 0
                flyto.lookat.tilt = 45
                flyto.lookat.heading = 0
                flyto.lookat.range = distance / 3
                # flyto.lookat.AltitudeMode = 'relativeToGround'

            if point_idx * 9 == idx:
                flyto = self.playlist.newgxflyto(gxduration=fly_duration * 4)
                flyto.gxflytomode = 'smooth'
                flyto.lookat.longitude = longitude
                flyto.lookat.latitude = latitude
                flyto.lookat.altitude = 0
                flyto.lookat.tilt = 45
                flyto.lookat.heading = 0
                flyto.lookat.range = distance / 3
                # flyto.lookat.AltitudeMode = 'relativeToGround'

            if point_idx * 13 == idx:
                flyto = self.playlist.newgxflyto(gxduration=fly_duration * 4)
                flyto.gxflytomode = 'smooth'
                flyto.lookat.longitude = longitude
                flyto.lookat.latitude = latitude
                flyto.lookat.altitude = 0
                flyto.lookat.tilt = 45
                flyto.lookat.heading = 0
                flyto.lookat.range = distance / 3
                # flyto.lookat.AltitudeMode = 'relativeToGround'

            if point_idx * 15 == idx:
                flyto = self.playlist.newgxflyto(gxduration=fly_duration * 2)
                flyto.gxflytomode = 'smooth'
                flyto.lookat.longitude = longitude
                flyto.lookat.latitude = latitude
                flyto.lookat.altitude = 0
                flyto.lookat.tilt = 45
                flyto.lookat.heading = 0
                flyto.lookat.range = distance / 3
                # flyto.lookat.AltitudeMode = 'relativeToGround'

            if point_idx * 17 == idx:
                flyto = self.playlist.newgxflyto(gxduration=fly_duration)
                flyto.gxflytomode = 'smooth'
                flyto.lookat.longitude = longitude
                flyto.lookat.latitude = latitude
                flyto.lookat.altitude = 0
                flyto.lookat.tilt = 45
                flyto.lookat.heading = 0
                flyto.lookat.range = distance / 3
                # flyto.lookat.AltitudeMode = 'relativeToGround'

            if point_idx * 18 == idx:
                flyto = self.playlist.newgxflyto(gxduration=fly_duration * 2)
                flyto.gxflytomode = 'smooth'
                flyto.lookat.longitude = longitude
                flyto.lookat.latitude = latitude
                flyto.lookat.altitude = 0
                flyto.lookat.tilt = 45
                flyto.lookat.heading = 0
                flyto.lookat.range = distance / 3
                # flyto.lookat.AltitudeMode = 'relativeToGround'
                self.playlist.newgxwait(gxduration=1)
                flyto = self.playlist.newgxflyto(gxduration=3)
                flyto.gxflytomode = 'smooth'
                flyto.lookat.longitude = coords[int(length // 1.7)][0]  # center_lon
                flyto.lookat.latitude = coords[int(length // 1.7)][1]  # center_lat
                flyto.lookat.altitude = 0
                flyto.lookat.tilt = 45
                flyto.lookat.heading = 0
                flyto.lookat.range = (distance / 2) * 2.5

    def tour_line_follow_change(self, kmlname, coords, length=0, distance=0, tour_time=30):

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

        delay_duration = 0                      # 坐标移动时间
        duration = tour_time / length           # 平均坐标移动时间

        look_pnt_longitude = coords[int(length // 1.7)][0]
        look_pnt_latitude = coords[int(length // 1.7)][1]
        look_pnt_range = (distance / 2) * 2.5

        pnt = fol.newpoint(name="", coords=[(look_pnt_longitude, look_pnt_latitude)])
        pnt.iconstyle.icon.href = ''
        pnt.lookat = simplekml.LookAt(
            gxaltitudemode=simplekml.GxAltitudeMode.relativetoseafloor,
            latitude=look_pnt_longitude,
            longitude=look_pnt_latitude,
            range=look_pnt_range,
            heading=0,
            tilt=45
        )
        for idx, coord in enumerate(coords):
            line = [coord, coord]
            longitude, latitude, altitude = coord
            d_ls = fol.newlinestring(name=f'path_{idx}')
            d_ls.coords = line
            d_ls.style = self.path
            d_ls.tessellate = 1
            if idx == 0:
                self.playlist.newgxwait(gxduration=2.5)
                animatedupdate = self.playlist.newgxanimatedupdate()  # dot_s     50dfdfdf
                animatedupdate.update.change = f"""
                    <IconStyle targetId="{self.dot.iconstyle.id}">
                        <scale>1</scale>
                    </IconStyle>
                    <LineStyle targetId="{self.route.linestyle.id}">
                        <color>50dfdfdf</color>
                    </LineStyle>
                """

                flyto = self.playlist.newgxflyto(gxduration=1.5)
                flyto.gxflytomode = 'smooth'
                flyto.lookat.longitude = longitude
                flyto.lookat.latitude = latitude
                flyto.lookat.altitude = 0
                flyto.lookat.heading = 0
                flyto.lookat.tilt = 60
                flyto.lookat.range = distance / 3
                flyto.lookat.AltitudeMode = 'relativeToGround'

                animatedupdate = self.playlist.newgxanimatedupdate(gxduration=1.5)  # path_w
                animatedupdate.update.change = f"""
                    <LineStyle targetId="{self.path.linestyle.id}">
                        <width>5</width>
                    </LineStyle>
                """
                self.playlist.newgxwait(gxduration=1)

            animatedupdate = self.playlist.newgxanimatedupdate(gxduration=0.1)
            animatedupdate.gxduration = duration
            animatedupdate.gxdelayedstart = delay_duration

            if idx + 1 == length:
                animatedupdate.update.change = f"""
                <IconStyle targetId="{self.dot.iconstyle.id}">
                        <scale>0</scale>
                        <href></href>
                    </IconStyle>
                    <LineString targetId="{self.dot.labelstyle.id}">
                        <scale>0</scale>
                    </LineString>
                """
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
            animatedupdate = self.playlist.newgxanimatedupdate(gxduration=0.1)
            animatedupdate.gxduration = duration
            animatedupdate.gxdelayedstart = delay_duration
            animatedupdate.update.change = f"""
                    <Point targetId="{dot_pnt.id}">
                        <coordinates>{image_pnt}</coordinates>
                    </Point>
            """
            delay_duration += duration


    def tour_line_follow(self, kmlname, coords, length=0, distance=0, tour_time=30):
        self.tour_line_follow_change(kmlname, coords, length, distance, tour_time)
        self.tour_line_follow_play(kmlname, coords, length, distance, tour_time)
        wono = datetime.now().strftime('%Y%m%d%H%M%S')
        self.kml.save(f"{FILEPATH}{wono}{kmlname}.kml")


if __name__ == '__main__':

    xml_name = '/Users/python/Desktop/maps/kmlname_generater/utlis/北京-天津.xml'
    coords = parser_line_coords(xml_name)
    kmlname = 'sss'


    length = len(coords)

    distance = 0
    for idx, coord in enumerate(coords):
        if length == idx +1:
            continue
        start_latitude, start_longitude, start_altitude = coord
        end_latitude, end_longitude, end_altitude = coords[idx+1]
        start = [start_longitude, start_latitude]
        end = [end_longitude, end_latitude]
        dte = location_great_circle(start, end)
        distance += dte

    # TourLineFollow(kmlname).tour_line_follow(kmlname, coords, length=length, distance=distance, tour_time=30)

    TourLineArrount(kmlname).tour_line_follow(kmlname, coords, length=length, distance=distance, tour_time=30)



