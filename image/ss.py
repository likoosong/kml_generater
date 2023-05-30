
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


    # start_pnt.lookat = simplekml.LookAt(
    #     gxaltitudemode=simplekml.GxAltitudeMode.relativetoseafloor,
    #     longitude=start_longitude,      # 经度
    #     latitude=start_latitude,        # 纬度
    #     range=distance,                 # 视点离兴趣点有多远
    #     heading=0,                      # 视图位于正北角度
    #     tilt=30                         # 本人理解地球水平倾斜角度   90° 直视地平线
    # )



蓝箭头 与 蓝颜色 99ffac59
'http://earth.google.com/images/kml-icons/track-directional/track-0.png'


from simplekml import Kml, OverlayXY, ScreenXY, Units, Camera, AltitudeMode, ViewVolume
photo.camera = Camera(longitude=18.410858, latitude=-33.904446, altitude=50, altitudemode=AltitudeMode.clamptoground)


linestring.altitudemode = simplekml.AltitudeMode.relativetoground
linestring.extrude = 1




lo.iconstyle.icon.href = "" # Remove the icons

# Style everything
multipnt.labelstyle.scale = 0.0 # Hide the labels of the points
multipnt.iconstyle.icon.href = "http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png"
multilin.linestyle.color = Color.black
multilin.linestyle.width = 5
multipoleven.polystyle.color = Color.changealpha("77", Color.orange)
multipoleven.linestyle.color = Color.changealpha("77", Color.orange)
multipolodd.polystyle.color = Color.changealpha("77", Color.lightblue)
multipolodd.linestyle.color = Color.changealpha("77", Color.lightblue)

multipolodd.newpolygon(outerboundaryis=polycoordsodd[0]+end)


    # pnt.style.labelstyle.color = 'ff0000ff'
    # trk.stylemap.normalstyle.iconstyle.icon.href = 'http://earth.google.com/images/kml-icons/track-directional/track-0.png'
    # trk.stylemap.normalstyle.linestyle.color = '99ffac59'
    # trk.stylemap.normalstyle.linestyle.width = 6

    # trk.stylemap.highlightstyle.iconstyle.icon.href = 'http://earth.google.com/images/kml-icons/track-directional/track-0.png'
    # trk.stylemap.highlightstyle.iconstyle.scale = 1.2
    # trk.stylemap.highlightstyle.linestyle.color = '99ffac59'
    # trk.stylemap.highlightstyle.linestyle.width = 8


path.iconstyle.scale = 3      # 设置图标的大小
path.iconstyle.icon.href = 'http://earth.google.com/images/kml-icons/track-directional/track-0.png'

    <IconStyle id="substyle_0">
    <colorMode>normal</colorMode>
    <scale>1</scale>
    <heading>0</heading>
    <Icon id="link_0">
        <href>http://earth.google.com/images/kml-icons/track-directional/track-0.png</href>
    </Icon>
    </IconStyle>



a = """


ffmpeg -i 上海88.m4v -i 英雄的黎明.mp3 -vcodec copy -acodec copy new.mp4

ffmpeg -i 上海88.m4v -i StarSky.mp3 -vcodec copy -acodec copy new2.mp4

ffmpeg -i new2.mp4 -ss 00:00:00 -to 00:03:36 out.mp4

ffmpeg -t 10 -i input.mp4  -filter_complex  "[0:v]crop=w=100:h=100:x=300:y=300,boxblur=luma_radius=25:luma_power=2[boxblur];[0:v][boxblur]overlay=300:300[vout]" -map "[vout]" -map 0:a -c:v libx264 -crf 28 -preset veryfast -c:a copy -movflags +faststart output.mp4 -y

"""




import os
from simplekml import Kml, ListItemType, Color

kml = Kml(name="Styling", open=1)

# Make all the items into radio buttons
kml.document.liststyle.listitemtype = ListItemType.radiofolder

# Change the icon of the document in the TOC
kml.document.liststyle.itemicon.href = "http://maps.google.com/mapfiles/kml/shapes/parks.png"

# A normal Point with both a LabelStyle and IconStyle
pnt = kml.newpoint(name="Kirstenbosch Normal", description="A style map.", coords=[(18.431486,-33.988)])
pnt.labelstyle.color = 'ff0000ff'
pnt.labelstyle.scale = 2  # Text twice as big
pnt.labelstyle.color = "ffff0000"
pnt.iconstyle.color = 'ffff0000'  # Blue
pnt.iconstyle.scale = 3  # Icon thrice as big
pnt.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/info-i.png'  # Culry 'information i

