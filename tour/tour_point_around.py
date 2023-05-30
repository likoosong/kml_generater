# -*- coding: utf-8 -*-
import math
from datetime import datetime

import simplekml
from polycircles import polycircles

from settings.constant import FILEPATH


class TourPointAround(object):

    def __init__(self):
        self.kml = simplekml.Kml()

    def parser_coordinate_point(self, latitude, longitude, radius):
        """
        将距离坐标 radius 米的 圆圈重新排序
         :latitude  纬度
         :longitude 经度
         :radius    距离中心的距离
         """
        coordinates = list(polycircles.Polycircle(latitude=latitude, longitude=longitude, radius=radius, number_of_vertices=36).to_lon_lat())
        coordinates.pop()
        left_pnt = coordinates[19:]
        right_pnt = coordinates[0:19]
        left_pnt.extend(right_pnt)
        return left_pnt

    def parser_direction(self, coordinate, clock=True):
        """
        将旋转一周的坐标与旋转的角度进行绑定
        """
        headings = list(enumerate(range(0, 360, 10)))
        heading_pnt = list(zip(headings, coordinate))
        if clock:  # 正序
            return heading_pnt
        return heading_pnt.reverse()   # 倒序

    def parser_around_heading_point(self, heading, pnts):
        """
        根据开始的角度 重新生成开始旋转的顺序
        """
        # 如果 heading <= 0
        if heading <= 0:
            heading += 360
        pnt_idx = math.ceil(math.fabs(heading) / 10)
        if pnt_idx == 0 or pnt_idx == 36:
            pnts.append(pnts[0])
            return pnts

        left_pnt = pnts[0:pnt_idx]
        right_pnt = pnts[pnt_idx:]
        right_pnt.extend(left_pnt)
        right_pnt.append(right_pnt[0])
        return right_pnt

    def create_tour_point_around(self, kmlname, longitude, latitude, altitude, horizfov, tilt=60,  heading=0, radius=20, tour_time=30, roll=0, clock=True, heading_point=None):
        tour = self.kml.newgxtour(name=kmlname)
        playlist = tour.newgxplaylist()
        duration = (tour_time - 1) / 36

        for ix, point in enumerate(heading_point):
            hd, pnt = point
            lon, lat = pnt
            idx, heading = hd
            if ix == 0:
                flyto = playlist.newgxflyto()  # 0.25
                flyto.camera.gxhorizfov = horizfov
                flyto.camera.longitude = lon
                flyto.camera.latitude = lat
                flyto.camera.altitude = altitude
                flyto.camera.heading = heading
                flyto.camera.tilt = tilt
                flyto.camera.roll = roll
                flyto.camera.altitudemode = simplekml.AltitudeMode.absolute
                playlist.newgxwait(gxduration=1)
            else:
                flyto = playlist.newgxflyto(gxduration=duration)  # 0.25
                flyto.camera.gxhorizfov = horizfov
                flyto.camera.longitude = lon
                flyto.camera.latitude = lat
                flyto.camera.altitude = altitude
                flyto.camera.heading = heading
                flyto.camera.tilt = tilt
                flyto.camera.roll = roll
                flyto.camera.altitudemode = simplekml.AltitudeMode.absolute
                flyto.gxflytomode = 'smooth'



            # self.kml.newpoint(name=f"{heading}", coords=[(lon, lat)])

        self.kml.newpoint(name=f"{kmlname}", coords=[(longitude, latitude)])

    def tour_point_around(self, kmlname, longitude, latitude, altitude, horizfov, tilt=60,  heading=0, radius=20, tour_time=30, roll=0, clock=True):

        coordinate = self.parser_coordinate_point(latitude, longitude, radius)
        pnts = self.parser_direction(coordinate, clock)
        heading_point = self.parser_around_heading_point(heading, pnts)
        self.create_tour_point_around(
            kmlname=kmlname,
            longitude=longitude,
            latitude=latitude,
            altitude=altitude,
            horizfov=horizfov,
            tilt=tilt,
            heading=heading,
            radius=radius,
            tour_time=tour_time,
            roll=roll,
            heading_point=heading_point
        )
        wono = datetime.now().strftime('%Y%m%d%H%M%S')
        self.kml.save(f"{FILEPATH}{wono}{kmlname}.kml")


    def run(self):

        filename = "上海4"  # 文件名
        longitude = 121.4952627807584  # 经度
        latitude = 31.24188370156092  # 纬度
        tilt = 60  # 環繞傾斜角度
        direction = 0  # 環繞啟始方向
        tour_time = 30  # 環繞一圈時間,
        radius = 868
        altitude = 765  # 高度
        horizfov = 60  # 環繞視野角度
        heading = -60  # 環繞啟始方向
        roll = 0

        self.tour_point_around(
            filename,
            longitude=longitude,
            latitude=latitude,
            altitude=altitude,
            horizfov=horizfov,
            tilt=tilt,
            heading=heading,
            radius=radius,
            tour_time=tour_time,
            roll=roll,
        )



if __name__ == '__main__':
    yy = TourPointAround()
    yy.run()



'''
功能：
1. Camera 首先初始化 对传入的参数进行初始化定位
2. 然后进行休眠1s
3. 对Camera 35
環繞方向 clockwise:順時針Clockwise    反時針CounterClockwise
    顺时针：后纬度 - 前纬度 = 为负   heading递增
    反时针：后纬度 - 前纬度 = 为正   heading递减
環繞半徑 Radius: 868 建議值為高度的1.67倍 , 0 表為環景
<gx:FlyTo>
    <gx:duration>0.52777777777778</gx:duration>
    gx:duration 双倍表示相机保持静止的时间： （用户传来环绕一周的时间 - 1秒)/36
    <gx:flyToMode>smooth</gx:flyToMode>
    gxflytomode  相机的行为方式 smooth 平滑的
    <Camera>
        <gx:horizFov>60</gx:horizFov>
        gxhorizfov  環繞視野角度 Fov: 30° <--> 120° (地平线 绕 x 轴旋转，接受浮点数)
        <longitude>116.40321286214</longitude>
        <latitude>39.895972974059</latitude>
        <altitude>915</altitude>
        altitude 海拔高度是一定的  環繞視點高度 Height (参数不会变， 用户传来什么是什么)
        <heading>60</heading>
        heading  z轴的旋转  環繞啟始方向 Ring Around Start Direction: -180° <--> 180°
        用户传入参数： 60 ~ 360 ~ 0 ~ 60  不会变
        <tilt>60</tilt>
        環繞傾斜角度 Tilt:60° (0°為正射，90°為水平) 不会变
        如果是，请使用默认<tilt> 值; 如果否，相机向上倾斜朝向地平线；
        指定 <tilt> 旋转 ≤ 90°。 90° 直视地平线。
        （如果距离较远且 <tilt> 等于 90°，则可能根本看不到地球表面。）本人理解地球水平倾斜角度
        <roll>0</roll>
        y轴指向北并与经线平行，x 轴指向东并与纬线平行 不会变
        <altitudeMode>absolute</altitudeMode>
    </Camera>
</gx:FlyTo>
:param filename:  文件名
:param longitude: 经度
:param latitude:  纬度
:param altitude: 高度
:param horizfov: 環繞視野角度
:param tilt:     環繞傾斜角度
:param start_head:  環繞啟始方向
:param duration:  環繞一圈時間
:param roll:
:param order:
:return:
'''
