# -*- coding: utf-8 -*-
from datetime import datetime

import simplekml
from simplekml import Kml, Snippet, Types, Style
from simplekml import Kml, Model, AltitudeMode, Orientation, Scale

from settings.constant import FILEPATH
from utlis.parser_line_coords import parser_line_coords, location_great_circle


class TourLineFollowMode(object):

    def __init__(self, kmlname):
        self.kml = Kml(name=kmlname, open=1)
        # 白色路线 样式
        self.route = Style()
        self.route.linestyle.color = '50dfdfdf'  # 白色
        self.route.linestyle.width = 2

        # 黄色路线 样式
        self.path = Style()
        self.path.labelstyle.scale = 0
        self.path.linestyle.color = 'ff0055ff'  # 黄色 ff0055ff 99ffac59
        self.path.linestyle.width = 3

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
        '''
        simplekml.Orientation( heading=0 , tilt=0 , roll=0 )
            描述 3D 模型坐标系的旋转。
            heading 绕 z 轴旋转，接受浮动。
            roll    绕 y 轴旋转，接受浮点数。
            tilt    绕 x 轴旋转，接受浮点数。
        simplekml.Scale( x=1 , y=1 , z=1 )
            在模型的坐标空间中沿 x、y 和 z 轴缩放模型
            x在 x 方向缩放，接受浮动。
            y在 y 方向缩放，接受浮动。
            z在 z 方向缩放，接受浮动。
        '''

        first_lon, first_lat, first_alt = coords[0]
        model_car = self.kml.newmodel(name='car')
        model_car.link.href = 'mode/car.dae'
        model_car.altitudemode = simplekml.GxAltitudeMode.relativetoseafloor
        model_car.orientation = simplekml.Orientation(heading=0, tilt=0, roll=0)
        model_car.scale = simplekml.Scale(x=66.91844611301006, y=66.91534601247388, z=66.91689606274197)
        model_car.location = simplekml.Location(longitude=float(first_lon), latitude=float(first_lat), altitude=float(first_alt))


        # 子项样式 设置列表项类型
        fol = self.kml.newfolder(name='data', open=1)
        fol.style.liststyle.listitemtype = simplekml.ListItemType.checkhidechildren  # 列表项是否展开
        fol.liststyle.bgcolor = '00ffffff'  # 背景颜色 00ffffff

        # 创建并设置-白的的底图
        ls = fol.newlinestring(name='route')
        ls.coords = coords
        ls.style = self.route
        ls.tessellate = 1                       # 是否跟随地形

        delay_duration = 0  #  坐标移动时间
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
        for idx, coord in enumerate(coords[0:-1]):
            line = [coord, coord]
            longitude, latitude, altitude = coord
            d_ls = fol.newlinestring(name=f'path_{idx}')
            d_ls.coords = line
            d_ls.style = self.path
            d_ls.tessellate = 1

            update_line = ','.join(coord) + ' ' + ','.join(coords[idx + 1])
            animatedupdate = self.playlist.newgxanimatedupdate(gxduration=0.1)
            animatedupdate.gxduration = duration
            animatedupdate.gxdelayedstart = delay_duration
            animatedupdate.update.change = f"""
                <LineString targetId="{d_ls.id}">
                    <coordinates>{update_line}</coordinates>
                </LineString>
                <Placemark targetId="{int(model_car.id) + 1}">
                    <Model>
                        <Location>
                            <longitude>{coord[0]}</longitude>
                            <latitude>{coord[1]}</latitude>
                        </Location>
                    </Model>
                </Placemark>
            # """
            delay_duration += duration

    def tour_line_follow(self, kmlname, coords, length=0, distance=0, tour_time=30):
        self.tour_line_follow_change(kmlname, coords, length, distance, tour_time)
        self.tour_line_follow_play(kmlname, coords, length, distance, tour_time)
        wono = datetime.now().strftime('%Y%m%d%H%M%S')
        self.kml.save(f"{FILEPATH}{wono}{kmlname}.kml")


if __name__ == '__main__':

    xml_name = 'Route.xml'
    coords = parser_line_coords(xml_name)
    kmlname = '模型运动测试'

    length = len(coords)

    distance = 0
    for idx, coord in enumerate(coords):
        if length == idx +1:
            continue
        start_latitude, start_longitude, start_altitude = coord
        end_latitude, end_longitude, end_altitude = coords[idx+1]
        start = [start_longitude, start_latitude]
        # end = [end_longitude, end_latitude]
        # dte = location_great_circle(start, end)
        # distance += dte

    # TourLineFollow(kmlname).tour_line_follow(kmlname, coords, length=length, distance=distance, tour_time=30)

    TourLineFollowMode(kmlname).tour_line_follow(kmlname, coords, length=length, distance=distance, tour_time=30)



'''
<Placemark id="166447">
    <name>car</name>
    <styleUrl>#default</styleUrl>
    <Model id="166446">
        <gx:altitudeMode>relativeToSeaFloor</gx:altitudeMode>
        <Location>
            <longitude>116.4049374014361</longitude>
            <latitude>39.90089847603129</latitude>
            <altitude>0</altitude>
        </Location>
        <Orientation>                        模型上的旋转，接受simplekml.Orientation
            <heading>0</heading>
            <tilt>0</tilt>
            <roll>0</roll>
        </Orientation>
        <Scale>
            <x>66.91844611301006</x>       模型的规模，接受simplekml.Scale
            <y>66.91534601247388</y>
            <z>66.91689606274197</z>
        </Scale>
        <Link id="166448">                “一个simplekml.Link类实例，接受simplekml.Link
            <href>kmlfile/mode/car.dae</href>
        </Link>
        <ResourceMap>
        </ResourceMap>
    </Model>
</Placemark>
'''