# A Point with a styleMap. The Text changes from blue to red on mouse over.
pnt = kml.newpoint(name="Kirstenbosch StyleMap", coords=[(18.432314,-33.988862)])
pnt.stylemap.normalstyle.labelstyle.color = 'ffff0000'
pnt.stylemap.highlightstyle.labelstyle.color = 'ff0000ff'

# A red thick LineString
lin = kml.newlinestring(name="Pathway", description="A pathway in Kirstenbosch",
                        coords=[(18.43312,-33.98924), (18.43224,-33.98914), (18.43144,-33.98911), (18.43095,-33.98904)])
lin.linestyle.color = Color.red  # Red
lin.linestyle.width = 10  # 10 pixels

# A Polygon with a hole. Half invisible.
pol = kml.newpolygon(name="Atrium Garden",
                     outerboundaryis=[(18.43348,-33.98985), (18.43387,-33.99004262216968), (18.43410,-33.98972), (18.43371,-33.98952), (18.43348,-33.98985)],
                     innerboundaryis=[(18.43360,-33.98982), (18.43386,-33.98995), (18.43401,-33.98974), (18.43376,-33.98962), (18.43360,-33.98982)])
pol.polystyle.color = '990000ff'  # Red
pol.polystyle.outline = 0

# A Point showing off a BalloonStyle
pnt = kml.newpoint(name="BallonStyle", coords=[(18.429191, -33.987286)])
pnt.balloonstyle.text = "These are trees and this text is blue with a green background."
pnt.balloonstyle.bgcolor = Color.lightgreen
pnt.balloonstyle.textcolor = Color.rgb(0, 0, 255)




# Some sub folders
fol = fol.newfolder(name='A Nested Folder', description="Description of a nested folder")
fol = kml.newfolder(name='Point Tests', description="Description of Point Folder")

# A folder containing points with style
stpnt = fol.newpoint(name="Cape Town Stadium", description='The Cape Town stadium built for the 2010 world cup soccer.', coords=[(18.411102, -33.903486)])
vapnt = fol.newpoint()
vapnt.name = "V&A Waterfront"
vapnt.description = "The V&A Waterfront in Cape Town"
vapnt.coords = [(18.418699, -33.907080)]
vapnt.style.labelstyle.color = 'ff0000ff'
vapnt.labelstyle.scale = 2
vapnt.labelstyle.colormode = ColorMode.random
vapnt.style.iconstyle.color = 'ffff00ff'
vapnt.iconstyle.heading = 45
vapnt.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/arrow.png'
fwpnt = fol.newpoint(name="Ferris Wheel", description="Same style as V&A", coords=[(18.422892, -33.912937)])
fwpnt.style = vapnt.style
shpnt = fol.newpoint(name="Signal Hill", description="Style from a class", coords=[(18.399813, -33.920250)])
style = Style()
style.labelstyle.color = "ff00ffff"
shpnt.style = style








# -*- coding: utf-8 -*-
from datetime import datetime

import simplekml
from simplekml import Kml, Snippet, Types, Style
# from simplekml import Kml, Model, AltitudeMode, Orientation, Scale
#
# model_car = Model(
#     altitudemode=AltitudeMode.clamptoground,
#     orientation=Orientation(heading=75.0, tilt=0, roll=0),
#     scale=Scale(x=1, y=1, z=1)
# )
# model_car.link.href = 'mode/car.dae'
# model_car.location
# # trk.model = model_car
# # trk.model.link.href = car_dae



import simplekml

# 创建KML文档和3D模型对象
kml = simplekml.Kml()
model_car = kml.newmodel(name='Car')

# 创建链接对象，指向包含3D模型数据的文件
link = simplekml.Link(href='mode/car.dae')
model_car.link = link

# 设置3D模型的位置、方向和缩放比例
model_car.location = simplekml.Location(longitude=-122.0822035425683, latitude=37.42228990140251, altitude=0)
model_car.orientation = simplekml.Orientation(heading=75.0)
model_car.scale = simplekml.Scale(x=1, y=1, z=1)

# 设置3D模型的其他属性
model_car.altitudemode = simplekml.AltitudeMode.clamptoground
model_car.color = 'ffffffff'  # 白色

# 保存KML文档
kml.save('car.kml')







三、python 模块

```
pip install simplekml
```



```
country-bounding-boxes 国家边界
pygeoj
pip install georeverse     找到给经纬度的城市、州和国家/地区的最佳估值
pip install geojso 可解析  并随机生成点、线、面


将 geoJson 转换为 KML 格式。来自https://github.com/mapbox/tokml的端口
pip3 install geo2kml

from osgeo import gdal, ogr
srcDS = gdal.OpenEx('input.kml')
ds = gdal.VectorTranslate('output.json', srcDS, format='GeoJSON')


```







'''
















