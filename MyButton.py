from PyQt5.QtWidgets import QLabel, QApplication, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui
from PyQt5 import QtCore
import sys
from PyQt5.QtCore import *


# 按钮类
class MyButton(QLabel):
    # 信号机制
    clicked = pyqtSignal()

    def __init__(self, *args, parent=None):
        super(MyButton, self).__init__(parent)
        self.normal = QPixmap(args[0])
        self.hover = QPixmap(args[1])
        self.press = QPixmap(args[2])
        self.setPixmap(self.normal)  # 设置默认图片
        self.enterState = False  # 鼠标位置的状态 按钮上方？ 还是在按钮外部？
        # 定义按钮大小:图片的尺寸
        self.setFixedSize(self.normal.size())

    def mousePressEvent(self, ev: QtGui.QMouseEvent):
        # 鼠标按压事件
        # print('鼠标按压')
        self.setPixmap(self.press)

    def mouseReleaseEvent(self, ev: QtGui.QMouseEvent):
        # 鼠标释放事件
        # print('鼠标释放')
        self.setPixmap(self.hover)
        if self.enterState:
            self.setPixmap(self.hover)
        else:
            self.setPixmap(self.normal)
        self.clicked.emit()  # 当鼠标释放之后 将信号释放

    def enterEvent(self, a0: QtCore.QEvent):
        # 鼠标进入事件
        # print('鼠标进入')
        self.setPixmap(self.hover)
        self.enterState = True

    def leaveEvent(self, a0: QtCore.QEvent):
        # 鼠标移开事件
        # print('鼠标移开')
        self.setPixmap(self.normal)
        self.enterState = False


# 鼠标时间有哪些：
# 鼠标进入
# 鼠标移开
# 鼠标按下
# 鼠标释放
def test():
    print('检测到信号')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    windows = QWidget()  # 实例化一个窗口对象
    windows.setWindowTitle('测试窗口')  # 设置窗口的标题
    # windows.setGeometry(300, 300, 600, 600)  # 设置窗口的大小  单位像素
    # 固定窗口大小
    windows.setFixedSize(600, 300)

    # 创建一个按钮
    myBut = MyButton(
        'source/人机对战_normal.png',
        'source/人机对战_hover.png',
        'source/人机对战_press.png',
        parent=windows)
    myBut.move(200, 200)
    myBut.clicked.connect(test)
    windows.show()  # 展示窗口
    # # 展示按钮
    myBut.show()
    sys.exit(app.exec())
