import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QLabel
from PyQt5.QtCore import QTimer, Qt, QPropertyAnimation, QRect, QPoint
from enum import Enum
import qtawesome as qta

# 定义一个枚举类型，表示消息的四个级别。
class AlertLevel(Enum):
    INFO = "Info"
    SUCCESS = "Success"
    WARNING = "Warning"
    ERROR = "Error"

class Toast(QFrame):
    # 为每个消息级别定义对应的样式和图标。这种结构便于后续根据级别获取相应的样式和图标。
    THEMES = {
        AlertLevel.INFO: {
            'style': "background-color: rgba(200, 245, 200, 120); color: white; border-radius: 5px; padding: 10px;",
            'icon': 'ph.info-bold',
            'color': 'white'
        },
        AlertLevel.SUCCESS: {
            'style': "background-color: rgba(60, 180, 60, 220); color: white; border-radius: 5px; padding: 10px;",
            'icon': 'mdi6.hand-okay',
            'color': 'white'
        },
        AlertLevel.WARNING: {
            'style': "background-color: rgba(230, 190, 60, 220); color: black; border-radius: 5px; padding: 10px;",
            'icon': 'ri.alarm-warning-line',
            'color': 'white'
        },
        AlertLevel.ERROR: {
            'style': "background-color: rgba(200, 60, 60, 180); color: white; border-radius: 5px; padding: 10px;",
            'icon': 'fa5s.star',
            'color': 'white'
        },
    }
    # 定义动画和消息显示的时长
    ANIMATION_DURATION = 2000       # 吐司消息滑入的动画持续时间
    TOAST_DISPLAY_DURATION = 2000 # 吐司消息显示的持续时间

    def __init__(self, title="", content="", level=AlertLevel.INFO, parent=None):
        super(Toast, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 根据消息级别获取对应的样式和图标
        theme = self.THEMES[level]
        # 将定义的样式应用于吐司消息窗口
        self.setStyleSheet(theme['style'])

        containerWidget = QWidget(self)

        self.iconButton = QPushButton(self)
        self.iconButton.setIcon(qta.icon(theme['icon'], color=theme['color']))

        self.iconButton.setStyleSheet("background-color: transparent; border: none; padding: 0; margin: 0;")

        self.titleLabel = QLabel(title, self)
        self.titleLabel.setVisible(bool(title))
        self.titleLabel.setStyleSheet("""
            background-color: transparent;
            padding: 0;
            margin: 0;
            font-weight: bold !important;
            font-size: 14px !important;
        """)
        self.contentLabel = QLabel(content, self)
        self.contentLabel.setVisible(bool(content))
        self.contentLabel.setStyleSheet("background-color: transparent; padding: 0; margin: 0;")

        layout = QHBoxLayout(containerWidget)  # 创建一个水平布局并设置其父容器为containerWidget
        # layout.setSpacing(5)  # 设置布局中各个组件之间的间隔为5个像素
        # layout.setContentsMargins(5, 5, 5, 5)  # 设置布局的边距，分别为左、上、右、下
        layout.addWidget(self.iconButton, 0, Qt.AlignLeft)  # 在布局中添加iconButton组件，对齐方式为靠左，stretch因子为0
        layout.addSpacing(5)  # 在布局的开始处添加5个像素的空间
        layout.addWidget(self.titleLabel, 1)  # 在布局中添加titleLabel组件，stretch因子为1
        layout.addSpacing(-5)  # 在布局的开始处添加5个像素的空间
        layout.addWidget(self.contentLabel, 2)  # 在布局中添加contentLabel组件，stretch因子为2

        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(containerWidget)
        self.setLayout(mainLayout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.hideToast)

        # 添加一个新的动画属性来处理上移动画
        self.animation = QPropertyAnimation(self, b"geometry")

    def showLeftToRightToast(self, x, y):
        self.animation.stop()
        self.animation.setDuration(self.ANIMATION_DURATION)
        # 创建一个属性动画，使吐司消息从左侧滑入
        self.animation.setStartValue(QRect(x - self.width(), y, self.width(), self.height()))
        self.animation.setEndValue(QRect(x, y, self.width(), self.height()))
        # 用单发计时器确保在动画开始之前显示吐司消息
        QTimer.singleShot(1, self.show)
        self.animation.start()
        # 启动自动隐藏的计时器
        self.timer.start(self.TOAST_DISPLAY_DURATION)


    def showRightToLeftToast(self, x, y):
        # 创建一个属性动画，使吐司消息从右侧滑入到左侧
        self.animation.setDuration(self.ANIMATION_DURATION)
        # 开始位置是`Toast`消息的右侧与x坐标对齐
        self.animation.setStartValue(QRect(x - self.width(), y, self.width(), self.height()))
        # 结束位置是`Toast`消息的左边界与x坐标对齐
        self.animation.setEndValue(QRect(x- 1.5*self.width(), y, self.width(), self.height()))
        print("self.width()", self.width(), self.height())
        # 用单发计时器确保在动画开始之前显示吐司消息
        QTimer.singleShot(1, self.show)
        self.animation.start()

        # 启动自动隐藏的计时器
        self.timer.start(self.TOAST_DISPLAY_DURATION)

    def showTopToBottomToast(self, x, y):
        self.setFixedSize(500, 100)
        self.animation.stop()
        self.animation.setDuration(self.ANIMATION_DURATION)
        self.animation.setStartValue(QRect(x - self.width(), y, self.width(), self.height()))
        self.animation.setEndValue(QRect(x - self.width(), y+self.height(), self.width(), self.height()))

        # 开始位置是Toast完全隐藏在PointDay24View的顶部
        self.animation.setStartValue(QRect(x-self.width()*0.5, y-self.width() * 0.2, self.width(), self.height()))
        # 结束位置是Toast完全展现在PointDay24View的下方
        self.animation.setEndValue(QRect(x-self.width()*0.5, y-self.width() * 0.1, self.width(), self.height()))

        QTimer.singleShot(1, self.show)
        self.animation.start()
        # 启动自动隐藏的计时器
        self.timer.start(self.TOAST_DISPLAY_DURATION)

    def showToast(self, x, y):
        """
        :param x：平面图的x坐标
        :param y：平面图的y坐标
        :param width：形状的宽度。
        :param height：身高的高度
        :return:
        """
        self.setFixedSize(500, 100)
        self.animation.stop()
        self.animation.setDuration(self.ANIMATION_DURATION)
        self.animation.setStartValue(QRect(x - self.width()*0.5, y-30, self.width(), self.height()))
        self.animation.setEndValue(QRect(x - self.width()*0.5, y+20, self.width(), self.height()))
        QTimer.singleShot(1, self.show)
        self.animation.start()
        # 启动自动隐藏的计时器
        self.timer.start(self.TOAST_DISPLAY_DURATION)

    def hideToast(self):
        # 隐藏吐司消息
        self.hide()

class Demo(QWidget):
    def __init__(self):
        super().__init__()

        # 创建一个按钮，点击时显示吐司消息
        layout = QVBoxLayout(self)
        self.toastButton = QPushButton('Show Toast', self)
        self.toastButton.clicked.connect(self.displayToast)
        layout.addWidget(self.toastButton)
        self.resize(500, 500)

    def displayToast(self):

        toast = Toast(title="下载成功", content="非常人、非俗人、非庸人", level=AlertLevel.ERROR, parent=self)
        # 获取Demo窗口的顶部中心位置
        center_x = self.frameGeometry().x() + self.width() // 2 - toast.width() // 2
        position_y = self.frameGeometry().y() - toast.height()
        toast.showTopToBottomToast(center_x, position_y)


        # toast = Toast("This is an error message!", AlertLevel.ERROR, self)
        #
        # # 获取 PointDay24View 部件的顶部中心坐标
        # top_center_point = self.mapToGlobal(QPoint(self.rect().width() // 2, 0))
        #
        # # 计算吐司的 x 和 y 位置
        # x_position = top_center_point.x() - toast.width() // 2
        # y_position = top_center_point.y()
        # print(f"y_position{y_position}")
        # toast.showTopToBottomToast(x_position, y_position)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Demo()
    window.show()
    sys.exit(app.exec_())
