import simplekml

class ScreenOverlaysGenerator(object):

    def __init__(self):
        self.kml = simplekml.Kml()


    def simple_crosshairs(self):
        """
        中心的十字光标
        :return:
        """
        screen = self.kml.newscreenoverlay(name='crosshairs')
        screen.icon.href = "http://developers.google.com/kml/documentation/images/crosshairs.png"

        # 设置图标在屏幕上的位置 为屏幕中心
        screen.overlayxy = simplekml.OverlayXY(x=0.5, y=0.5, xunits=simplekml.Units.fraction, yunits=simplekml.Units.fraction)

        # 设置图标在屏幕上的位置（相对于屏幕中心位置） simplekml.Units.pixels 像素位置 15     simplekml.Units.insetpixels 15
        screen.screenxy = simplekml.ScreenXY(x=0.5, y=0.5, xunits=simplekml.Units.fraction, yunits=simplekml.Units.fraction)
        # 设置图标的旋转中心位置为屏幕中心
        screen.rotationxy = simplekml.RotationXY(x=0.5, y=0.5, xunits=simplekml.Units.fraction, yunits=simplekml.Units.fraction)
        # 设置图像的大小为 0x0 像素（将会根据图标原始尺寸等比例缩放）
        screen.size = simplekml.Size(x=0, y=0, xunits=simplekml.Units.pixels, yunits=simplekml.Units.pixels)

        # 设置十字光标是否可见
        screen.visibility = 1

    def absolute_position_top_left(self):
        """
        绝对定位：左上
        :return:
        """
        screen = self.kml.newscreenoverlay(name='screen overlay absolute top left')
        screen.icon.href = "http://developers.google.com/kml/documentation/images/top_left.jpg"

        # 设置图标在屏幕上的位置为屏幕左上角
        screen.overlayxy = simplekml.OverlayXY(x=0, y=1, xunits=simplekml.Units.fraction, yunits=simplekml.Units.fraction)
        # 设置图标在屏幕上的像素位置为屏幕左上角
        screen.screenxy = simplekml.ScreenXY(x=0, y=1, xunits=simplekml.Units.fraction, yunits=simplekml.Units.fraction)
        # 设置图标的旋转中心位置为图标左上角
        screen.rotationxy = simplekml.RotationXY(x=0, y=0, xunits=simplekml.Units.fraction, yunits=simplekml.Units.fraction)
        # 设置图标的大小为 0x0 分数单位，将根据图标原始尺寸等比例缩放
        screen.size = simplekml.Size(x=0, y=0, xunits=simplekml.Units.fraction, yunits=simplekml.Units.fraction)
        # 图片是否可见
        screen.visibility = 1

    def absolute_position_top_right(self):
        """
        绝对定位：右上角
        :return:
        """
        screen = self.kml.newscreenoverlay(name='screen overlay absolute top right')
        screen.icon.href = "http://developers.google.com/kml/documentation/images/top_right.jpg"

        # 设置图标在屏幕上的位置为屏幕右上角
        screen.overlayxy = simplekml.OverlayXY(x=1, y=1, xunits=simplekml.Units.fraction, yunits=simplekml.Units.fraction)
        # 设置图标在屏幕上的像素位置为屏幕右上角
        screen.screenxy = simplekml.ScreenXY(x=1, y=1, xunits=simplekml.Units.fraction, yunits=simplekml.Units.fraction)
        # 设置图标的旋转中心位置为图标右上角
        screen.rotationxy = simplekml.RotationXY(x=0, y=0, xunits=simplekml.Units.fraction, yunits=simplekml.Units.fraction)
        # 设置图标的大小为 0x0 分数单位，将根据图标原始尺寸等比例缩放
        screen.size = simplekml.Size(x=0, y=0, xunits=simplekml.Units.fraction, yunits=simplekml.Units.fraction)
        # 图片是否可见
        screen.visibility = 1

    def absolute_position_bottom_left(self):
        """
        绝对定位：左下
        :return:
        """
        screen = self.kml.newscreenoverlay(name='screen overlay absolute bottom left')
        screen.icon.href = "http://developers.google.com/kml/documentation/images/bottom_left.jpg"

        # 设置图标在屏幕上的位置为屏幕左下角
        screen.overlayxy = simplekml.OverlayXY(x=0, y=-1, xunits=simplekml.Units.fraction, yunits=simplekml.Units.fraction)
        # 设置图标在屏幕上的像素位置为屏幕左下角
        screen.screenxy = simplekml.ScreenXY(x=0, y=0, xunits=simplekml.Units.fraction, yunits=simplekml.Units.fraction)
        # 设置图标的旋转中心位置为图标左下角
        screen.rotationxy = simplekml.RotationXY(x=0, y=0, xunits=simplekml.Units.fraction, yunits=simplekml.Units.fraction)
        # 设置图标的大小为 0x0 分数单位，将根据图标原始尺寸等比例缩放
        screen.size = simplekml.Size(x=0, y=0, xunits=simplekml.Units.fraction, yunits=simplekml.Units.fraction)
        # 图片是否可见
        screen.visibility = 1

    def absolute_position_bottom_right(self):
        """
        绝对定位：右下角
        :return:
        """
        screen = self.kml.newscreenoverlay(name='screen overlay absolute bottom right')
        screen.icon.href = "http://developers.google.com/kml/documentation/images/bottom_right.jpg"

        # 设置图标在屏幕上的位置为屏幕右下角
        screen.overlayxy = simplekml.OverlayXY(x=1, y=-1, xunits=simplekml.Units.fraction, yunits=simplekml.Units.fraction)
        # 设置图标在屏幕上的像素位置为屏幕右下角
        screen.screenxy = simplekml.ScreenXY(x=1, y=0, xunits=simplekml.Units.fraction, yunits=simplekml.Units.fraction)
        # 设置图标的旋转中心位置为图标右下角
        screen.rotationxy = simplekml.RotationXY(x=0, y=0, xunits=simplekml.Units.fraction, yunits=simplekml.Units.fraction)
        # 设置图标的大小为 0x0 分数单位，将根据图标原始尺寸等比例缩放
        screen.size = simplekml.Size(x=0, y=0, xunits=simplekml.Units.fraction, yunits=simplekml.Units.fraction)
        # 图片是否可见
        screen.visibility = 1

    def dynamic_position_top_screen(self):
        """
        动态定位：屏幕顶部
        :return:
        """
        screen = self.kml.newscreenoverlay(name='screen overlay dynamic top screen')
        screen.icon.href = "http://developers.google.com/kml/documentation/images/dynamic_screenoverlay.jpg"

        # 设置图标在屏幕上的位置为屏幕左上角，使用分数单位表示，(0, 1) 表示左上角，(1, 1) 表示右上角
        screen.overlayxy = simplekml.OverlayXY(x=0, y=1, xunits=simplekml.Units.fraction, yunits=simplekml.Units.fraction)
        # 设置图标在屏幕上的像素位置为屏幕左上角，使用分数单位表示，(0, 1) 表示左上角，(1, 1) 表示右上角
        screen.screenxy = simplekml.ScreenXY(x=0, y=1, xunits=simplekml.Units.fraction, yunits=simplekml.Units.fraction)
        # 设置图标的旋转中心位置为图标左上角，使用分数单位表示，(0, 0) 表示左上角，(1, 1) 表示右下角
        screen.rotationxy = simplekml.RotationXY(x=0, y=0, xunits=simplekml.Units.fraction, yunits=simplekml.Units.fraction)

        # 设置图标的大小为宽度的1和高度的1/5，使用分数单位表示，将根据图标原始尺寸等比例缩放
        screen.size = simplekml.Size(x=1, y=0.2, xunits=simplekml.Units.fraction, yunits=simplekml.Units.fraction)
        # 图片是否可见，设置为 1 表示可见，0 表示隐藏
        screen.visibility = 1
    def dynamic_position_top_centre_screen(self):
        """
        动态定位：屏幕顶部居中
        :return:
        """
        screen = self.kml.newscreenoverlay(name='screen overlay dynamic top centre screen')
        screen.icon.href = "http://developers.google.com/kml/documentation/images/dynamic_screenoverlay.jpg"

        # 设置图标在屏幕上的位置为屏幕顶部居中，使用分数单位表示，(0.5, 1) 表示屏幕顶部居中位置
        screen.overlayxy = simplekml.OverlayXY(x=0.5, y=1, xunits=simplekml.Units.fraction, yunits=simplekml.Units.fraction)
        # 设置图标在屏幕上的像素位置为屏幕顶部居中，使用分数单位表示，(0.5, 1) 表示屏幕顶部居中位置
        screen.screenxy = simplekml.ScreenXY(x=0.5, y=1, xunits=simplekml.Units.fraction, yunits=simplekml.Units.fraction)
        # 设置图标的旋转中心位置为图标左上角，使用分数单位表示，(0, 0) 表示左上角，(1, 1) 表示右下角
        screen.rotationxy = simplekml.RotationXY(x=0, y=0, xunits=simplekml.Units.fraction, yunits=simplekml.Units.fraction)

        # 设置图标的大小为宽度的1和高度的1/5，使用分数单位表示，将根据图标原始尺寸等比例缩放
        screen.size = simplekml.Size(x=0.5, y=0.1, xunits=simplekml.Units.fraction, yunits=simplekml.Units.fraction)
        # 图片是否可见，设置为 1 表示可见，0 表示隐藏
        screen.visibility = 1
    def dynamic_position_right_screen(self):
        """
        动态定位：屏幕右侧(图片本身竖着的)
        :return:
        """
        screen = self.kml.newscreenoverlay(name='screen overlay dynamic right screen')
        screen.icon.href = "http://developers.google.com/kml/documentation/images/dynamic_right.jpg"
        # 设置图标在屏幕上的位置为屏幕右上角，使用分数单位表示，(0, 0) 表示左下角，(1, 1) 表示右上角
        screen.overlayxy = simplekml.OverlayXY(x=1, y=1, xunits=simplekml.Units.fraction, yunits=simplekml.Units.fraction)
        # 设置图标在屏幕上的像素位置为屏幕右上角，使用分数单位表示，(0, 0) 表示左下角，(1, 1) 表示右上角
        screen.screenxy = simplekml.ScreenXY(x=1, y=1, xunits=simplekml.Units.fraction, yunits=simplekml.Units.fraction)
        # 设置图标的旋转中心位置为图标左上角，使用分数单位表示，(0, 0) 表示左上角，(1, 1) 表示右下角
        screen.rotationxy = simplekml.RotationXY(x=0, y=0, xunits=simplekml.Units.fraction, yunits=simplekml.Units.fraction)
        # 设置图标的大小为宽度的0和高度的1，使用分数单位表示，将宽度设置为0会导致图标不可见
        screen.size = simplekml.Size(x=0, y=1, xunits=simplekml.Units.fraction, yunits=simplekml.Units.fraction)
        # 图片是否可见，设置为 1 表示可见，0 表示隐藏
        screen.visibility = 1


    def dynamic_position_custom_screen(self):
        """
        动态定位：自定义
        :return:
        """
        screen = self.kml.newscreenoverlay(name='screen overlay dynamic top centre screen')
        screen.icon.href = "http://developers.google.com/kml/documentation/images/dynamic_screenoverlay.jpg"

        # 设置图标在屏幕上的位置为屏幕顶部居中偏下，使用分数单位表示，(0.5, 0.7) 表示屏幕顶部居中偏下位置
        screen.overlayxy = simplekml.OverlayXY(x=0.5, y=0.7, xunits=simplekml.Units.fraction, yunits=simplekml.Units.fraction)
        # 设置图标在屏幕上的像素位置为屏幕顶部居中偏下，使用分数单位表示，(0.5, 0.7) 表示屏幕顶部居中偏下位置
        screen.screenxy = simplekml.ScreenXY(x=0.5, y=0.7, xunits=simplekml.Units.fraction, yunits=simplekml.Units.fraction)
        # 设置图标的旋转中心位置为图标左上角，使用分数单位表示，(0, 0) 表示左上角，(1, 1) 表示右下角
        screen.rotationxy = simplekml.RotationXY(x=0, y=0, xunits=simplekml.Units.fraction, yunits=simplekml.Units.fraction)

        # 设置图标的大小为宽度的1和高度的1/5，使用分数单位表示，将根据图标原始尺寸等比例缩放
        screen.size = simplekml.Size(x=0.5, y=0.1, xunits=simplekml.Units.fraction, yunits=simplekml.Units.fraction)
        # 图片是否可见，设置为 1 表示可见，0 表示隐藏
        screen.visibility = 1


    def run(self):
        screen.dynamic_position_top_centre_screen()
        kml_file_path = "screen_overlay_example.kml"
        self.kml.save(kml_file_path)

        print(f"KML file saved to {kml_file_path}")


if __name__ == '__main__':
    screen = ScreenOverlaysGenerator()
    screen.run()


