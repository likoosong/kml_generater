


"""
拱形如何计算

如何绘画

"""






import math
from geopy.distance import great_circle
from geopy import Point

# 经纬度坐标
beijing_coords = (39.9042, 116.4074)
shanghai_coords = (31.2304, 121.4737)

# 计算两点间的大圆距离
distance = great_circle(beijing_coords, shanghai_coords).meters

# 计算半径和半圆高度
radius = distance / 5
height = [radius * math.sin(angle * math.pi / 180) for angle in range(0, 181, 5)]

# 创建KML文件
kml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
    <Style id="yellowLineStyle">
        <LineStyle>
            <color>7f00ffff</color>
            <width>4</width>
        </LineStyle>
    </Style>
    <Placemark>
        <name>Beijing to Shanghai</name>
        <styleUrl>#yellowLineStyle</styleUrl>
        <LineString>
            <tessellate>1</tessellate>
            <altitudeMode>relativeToGround</altitudeMode>
            <coordinates>
"""

# 在KML中添加半圆形轮廓的坐标
start_point = Point(beijing_coords)
end_point = Point(shanghai_coords)

for i, h in enumerate(height):
    # 计算当前角度下的点坐标
    current_angle = i * 5
    current_ratio = current_angle / 180
    current_point = Point(
        start_point.latitude + (end_point.latitude - start_point.latitude) * current_ratio,
        start_point.longitude + (end_point.longitude - start_point.longitude) * current_ratio,
        h
    )
    kml_content += f"{current_point.longitude},{current_point.latitude},{current_point.altitude} "

kml_content += """
            </coordinates>
        </LineString>
    </Placemark>
</Document>
</kml>
"""

# 将KML内容写入文件
with open("beijing_to_shanghai.kml", "w") as kml_file:
    kml_file.write(kml_content)


# http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2021/
# https://gemvg.com/archives/561