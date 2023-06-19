# -*- coding: utf-8 -*-
import random
from datetime import datetime

import simplekml
from simplekml import Kml, Snippet, Types, Style

from settings.constant import FILEPATH
from utlis.parser_line_coords import parser_line_coords, location_great_circle


class TourPolygonShow(object):

    def __init__(self, kmlname):
        self.kml = Kml(name=kmlname, open=1)
        self.polygon_folder = self.kml.newfolder(name="polygon")
        self.play_tour = self.kml.newgxtour(name="play me")
        self.play_playlist = self.play_tour.newgxplaylist()
        # # poly 样式
        # self.poly = Style()
        # self.poly.linestyle.color = '00ffffff'  # 白色
        # self.poly.linestyle.width = 2
        # self.poly.polystyle.color = '00ffffff'

    def polygon_linear(self, poly_name, tour_time, poly_color, coords):

        pol = self.polygon_folder.newpolygon(name=poly_name, outerboundaryis=coords)
        # pol.style = self.poly
        pol.style.linestyle.color = '00ffffff'  # 白色
        pol.style.linestyle.width = 2
        pol.style.polystyle.color = '00ffffff'
        pol.extrude = 1
        pol.tessellate = 1          # 是否跟随地形

        self.tour = self.kml.newgxtour(name=poly_name)
        self.playlist = self.tour.newgxplaylist()
        self.playlist.newgxwait(gxduration=1)

        animatedupdate = self.playlist.newgxanimatedupdate(gxduration=tour_time) # Line bf0000ff  Poly 4c0000ff
        # poly_color = f"{255:02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"
        # <LineStyle><color>bf0000ff</color></LineStyle> self.poly.id
        animatedupdate.update.change = f"""
            <Style targetId="{pol.style.id}">
				<PolyStyle><color>{poly_color}</color></PolyStyle>
            </Style>
        """
        self.playlist.newgxwait(gxduration=tour_time+3)  # 控制长短

        # ================所有========================================
        self.play_playlist.newgxwait(gxduration=tour_time)
        play_animatedupdate = self.play_playlist.newgxanimatedupdate(gxduration=tour_time) # Line bf0000ff  Poly 4c0000ff
        play_animatedupdate.update.change = f"""
                    <Style targetId="{pol.style.id}">
        				<PolyStyle><color>{poly_color}</color></PolyStyle>
                    </Style>
                """

    def tour_polygon_linear(self, kmlname, tour_time, poly_color, polygon_coords):

        for idx, each in enumerate(polygon_coords):
            poly_name = each.get('poly_name')
            coords = each.get('coords')
            self.polygon_linear(poly_name, tour_time, poly_color, coords)

        self.play_playlist.newgxwait(gxduration=3)  # 控制长短

        wono = datetime.now().strftime('%Y%m%d%H%M%S')
        self.kml.save(f"{FILEPATH}{wono}{kmlname}.kml")


if __name__ == '__main__':


    kmlname = 'wwwwwww'

    from utlis.t import aaaa as polygon_coords

    tour_time = 1

    show = TourPolygonShow(kmlname)
    show.tour_polygon_linear(kmlname, tour_time, polygon_coords)
