# -*- coding: utf-8 -*-
import math
import random
from datetime import datetime

import simplekml
from polycircles import polycircles

from settings.constant import FILEPATH


class TourPointRing(object):

    def __init__(self):
        self.kml = simplekml.Kml()

    def tour_point_ring(self, kmlname, latitude, longitude, outer_radius, inner_radius=0, fill=1):
        """
        将距离坐标 radius 米的 圆圈重新排序
         :latitude  纬度
         :longitude 经度
         :radius    距离中心的距离
         """
        outer_polycircle = polycircles.Polycircle(latitude=latitude, longitude=longitude, radius=outer_radius, number_of_vertices=36)
        if inner_radius == 0:  # 圆形
            pol = self.kml.newpolygon(name=kmlname, outerboundaryis=outer_polycircle.to_kml())
        else: # 圆环
            inner_polycircle = polycircles.Polycircle(latitude=latitude, longitude=longitude, radius=inner_radius, number_of_vertices=36)
            pol = self.kml.newpolygon(name=kmlname, outerboundaryis=outer_polycircle.to_kml(), innerboundaryis=inner_polycircle.to_kml())

        pol.style.polystyle.color = simplekml.Color.changealphaint(200, simplekml.Color.rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        pol.extrude = 1
        pol.style.linestyle.width = 3
        pol.style.polystyle.outline = 1  # 必须勾勒出多边形，接受 0 或 1 的整数
        pol.style.polystyle.fill = fill  # 填充多边形，接受 0 或 1 的 int
        wono = datetime.now().strftime('%Y%m%d%H%M%S')
        self.kml.save(f"{FILEPATH}{wono}{kmlname}.kml")


    def run(self):

        kmlname = "上海4"  # 文件名
        longitude = 121.4952627807584  # 经度
        latitude = 31.24188370156092  # 纬度
        outer_radius = 868
        self.tour_point_ring(kmlname, latitude, longitude, outer_radius, inner_radius=800)




if __name__ == '__main__':
    yy = TourPointRing()
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
