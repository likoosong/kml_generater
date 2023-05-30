#### 一、KML generater 

- 运行
    ```
    安装python环境后，请运行
    pip install -r requestments.txt
    python main.py
    ```
- 打包
	```
	pyinstaller --windowed --onefile --key '123456789' --icon=image/logo.ico --clean --noconfirm main.py
	```

#### 二、功能介绍


<iframe src="//player.bilibili.com/player.html?aid=612801653&bvid=BV1ph4y1p7Hq&cid=1105709938&page=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"> </iframe>




#### 三、更新迭代

```
2022-11-29：新增动态浏览模块，包括四顾浏览和环绕浏览功能。
2022-12-31：新增圆形、环形和饼图的生成功能。
2023-01-01：新增生长路线模块，包括固定视角、环绕视角和跟随视角的生长路线功能。
2023-01-12：新增省市县区下载功能，支持轮廓和填充颜色。
2023-01-14：修复多边形区域选择中国、包含子区域、颜色填充下载失败的问题。
2023-01-21：修复选择中国时，子区域不包含在内，颜色填充包含的bug。
2023-01-31：修复Windows版本无法安装的问题。
2023-02-19：增加缩时浏览功能（展示24小时太阳的变化）。
2023-03-19：修复缩时浏览生成动画播放逻辑混乱的问题。
2023-04-22：新增区域渐显功能。
2023-05-01：新增区域形状的动态演化功能。
2023-05-29：新增线路浏览（生长路线-跟随视角）功能，支持模型移动，并优化了kml文件的大小。
```



重要提示：具体操作可关注哔哩哔哩
哔哩哔哩教程: https://space.bilibili.com/153276950
QQ群号: 708329713
主要功能：生成动画仅支持Google Earth Pro
- 点：环绕浏览、四顾浏览、圆环饼图
- 线：固定视角生长、环绕视角生长、跟随视角生长
- 面：生成省市县的地图，区域动态变化

严禁售卖，开源免费
下载位置：
- 点击下载后，生成的文件一般会保存在桌面上。
- 如果找不到桌面上的文件，请查找以下目录：
    Windows：C:\Users\用户名\Desktop\kmlfile
             找不到的话，试试这个目录：C:\Users\Administrator\Desktop\kmlfile
    Mac：/Users/用户名/Desktop/kmlfile

1. 线路的模型动画需要在kmlfile目录下创建一个名为"mode"的文件夹，并将您的dae文件命名为"car.dae"，即可运行。测试奥迪模型由零拾ZeroTen提供，感谢



强调：具体操作可关注哔哩哔哩
哔哩哔哩教程: https://space.bilibili.com/153276950
QQ群号:708329713



主要功能：生成动画仅支持某歌earthpro
	点: 环绕浏览、四顾浏览、圆环饼图
	线: 固定视角生长、环绕视角生长、跟随视角生长
	面：省市县的生成、区域的动态变化


严禁售卖，开源免费 
下载那里查找
	点击下载，生成的文件路径地址一般在桌面
	如果桌面没有，则在下面目录下查找
	windows： C:\Users\用户名\Desktop\kmlfile
                  找不到看这个文件夹： C:\Users\Administrator\Desktop\kmlfile
	Mac：     /Users/用户名/Desktop/kmlfile



1.线路的模型动画，需要在kmlfile种新建mode文件夹，并将你的dae文件命名为car.dae即可运行
  测试奥迪模型由 零拾ZeroTen提供，感谢零拾ZeroTen














