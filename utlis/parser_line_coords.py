import json
from lxml import etree
from geopy.distance import geodesic, great_circle
from lxml import etree

def hex_to_rgba(hex_color):
    if len(hex_color) != 8:
        raise ValueError("颜色代码长度必须为8个字符")

    alpha = int(hex_color[0:2], 16)
    red = int(hex_color[2:4], 16)
    green = int(hex_color[4:6], 16)
    blue = int(hex_color[6:8], 16)
    return [red, green, blue, alpha]

def parser_polygon_show_hide_coords(xml_name):
    tree = etree.parse(xml_name)
    namespaces = {'kml': 'http://www.opengis.net/kml/2.2'}
    # 使用XPath找到所有包含Polygon子元素的Placemark元素中的styleUrl元素
    style_urls = tree.xpath('//kml:Placemark[kml:Polygon]/kml:styleUrl', namespaces=namespaces)

    polygons = []
    for idx, style_url in enumerate(style_urls):
        style_id = style_url.text[1:]  # 移除哈希字符'#'
        poly_color = tree.xpath(f'//kml:Style[@id="{style_id}"]//kml:PolyStyle//kml:color', namespaces=namespaces)
        if poly_color:
            poly_color = poly_color[0]
        else:
            style_map_urls = tree.xpath(f'//kml:StyleMap[@id="{style_id}"]//kml:Pair//kml:styleUrl', namespaces=namespaces)
            for style_map in style_map_urls:
                style_map_id = style_map.text[1:]  # 移除哈希字符'#'
                poly_color = tree.xpath(f'//kml:Style[@id="{style_map_id}"]//kml:PolyStyle//kml:color', namespaces=namespaces)
                if poly_color:
                    poly_color = poly_color[0]
                    continue

        poly_name = style_url.xpath('../kml:name', namespaces=namespaces)[0]
        # 获取同级别的Polygon中的coordinates
        coordinates_element = style_url.xpath('../kml:Polygon//kml:coordinates', namespaces=namespaces)[0]
        coords = []
        for point in coordinates_element.text.split(' '):
            point = point.strip()
            if not point:
                continue
            coords.append(point.split(','))
        polygons.append({'poly_name': poly_name.text, 'poly_color': poly_color.text, 'coordinates': coords})
    return polygons


def parser_polygon_coords(xml_name):

    polygons = []
    tree = etree.parse(xml_name, parser=etree.HTMLParser())

    placemarks = tree.xpath('//placemark')

    for placemark in placemarks:
        coordinates = placemark.xpath('./polygon//coordinates/text()')
        if not coordinates:
            continue
        name = placemark.xpath('./name/text()')[0]
        coords = []
        coordinates = coordinates[0]
        for point in coordinates.split(' '):
            point = point.strip()
            if not point:
                continue
            coords.append(point.split(','))
        polygons.append({"poly_name": name, 'coords': coords})
    return polygons


def parser_line_coords(xml_name):

    # 读取xml 文件
    tree = etree.parse(xml_name, parser=etree.HTMLParser())
    coordinates = tree.xpath('//coordinates/text()')[0]
    coords = []
    for point in coordinates.split(' '):
        point = point.strip('').strip("\t").strip("\r").strip("\n")
        if not point:
            continue
        coords.append(point.split(','))

    # 删除一些坐标
    return coords[0:-1:3]


def location_great_circle(start, end):
    """
    计算球面距离: 大地线使用目前国际通用的方法，用旋转椭球面表示地球，其计算的是两点在椭球面上的最短距离。
    优点:精确度高    缺点: 大地线的劣势在于计算速度太慢
    :return:
    """
    # gc = great_circle((45.768189, 126.6212835), (45.768189, 126.7212832))  # 同样返回distance对象
    gc = great_circle(start, end)  # 同样返回distance对象
    # print(gc.m)  # 距离: km: 千米, m: 米, miles: 英里
    return gc.m


def parser_line_distance(coords):
    """
    计算球面距离: 大地线使用目前国际通用的方法，用旋转椭球面表示地球，其计算的是两点在椭球面上的最短距离。
    优点:精确度高    缺点: 大地线的劣势在于计算速度太慢
    :return:
    """
    distance = 0
    length = len(coords)
    for idx, each in enumerate(coords):
        if length == idx +1:
            continue
        start_latitude, start_longitude, start_altitude = each
        end_latitude, end_longitude, end_altitude = coords[idx+1]
        start = [start_longitude, start_latitude]
        end = [end_longitude, end_latitude]
        dst = location_great_circle(start, end)
        distance += dst
    return length, distance


from math import cos, sin, atan2, sqrt, pi, radians, degrees
"""
https://stackoverflow.com/questions/6671183/calculate-the-center-point-of-multiple-latitude-longitude-coordinate-pairs
"""
def center_geolocation(geolocations):
    x = 0
    y = 0
    z = 0
    lenth = len(geolocations)
    for lon, lat in geolocations:
        lon = radians(float(lon))
        lat = radians(float(lat))
        x += cos(lat) * cos(lon)
        y += cos(lat) * sin(lon)
        z += sin(lat)

    x = float(x / lenth)
    y = float(y / lenth)
    z = float(z / lenth)

    return (degrees(atan2(y, x)), degrees(atan2(z, sqrt(x * x + y * y))))


def center_geolocation_coord(geolocations):
    x = 0
    y = 0
    z = 0
    lenth = len(geolocations)
    for coord in geolocations:

        lon, lat, height = coord

        lon = radians(float(lon))
        lat = radians(float(lat))
        x += cos(lat) * cos(lon)
        y += cos(lat) * sin(lon)
        z += sin(lat)

    x = float(x / lenth)
    y = float(y / lenth)
    z = float(z / lenth)
    return (degrees(atan2(y, x)), degrees(atan2(z, sqrt(x * x + y * y))))


if __name__ == '__main__':
    pass
