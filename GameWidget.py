"""游戏界面类"""
import sys
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon, QPalette, QBrush, QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QLabel
from PyQt5.QtMultimedia import QSound
from Chessman import Chessman
from MyButton import MyButton
from PyQt5.QtCore import *


class GameWidget(QWidget):
    goback_clicked = pyqtSignal()
    start_clicked = pyqtSignal()
    regret_clicked = pyqtSignal()
    lose_clicked = pyqtSignal()
    # 点击棋盘信号
    position_signal = pyqtSignal(tuple)

    def __init__(self, parent=None):
        super(GameWidget, self).__init__(parent=parent)
        self.init_ui()  # 初始化ui
        self.create_button()  # 创建按钮
        self.goback_button = None
        self.start_button = None
        self.regret_button = None
        self.lose_button = None
        # 棋盘上的棋子可以用一个列表存储
        self.chessman_list = []
        # 定义输赢的标签
        self.win_label = QLabel(self)
        self.win_label.hide()  # 游戏刚开始时不显示(隐藏)

        # 落子标识
        self.focus_point = QLabel(self)
        self.focus_point.setPixmap(QPixmap('source/标识.png'))
        self.focus_point.setFixedSize(QPixmap('source/标识.png').size())
        self.focus_point.hide()

    def init_ui(self):
        # 设计当前窗口样式
        self.setFixedSize(QImage('source/游戏界面.png').size())  # 固定窗口大小
        # 调用move方法可以移动窗口的初始位置
        self.move(600, 200)
        # 设置标题
        self.setWindowTitle('五子棋')
        # 设置窗口的图标
        self.setWindowIcon(QIcon('source/icon.ico'))  # 参数必须是.ico文件

        # 放置背景图片
        # 画板 笔刷 把画板添加到窗口上
        palette = QPalette(self.palette())  # 生成一个画板对象
        brush = QBrush(QImage('source/游戏界面.png'))  # 创建笔刷
        palette.setBrush(QPalette.Background, brush)  # 用笔刷画背景
        # 将画板应用在窗口上
        self.setPalette(palette)

    def create_button(self):
        # 添加按钮
        self.goback_button = MyButton(
            'source/返回按钮_normal.png',
            'source/返回按钮_hover.png',
            'source/返回按钮_press.png',
            parent=self
        )
        self.goback_button.show()
        self.goback_button.move(665, 75)
        self.goback_button.clicked.connect(self.goback_clicked)

        self.start_button = MyButton(
            'source/开始按钮_normal.png',
            'source/开始按钮_hover.png',
            'source/开始按钮_press.png',
            parent=self
        )
        self.start_button.show()
        self.start_button.move(650, 200)
        self.start_button.clicked.connect(self.start_clicked)

        self.regret_button = MyButton(
            'source/悔棋按钮_normal.png',
            'source/悔棋按钮_hover.png',
            'source/悔棋按钮_press.png',
            parent=self
        )
        self.regret_button.show()
        self.regret_button.move(650, 285)
        self.regret_button.clicked.connect(self.regret_clicked)

        self.lose_button = MyButton(
            'source/认输按钮_normal.png',
            'source/认输按钮_hover.png',
            'source/认输按钮_press.png',
            parent=self
        )
        self.lose_button.show()
        self.lose_button.move(650, 370)
        self.lose_button.clicked.connect(self.lose_clicked)

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        # print(a0, a0.x(), a0.y())
        coord_x = a0.x()
        coord_y = a0.y()

        # 鼠标坐标 转成棋盘坐标
        pos = self.reverse_to_position((coord_x, coord_y))
        # 判断有没有拿到
        if pos == ():
            return
        else:
            # 拿到后
            self.position_signal.emit(pos)  # 释放信号

    @staticmethod
    def reverse_to_position(coordinate: tuple) -> tuple:
        """
        将鼠标坐标 转成棋盘坐标
        :return: 棋盘坐标,元组
        """
        # 拿到x和y
        x = coordinate[0]
        y = coordinate[1]
        # 并不是所有的鼠标坐标都要转换成棋盘坐标  只转化棋盘里的 保证鼠标点的位置在棋盘中
        # 605 >= x, y >= 35
        if x <= 35 or x >= 605 or y <= 35 or y >= 605:
            # 当上述条件有一个不满足 就说明点击位置在棋盘 外部
            return ()
        # 当前点击位置是有效位置
        # 将鼠标坐标转换成棋盘坐标
        pos_x = (x-35) // 30
        pos_y = (y-35) // 30
        # print(pos_x, pos_y)
        return pos_x, pos_y

    @staticmethod
    def reverse_to_coordinate(position: tuple) -> tuple:
        # 将棋盘位置转成鼠标位置，此时落子的话才能落到棋盘的对应位置上
        # 拿到x和y
        coord_x = position[0] * 30 + 50
        coord_y = position[1] * 30 + 50
        return coord_x, coord_y

    def reset(self):
        # 重置：将棋子列表中的所有棋子清空
        for chessman in self.chessman_list:
            chessman.close()  # 在界面上删除
        self.chessman_list.clear()  # 清空列表
        # 重置游戏 要将输赢判断结果和落子隐藏
        self.focus_point.hide()
        self.win_label.hide()

    def regret(self):
        # 悔棋：将最后的元素删除掉
        if len(self.chessman_list) == 0:
            return
        chessman = self.chessman_list.pop()  # 获取最后一颗棋子
        chessman.close()  # 从界面上删除
        del chessman  # 删除变量资源
        self.focus_point.hide()

    def show_win(self, color='black'):
        # 展示输赢结果
        if color == 'black':
            self.win_label.setPixmap(QPixmap('source/黑棋胜利.png'))
            self.win_label.move(10, 200)
        else:
            self.win_label.setPixmap(QPixmap('source/白棋胜利.png'))
            self.win_label.move(120, 200)  # 移动
        self.win_label.show()  # 显示
        self.win_label.raise_()  # 显示在最上层

    def down_chess(self, color: str, position: tuple):
        """
        落子
        :param color: 颜色
        :param position: 落子的位置
        :return:
        """
        # 根据颜色创建棋子对象
        chessman = Chessman(color=color, parent=self)
        # 设置棋子的坐标
        chessman.set_index(position[0], position[1])
        # 将棋盘位置转成坐标
        coord = QPoint(*self.reverse_to_coordinate(position))
        chessman.move(coord)  # 移动棋子  QWeight里自带的方法
        chessman.show()  # 展示棋子
        chessman.raise_()  # 至于上层
        # 落子的声音
        QSound.play('source/luozisheng.wav')
        # 落子后将棋子放在棋子列表中
        self.chessman_list.append(chessman)
        # 将落子标识显示出来
        self.focus_point.move(coord.x()-15, coord.y()-15)
        self.focus_point.show()
        self.focus_point.raise_()


def test():
    print('11111')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 创建菜单窗口对象
    game = GameWidget()
    # 展示窗口
    game.show()
    game.start_clicked.connect(game.reset)
    game.goback_clicked.connect(test)
    game.regret_clicked.connect(game.regret)
    game.lose_clicked.connect(game.show_win)
    # game.position_signal.connect(test)
    # game.show_win('black')
    game.down_chess(color='black', position=(0, 0))
    game.down_chess(color='black', position=(10, 0))
    game.down_chess(color='black', position=(0, 10))
    game.down_chess(color='black', position=(10, 10))
    sys.exit(app.exec())
