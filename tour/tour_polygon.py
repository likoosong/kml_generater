import json
import random
import requests
import simplekml
from simplekml import Kml, Types, Snippet, Color, Style

from datetime import datetime
from settings.constant import FILEPATH

class TourPolygon(object):

    def __init__(self):
        self.kml = Kml()

    def china_polygon_boundary(self, kmlname, boundary, children=True):
        """
        生成中国边界 可以选择 是否包含省的地图
        可以包含省界地图 也可以不包含省届地图
        有个争议的边界放入 国界里面
        :param kmlname:
        :param boundary:
        :param children:
        :return:
        """

        r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

        fol_line = self.kml.newfolder(name="国界")

        for each in boundary.get("features"):
            geometry_type = each.get("geometry")['type']  # 图形
            coordinates = each.get("geometry")['coordinates']  # 坐标

            folder_name = each.get("properties")['type']  # 城市名

            if folder_name != '国界':
                fol_line = self.kml.newfolder(name=folder_name)
            
            if geometry_type == 'LineString':
                lin = fol_line.newlinestring(name='line-1', coords=coordinates)
                lin.style.linestyle.color = '990000ff'  # simplekml.Color.red  # Red
                lin.style.linestyle.width = 2  # 10 pixels

            if geometry_type == 'MultiLineString':
                for idx, coordinate in enumerate(coordinates):
                    if folder_name == '国界':
                        lin = fol_line.newlinestring(name=f'line-{idx}', coords=coordinate)
                        lin.style.linestyle.color = '990000ff'  # simplekml.Color.red  # Red
                        lin.style.linestyle.width = 4  # 10 pixels
                    if folder_name == '争议':
                        lin = fol_line.newlinestring(name=f'line-{idx}', coords=coordinate)
                        lin.style.linestyle.color = '990000ff'  # simplekml.Color.red  # Red
                        lin.style.linestyle.width = 4  # 10 pixels
                    if folder_name == '海洋':
                        lin = fol_line.newlinestring(name=f'line-{idx}', coords=coordinate)
                        lin.style.linestyle.color = '990000ff'  # simplekml.Color.red  # Red
                        lin.style.linestyle.width = 4  # 10 pixels
                    if folder_name == '省界' and children:
                        lin = fol_line.newlinestring(name=f'line-{idx}', coords=coordinate)
                        lin.style.linestyle.color = simplekml.Color.rgb(r, g, b)
                        lin.style.linestyle.width = 4
                    if folder_name == '港澳':
                        lin = fol_line.newlinestring(name=f'line-{idx}', coords=coordinate)
                        lin.style.linestyle.color = '990000ff'
                        lin.style.linestyle.width = 4

            wono = datetime.now().strftime('%Y%m%d%H%M%S')
            self.kml.save(f"{FILEPATH}{wono}{kmlname}.kml")

    def china_single_polygon(self, kmlname, boundary, color=False):
        """
        查询  不带子区域
        可以填充颜色、也可以不填充颜色
        color 为 True
        :return:
        """
        each = boundary["features"][0]
        name = each.get("properties")["name"]
        center = each.get("properties")["center"]
        geometry_type = each.get("geometry")["type"]
        coordinates = each.get("geometry")["coordinates"]
        r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

        fol = self.kml.newfolder(name='polygon')
        for idx, coords in enumerate(coordinates):
            if geometry_type == "Polygon":
                coords = coords
            elif geometry_type == "MultiPolygon":
                coords = coords[0]
            if color:
                pol = fol.newpolygon(name=f"line-{idx}")
                pol.outerboundaryis = coords
                pol.style.linestyle.color = simplekml.Color.rgb(r, g, b)
                pol.style.linestyle.width = 1  # 10 pixels
                pol.style.polystyle.color = simplekml.Color.changealphaint(150, simplekml.Color.rgb(r, g, b))
                # pol.altitudemode = simplekml.AltitudeMode.relativetoground
            else:
                lin = fol.newlinestring(name=f"line-{idx}", coords=coords)
                lin.style.linestyle.color = simplekml.Color.rgb(r, g, b)
                lin.style.linestyle.width = 2  # 10 pixels
                lin.altitudemode = simplekml.AltitudeMode.relativetoground


        pnt = self.kml.newpoint(name=name)
        pnt.coords = [center]
        pnt.style.iconstyle.scale = 1  # Icon thrice as big
        pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png'
        wono = datetime.now().strftime('%Y%m%d%H%M%S')
        self.kml.save(f"{FILEPATH}{wono}{kmlname}.kml")

    def china_full_polygon(self, kmlname, boundary, color=False):
        """
        查询  带子区域
        可以填充颜色、也可以不填充颜色
        color 为 True
        :return:
        """
        fol = self.kml.newfolder(name='polygon')
        point = self.kml.newfolder(name='point')
        features = boundary["features"]
        for feature in features:

            properties = feature.get("properties")

            name = properties.get("name")
            coordinates = feature.get("geometry")["coordinates"]
            geometry_type = feature.get("geometry")["type"]

            print(name, geometry_type)

            line_r, line_g, line_b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
            poly_r, poly_g, poly_b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
            idx = 0
            for coordinate in coordinates:
                if geometry_type == 'Polygon' and color:
                    pol = fol.newpolygon(name=f"line-{name}-{idx}")
                    pol.tessellate = 1
                    pol.outerboundaryis = coordinate
                    pol.style.linestyle.width = 1  # 10 pixels
                    pol.style.linestyle.color = simplekml.Color.rgb(line_r, line_g, line_b)
                    pol.style.polystyle.color = simplekml.Color.changealphaint(150, simplekml.Color.rgb(poly_r, poly_g,poly_b))
                    # pol.altitudemode = simplekml.AltitudeMode.relativetoground
                elif geometry_type == 'Polygon':
                    lin = fol.newlinestring(name=f"line-{name}-{idx}", coords=coordinate)
                    lin.style.linestyle.color = simplekml.Color.rgb(line_r, line_g, line_b)
                    lin.style.linestyle.width = 2  # 10 pixels
                    lin.altitudemode = simplekml.AltitudeMode.relativetoground
                else:
                    for coords in coordinate:
                        idx += 1
                        if color:
                            pol = fol.newpolygon(name=f"line-{name}-{idx}")
                            pol.tessellate = 1
                            pol.outerboundaryis = coords
                            pol.style.linestyle.width = 1  # 10 pixels
                            pol.style.linestyle.color = simplekml.Color.rgb(line_r, line_g, line_b)
                            pol.style.polystyle.color = simplekml.Color.changealphaint(150, simplekml.Color.rgb(poly_r, poly_g, poly_b))
                            # pol.altitudemode = simplekml.AltitudeMode.relativetoground
                        else:
                            lin = fol.newlinestring(name=f"line-{name}-{idx}", coords=coords)
                            lin.style.linestyle.color = simplekml.Color.rgb(line_r, line_g, line_b)
                            lin.style.linestyle.width = 2  # 10 pixels
                            lin.altitudemode = simplekml.AltitudeMode.relativetoground

            center = properties.get("center")

            print(center)
            if center:
                pnt = point.newpoint(name=name)
                pnt.coords = [center]
                pnt.style.iconstyle.scale = 1  # Icon thrice as big
                pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png'

        wono = datetime.now().strftime('%Y%m%d%H%M%S')
        self.kml.save(f"{FILEPATH}{wono}{kmlname}.kml")


if __name__ == '__main__':
    kmlname = "中国3444"

    # url = 'https://geo.datav.aliyun.com/areas_v3/bound/100000_boundary.json'
    # boundary = requests.get(url).json()
    # TourPolygon().china_polygon_boundary(kmlname, boundary, children=True)

    # url = f'https://geo.datav.aliyun.com/areas_v3/bound/460000.json' # 141081
    # boundary = requests.get(url).json()
    # TourPolygon().china_single_polygon(kmlname, boundary, color=False)

    # boundary = requests.get(url='https://geo.datav.aliyun.com/areas_v3/bound/141081_full.json').json()  # 100000    650000
    boundary = requests.get(url='https://geo.datav.aliyun.com/areas_v3/bound/141081.json').json()  # 100000    650000
    TourPolygon().china_full_polygon('610000', boundary, color=True)