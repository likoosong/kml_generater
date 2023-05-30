# -*- coding: utf-8 -*-
from datetime import datetime

import simplekml
from simplekml import Kml, Style, ListItemType, StyleMap

from settings.constant import FILEPATH


class TourChangePolygon(object):

    def __init__(self):

        self.kml = Kml()

        self.sn_ylw_pushpin0 = Style()
        self.sn_ylw_pushpin0.linestyle.color = 'ff00aaff'
        self.sn_ylw_pushpin0.linestyle.width = 1
        self.sn_ylw_pushpin0.polystyle.color = '7fff55ff'

        self.sh_ylw_pushpin2 = Style()
        self.sh_ylw_pushpin2.iconstyle.scale = 1.2
        self.sh_ylw_pushpin2.linestyle.color = 'ff00aaff'
        self.sh_ylw_pushpin2.linestyle.width = 1
        self.sh_ylw_pushpin2.polystyle.color = '7fff55ff'

        self.hide_line_style = Style()
        self.hide_line_style.linestyle.color = '50dfdfdf'  # simplekml.Color.red  # Red
        self.hide_line_style.linestyle.width = 1
        self.hide_line_style.extrude = 1
        self.hide_line_style.visibility = 0

        self.hide_point_style = Style()
        self.hide_point_style.labelstyle.color = simplekml.Color.red  # simplekml.Color.red  # Red
        self.hide_point_style.labelstyle.scale = 1
        self.hide_point_style.iconstyle.scale = 1
        self.hide_point_style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png'  # 设置图标

        self.msn_ylw_pushpin5 = StyleMap()
        self.msn_ylw_pushpin5.normalstyle = self.sn_ylw_pushpin0
        self.msn_ylw_pushpin5.highlightstyle = self.sh_ylw_pushpin2

        self.frontend = self.kml.newfolder(name='evolution', open=1)
        self.backend = self.frontend.newfolder(name='line', open=1)
        self.center_point = self.frontend.newfolder(name='point', open=1)

        self.tour = self.kml.newgxtour(name="play2 me")
        self.playlist = self.tour.newgxplaylist()


    def polygon_change(self, poly_name=None, longitude=None, latitude=None, linear_ring=None, tour_time=30):

        pnt = self.center_point.newpoint(name=poly_name, coords=[[longitude, latitude]])
        pnt.style = self.hide_point_style
        pnt.visibility = 0
        pnt.altitudemode = simplekml.GxAltitudeMode.relativetoseafloor

        animatedupdate = self.playlist.newgxanimatedupdate(gxduration=1)  # path_w
        animatedupdate.update.change = f"""<Placemark targetId="{int(pnt.id) + 1}"><visibility>1</visibility></Placemark>"""

        animatedupdate = self.playlist.newgxanimatedupdate(gxduration=tour_time)  # path_w

        animatedupdate.update.change = f"""
            <Polygon targetId="{self.pol_front.id}">
                <tessellate>1</tessellate>
                <outerBoundaryIs>
                    <LinearRing>
                        <coordinates>{linear_ring}</coordinates>
                    </LinearRing>
                </outerBoundaryIs>
            </Polygon>
            """

        self.flyto = self.playlist.newgxflyto(gxduration=tour_time)
        self.flyto.gxflytomode = 'smooth'
        self.playlist.newgxwait(gxduration=2)


    def tour_polygon_change(self, kmlname, tour_time, poly_coords):


        from utlis.parser_line_coords import parser_polygon_coords, center_geolocation_coord

        for idx, poly in enumerate(poly_coords):
            coords = poly.get('coords')
            poly_name = poly.get('poly_name')
            longitude, latitude = center_geolocation_coord(coords)
            if idx:
                linear_ring = ' '.join([','.join(coord) for coord in coords])
                self.polygon_change(poly_name, longitude=longitude, latitude=latitude, linear_ring=linear_ring, tour_time=tour_time)
            else:
                self.pol_front = self.frontend.newpolygon(name=poly_name, outerboundaryis=coords)
                self.pol_front.stylemap = self.msn_ylw_pushpin5
                self.pol_front.extrude = 1

                self.playlist.newgxwait(gxduration=3)
                pnt = self.center_point.newpoint(name=poly_name, coords=[[longitude, latitude]])
                pnt.style = self.hide_point_style
                pnt.visibility = 1
                pnt.altitudemode = simplekml.GxAltitudeMode.relativetoseafloor

            hide_line = self.backend.newlinestring(name=poly_name, coords=coords)
            hide_line.style = self.hide_line_style


        wono = datetime.now().strftime('%Y%m%d%H%M%S')
        self.kml.save(f"{FILEPATH}{wono}{kmlname}.kml")

if __name__ == '__main__':

    ss = TourChangePolygon()
    ss.tour_polygon_change()

# self.fol.liststyle.listitemtype = ListItemType.radiofolder
# self.front.liststyle.listitemtype = ListItemType.checkoffonly   # 拒绝点击