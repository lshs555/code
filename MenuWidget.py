from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QIcon, QPalette, QBrush, QImage
import sys
from MyButton import MyButton
from PyQt5.QtCore import *


class MenuWidget(QWidget):
    single_clicked = pyqtSignal()
    double_clicked = pyqtSignal()
    network_clicked = pyqtSignal()

    def __init__(self, parent=None):
        # parent=None  无父窗口
        super(MenuWidget, self).__init__(parent=parent)
        self.network_button = None
        self.double_button = None
        self.single_button = None
        self.init_ui()
        self.create_button()

    def init_ui(self):
        # 设计当前窗口样式
        self.setFixedSize(QImage('source/五子棋界面.png').size())  # 固定窗口大小
        # 调用move方法可以移动窗口的初始位置
        self.move(600, 200)
        # 设置标题
        self.setWindowTitle('五子棋')
        # 设置窗口的图标
        self.setWindowIcon(QIcon('source/icon.ico'))  # 参数必须是.ico文件
        # 放置背景图片
        # 画板 笔刷 把画板添加到窗口上
        palette = QPalette(self.palette())  # 生成一个画板对象
        brush = QBrush(QImage('source/五子棋界面.png'))  # 创建笔刷
        palette.setBrush(QPalette.Background, brush)  # 用笔刷画背景
        # 将画板应用在窗口上
        self.setPalette(palette)

    def create_button(self):
        # 添加按钮
        self.single_button = MyButton(
            'source/人机对战_normal.png',
            'source/人机对战_hover.png',
            'source/人机对战_press.png',
            parent=self
        )
        self.single_button.show()
        self.single_button.move(300, 200)
        self.single_button.clicked.connect(self.single_clicked)

        self.double_button = MyButton(
            'source/双人对战_normal.png',
            'source/双人对战_hover.png',
            'source/双人对战_press.png',
            parent=self
        )
        self.double_button.show()
        self.double_button.move(300, 325)
        self.double_button.clicked.connect(self.double_clicked)

        self.network_button = MyButton(
            'source/联机对战_normal.png',
            'source/联机对战_hover.png',
            'source/联机对战_press.png',
            parent=self
        )
        self.network_button.show()
        self.network_button.move(300, 450)
        self.network_button.clicked.connect(self.network_clicked)


def test1():
    print('人机对战被点击')


def test2():
    print('双人对战被点击')


def test3():
    print('联机对战被点击')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 创建菜单窗口对象
    menu = MenuWidget()
    # 展示窗口
    menu.show()
    # 测试信号
    menu.single_clicked.connect(test1)
    menu.double_clicked.connect(test2)
    menu.network_clicked.connect(test3)
    sys.exit(app.exec())
