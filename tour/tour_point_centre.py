from datetime import datetime

import simplekml

from settings.constant import FILEPATH

class TourPointCentre:

    def __init__(self, name):
        self.kml = simplekml.Kml(name=name)

    def tour_point_centre(self, kmlname, longitude, latitude, altitude, tilt, tour_time, clock=1):

        tour = self.kml.newgxtour(name=kmlname)
        playlist = tour.newgxplaylist()                #     新的gx播放列表
        duration = (tour_time - 1) / 36                #     旋转10度话费时间

        for idx, heading in enumerate(range(0, 370, 10)):    # 0， 10 ，20 ， 30  360

            flyto = playlist.newgxflyto(gxduration=duration)  # 0.25
            flyto.camera.longitude = longitude
            flyto.camera.latitude = latitude
            flyto.camera.altitude = altitude
            flyto.camera.heading = heading
            flyto.camera.tilt = tilt
            flyto.gxflytomode = 'smooth'
            flyto.camera.altitudemode = simplekml.AltitudeMode.absolute  # 高度模式绝对值
            if idx == 0:
                playlist.newgxwait(gxduration=1)

        wono = datetime.now().strftime('%Y%m%d%H%M%S')
        self.kml.save(f"{FILEPATH}{wono}{kmlname}.kml")

    def run(self):

        """  x: tilt   y: roll   z: heading """
        self.tour_point_centre(
            kmlname='东方明珠-初阶',
            longitude=121.4952627807584,  # 经度
            latitude=31.24188370156092,   # 纬度
            altitude=765,                 # 实际:467.9   高度 1.67 倍
            tilt=60,                      # 环绕倾斜角度
            tour_time=30,                 # 环绕一圈時間,
        )