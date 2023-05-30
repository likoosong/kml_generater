# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, timezone, date

import ephem
from astral.sun import sun
from astral import LocationInfo
import simplekml
from simplekml import Kml, Style, ListItemType, StyleMap

from settings.constant import FILEPATH

class TourPointDay24(object):

    def __init__(self, kmlname):
        self.kml = Kml(name=kmlname, open=1)
        pass

    def sun_location_sort_time(self, dates):
        new_dates = []
        prev_date = None
        for date_str in dates:
            date = datetime.fromisoformat(date_str[:-1])
            if prev_date and date < prev_date:
                date += timedelta(days=1)
            new_dates.append(date.strftime('%Y-%m-%dT%H:%M:%SZ'))
            prev_date = date
        return new_dates

    def sun_astral(self, longitude, latitude):

        date_to_check = date(2023, 3, 19)

        city = LocationInfo()
        city.latitude = latitude
        city.longitude = longitude

        s = sun(city.observer, date=date_to_check)
        # 将本地日出时间转换为 UTC 时间
        utc_dawn = s["dawn"].astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        # utc_sunrise = s["sunrise"].astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        utc_sunrise = (s["dawn"].astimezone(timezone.utc) + timedelta(hours=2)).strftime('%Y-%m-%dT%H:%M:%SZ')
        utc_noon = s["noon"].astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        # utc_sunset = s["sunset"].astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        utc_dusk = s["dusk"].astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

        date_to_check = date(2023, 3, 20)
        next_s = sun(city.observer, date=date_to_check)
        utc_next_dawn = next_s["dawn"].astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        utc_next_sunrise = (next_s["dawn"].astimezone(timezone.utc) + timedelta(hours=2)).strftime('%Y-%m-%dT%H:%M:%SZ')

        print(f"UTC 黎明时间: {utc_dawn}")
        print(f"UTC 日出时间: {utc_sunrise}")
        print(f"UTC 正午时间: {utc_noon}")
        # print(f"UTC 日落时间: {utc_sunset}")
        print(f"UTC 黄昏时间: {utc_dusk}")
        sun2 = ephem.Sun()
        date2 = ephem.date(date_to_check)
        location = ephem.Observer()
        location.lat, location.lon = latitude, longitude

        midnight = (location.next_antitransit(sun2, start=date2)).datetime().strftime('%Y-%m-%dT%H:%M:%SZ')  # 午夜时间
        print(midnight)

        print(f"UTC 黎明next: {utc_next_dawn}")
        print(f"UTC 日出next: {utc_next_sunrise}")
        # print([utc_dawn, utc_sunrise, utc_noon, utc_sunset, utc_dusk, utc_next_dawn, utc_next_sunrise])
        print([utc_dawn, utc_sunrise, utc_noon, utc_dusk, midnight, utc_next_dawn, utc_next_sunrise])
        return self.sun_location_sort_time([utc_dawn, utc_sunrise, utc_noon, utc_dusk, midnight, utc_next_dawn, utc_next_sunrise])

        # return [utc_dawn, utc_sunrise, utc_noon, utc_sunset, utc_dusk, utc_next_dawn, utc_next_sunrise]



    def sun_timestamp(self, longitude, latitude):
        from datetime import date
        now = date.today()
        sun = ephem.Sun()
        date = ephem.date(now)
        location = ephem.Observer()
        location.lat, location.lon = latitude, longitude

        # 计算日出的时间
        sunrise = location.next_rising(sun, start=date)
        noon = location.next_transit(sun, start=date)          # 中午时间
        sunset = location.next_setting(sun, start=date)        # 日落时间
        midnight = location.next_antitransit(sun, start=date)  # 午夜时间
        # sunrise = (location.next_rising(sun, start=date)).datetime().strftime('%Y-%m-%dT%H:%M:%SZ')

        sunrise = datetime.strptime(str(sunrise), "%Y/%m/%d %H:%M:%S")
        noon = datetime.strptime(str(noon), "%Y/%m/%d %H:%M:%S")
        sunset = datetime.strptime(str(sunset), "%Y/%m/%d %H:%M:%S")
        midnight = datetime.strptime(str(midnight), "%Y/%m/%d %H:%M:%S")

        sunrise_2_house = sunrise + timedelta(hours=2)   # 日出时间

        if sunrise > noon:
            noon = noon + timedelta(hours=24)            # 中午时间
        if sunrise > sunset:
            sunset = sunset + timedelta(hours=24)        # 日落时间
        if sunrise > midnight:
            midnight = midnight + timedelta(hours=24)    # 午夜时间

        sunrise_next = sunrise + timedelta(hours=24)                # 黎明
        sunrise_next_2_house = sunrise_2_house + timedelta(hours=24)  # 黎明后两个小时

        sunrise_1 = sunrise.strftime("%Y-%m-%dT%H:%M:%SZ")                 # 日出时间
        sunrise_2 = sunrise_2_house.strftime("%Y-%m-%dT%H:%M:%SZ")         # 日出后2个小时
        sunrise_3 = noon.strftime("%Y-%m-%dT%H:%M:%SZ")                    # 中午时间
        sunrise_4 = sunset.strftime("%Y-%m-%dT%H:%M:%SZ")                  # 日落时间
        sunrise_5 = midnight.strftime("%Y-%m-%dT%H:%M:%SZ")                # 午夜时间
        sunrise_6 = sunrise_next.strftime("%Y-%m-%dT%H:%M:%SZ")            # 下一个黎明
        sunrise_7 = sunrise_next_2_house.strftime("%Y-%m-%dT%H:%M:%SZ")    # 下一个黎明 日出后2个小时

        print([sunrise_1, sunrise_2, sunrise_3, sunrise_4, sunrise_5, sunrise_6, sunrise_7])
        return [sunrise_1, sunrise_2, sunrise_3, sunrise_4, sunrise_5, sunrise_6, sunrise_7]


    def tour_point_day_neight_change(self, kmlname, longitude, latitude, altitude=100, heading=90, roll=0, tilt=100, tour_time=30):

        # sunrise_1, sunrise_2, sunrise_3, sunrise_4, sunrise_5, sunrise_6, sunrise_7 = self.sun_timestamp(longitude, latitude)
        sunrise_1, sunrise_2, sunrise_3, sunrise_4, sunrise_5, sunrise_6, sunrise_7 = self.sun_astral(longitude, latitude)

        pnt = self.kml.newpoint(name=kmlname, coords=[[longitude, latitude]])
        camera = simplekml.Camera(
            latitude=latitude,
            longitude=longitude,
            altitude=altitude,
            heading=90,
            roll=0,
            tilt=45,
            gxaltitudemode = simplekml.AltitudeMode.absolute
        )
        pnt.camera = camera
        pnt.iconstyle.icon.href = ''

        self.tour = self.kml.newgxtour(name="play me")
        self.playlist = self.tour.newgxplaylist()


        # 第一个相机 出现的时间
        self.flyto = self.playlist.newgxflyto()
        self.flyto.camera.gxhorizfov = 60   # 绕 x 轴旋转
        self.flyto.camera.longitude = longitude
        self.flyto.camera.latitude = latitude
        self.flyto.camera.altitude = altitude
        self.flyto.camera.heading = 90
        self.flyto.camera.tilt = 100
        self.flyto.camera.roll = 0
        self.flyto.camera.gxaltitudemode = simplekml.AltitudeMode.absolute

        # 等待两秒在进行播放
        self.playlist.newgxwait(gxduration=2)

        # 第二个相机
        self.flyto = self.playlist.newgxflyto(gxduration=2)
        self.flyto.camera.gxhorizfov = 120   # 绕 x 轴旋转
        self.flyto.gxflytomode = 'smooth'
        self.flyto.camera.longitude = longitude
        self.flyto.camera.latitude = latitude
        self.flyto.camera.altitude = altitude
        self.flyto.camera.heading = 90
        self.flyto.camera.tilt = 120
        self.flyto.camera.roll = 0
        self.flyto.camera.gxaltitudemode = simplekml.AltitudeMode.absolute
        self.flyto.camera.gxtimestamp.when = sunrise_1

        s1  = simplekml.GxOption(name=simplekml.GxOption.historicalimagery, enabled=False)
        s2  = simplekml.GxOption(name=simplekml.GxOption.sunlight, enabled=True)
        s3  = simplekml.GxOption(name=simplekml.GxOption.streetview, enabled=False)
        self.flyto.camera.gxvieweroptions = simplekml.GxViewerOptions(gxoptions=[s1, s2, s3])

        # 等待两秒在进行播放
        self.playlist.newgxwait(gxduration=1)

        # 第三个相机
        self.flyto = self.playlist.newgxflyto(gxduration=5)
        self.flyto.camera.gxhorizfov = 120   # 绕 x 轴旋转
        self.flyto.gxflytomode = 'smooth'
        self.flyto.camera.longitude = longitude
        self.flyto.camera.latitude = latitude
        self.flyto.camera.altitude = altitude
        self.flyto.camera.heading = 90
        self.flyto.camera.tilt = 120
        self.flyto.camera.roll = 0
        self.flyto.camera.gxaltitudemode = simplekml.AltitudeMode.absolute
        self.flyto.camera.gxtimestamp.when = sunrise_2

        s1  = simplekml.GxOption(name=simplekml.GxOption.historicalimagery, enabled=False)
        s2  = simplekml.GxOption(name=simplekml.GxOption.sunlight, enabled=True)
        s3  = simplekml.GxOption(name=simplekml.GxOption.streetview, enabled=False)
        self.flyto.camera.gxvieweroptions = simplekml.GxViewerOptions(gxoptions=[s1, s2, s3])


        # 第四个相机
        self.flyto = self.playlist.newgxflyto(gxduration=10)
        self.flyto.camera.gxhorizfov = 120   # 绕 x 轴旋转
        self.flyto.gxflytomode = 'smooth'
        self.flyto.camera.longitude = longitude
        self.flyto.camera.latitude = latitude
        self.flyto.camera.altitude = altitude
        self.flyto.camera.heading = 180
        self.flyto.camera.tilt = 120
        self.flyto.camera.roll = 0
        self.flyto.camera.gxaltitudemode = simplekml.AltitudeMode.absolute
        self.flyto.camera.gxtimestamp.when = sunrise_3

        s1  = simplekml.GxOption(name=simplekml.GxOption.historicalimagery, enabled=False)
        s2  = simplekml.GxOption(name=simplekml.GxOption.sunlight, enabled=True)
        s3  = simplekml.GxOption(name=simplekml.GxOption.streetview, enabled=False)
        self.flyto.camera.gxvieweroptions = simplekml.GxViewerOptions(gxoptions=[s1, s2, s3])

        # 第五个相机
        self.flyto = self.playlist.newgxflyto(gxduration=10)
        self.flyto.camera.gxhorizfov = 120   # 绕 x 轴旋转
        self.flyto.gxflytomode = 'smooth'
        self.flyto.camera.longitude = longitude
        self.flyto.camera.latitude = latitude
        self.flyto.camera.altitude = altitude
        self.flyto.camera.heading = 270
        self.flyto.camera.tilt = 120
        self.flyto.camera.roll = 0
        self.flyto.camera.gxaltitudemode = simplekml.AltitudeMode.absolute
        self.flyto.camera.gxtimestamp.when = sunrise_4

        s1  = simplekml.GxOption(name=simplekml.GxOption.historicalimagery, enabled=False)
        s2  = simplekml.GxOption(name=simplekml.GxOption.sunlight, enabled=True)
        s3  = simplekml.GxOption(name=simplekml.GxOption.streetview, enabled=False)
        self.flyto.camera.gxvieweroptions = simplekml.GxViewerOptions(gxoptions=[s1, s2, s3])

        # 第六个相机
        self.flyto = self.playlist.newgxflyto(gxduration=10)
        self.flyto.camera.gxhorizfov = 120   # 绕 x 轴旋转
        self.flyto.gxflytomode = 'smooth'
        self.flyto.camera.longitude = longitude
        self.flyto.camera.latitude = latitude
        self.flyto.camera.altitude = altitude
        self.flyto.camera.heading = 0
        self.flyto.camera.tilt = 120
        self.flyto.camera.roll = 0
        self.flyto.camera.gxaltitudemode = simplekml.AltitudeMode.absolute
        self.flyto.camera.gxtimestamp.when = sunrise_5

        s1  = simplekml.GxOption(name=simplekml.GxOption.historicalimagery, enabled=False)
        s2  = simplekml.GxOption(name=simplekml.GxOption.sunlight, enabled=True)
        s3  = simplekml.GxOption(name=simplekml.GxOption.streetview, enabled=False)
        self.flyto.camera.gxvieweroptions = simplekml.GxViewerOptions(gxoptions=[s1, s2, s3])

        # 第七个相机
        self.flyto = self.playlist.newgxflyto(gxduration=10)
        self.flyto.camera.gxhorizfov = 120   # 绕 x 轴旋转
        self.flyto.gxflytomode = 'smooth'
        self.flyto.camera.longitude = longitude
        self.flyto.camera.latitude = latitude
        self.flyto.camera.altitude = altitude
        self.flyto.camera.heading = 90
        self.flyto.camera.tilt = 120
        self.flyto.camera.roll = 0
        self.flyto.camera.gxaltitudemode = simplekml.AltitudeMode.absolute
        self.flyto.camera.gxtimestamp.when = sunrise_6
        s1  = simplekml.GxOption(name=simplekml.GxOption.historicalimagery, enabled=False)
        s2  = simplekml.GxOption(name=simplekml.GxOption.sunlight, enabled=True)
        s3  = simplekml.GxOption(name=simplekml.GxOption.streetview, enabled=False)
        self.flyto.camera.gxvieweroptions = simplekml.GxViewerOptions(gxoptions=[s1, s2, s3])

        # 第八个相机
        self.flyto = self.playlist.newgxflyto(gxduration=5)
        self.flyto.camera.gxhorizfov = 120   # 绕 x 轴旋转
        self.flyto.gxflytomode = 'smooth'
        self.flyto.camera.longitude = longitude
        self.flyto.camera.latitude = latitude
        self.flyto.camera.altitude = altitude
        self.flyto.camera.heading = 90
        self.flyto.camera.tilt = 120
        self.flyto.camera.roll = 0
        self.flyto.camera.gxaltitudemode = simplekml.AltitudeMode.absolute
        self.flyto.camera.gxtimestamp.when = sunrise_7
        s1  = simplekml.GxOption(name=simplekml.GxOption.historicalimagery, enabled=False)
        s2  = simplekml.GxOption(name=simplekml.GxOption.sunlight, enabled=True)
        s3  = simplekml.GxOption(name=simplekml.GxOption.streetview, enabled=False)
        self.flyto.camera.gxvieweroptions = simplekml.GxViewerOptions(gxoptions=[s1, s2, s3])

        # 第九个相机
        self.flyto = self.playlist.newgxflyto(gxduration=5)
        self.flyto.camera.gxhorizfov = 60   # 绕 x 轴旋转
        # self.flyto.gxflytomode = 'smooth'
        self.flyto.camera.longitude = longitude
        self.flyto.camera.latitude = latitude
        self.flyto.camera.altitude = altitude
        self.flyto.camera.heading = 90
        self.flyto.camera.tilt = 100
        self.flyto.camera.roll = 0
        self.flyto.camera.gxaltitudemode = simplekml.AltitudeMode.absolute
        # self.flyto.camera.gxtimestamp.when = '2023-02-09T23:15:00Z'
        s1  = simplekml.GxOption(name=simplekml.GxOption.historicalimagery, enabled=False)
        s2  = simplekml.GxOption(name=simplekml.GxOption.sunlight, enabled=False)
        s3  = simplekml.GxOption(name=simplekml.GxOption.streetview, enabled=False)
        self.flyto.camera.gxvieweroptions = simplekml.GxViewerOptions(gxoptions=[s1, s2, s3])
        wono = datetime.now().strftime('%Y%m%d%H%M%S')
        self.kml.save(f"{FILEPATH}{wono}{kmlname}.kml")

    def run(self):
        kmlname = 'polygon演变'
        longitude = 121.548788
        latitude = 25.033257
        longitude = 116.4392438678113
        latitude = 39.91579922005565
        longitude = '121.4822068677437'
        latitude = '31.24177813485763'
        self.tour_point_day_neight_change(kmlname, longitude=longitude, latitude=latitude, altitude=100)
        wono = datetime.now().strftime('%Y%m%d%H%M%S')
        self.kml.save(f"{kmlname}2.kml")
        # self.sun_astral(longitude=longitude, latitude=latitude)



if __name__ == '__main__':

    ss = TourPointDay24('kmlname')
    ss.run()
