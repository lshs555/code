"""
主函数：创建游戏
打开游戏菜单
点击按钮能跳转到对应的模块中
捕获退出事件
"""
from PyQt5.QtCore import QObject
from MenuWidget import MenuWidget
from DoublePlayer import DoublePlayer
from SinglePlayer import SinglePlayer
from PyQt5.QtWidgets import QApplication
import sys
from NetPlayer import NetPlayer


class Main(QObject):
    def __init__(self):
        super(Main, self).__init__()
        self.menuWidget = MenuWidget()
        self.double_play = DoublePlayer()
        self.menuWidget.double_clicked.connect(self.start_double_play)
        self.double_play.exit_game.connect(self.start_program)

        self.single_play = SinglePlayer()
        self.menuWidget.single_clicked.connect(self.start_single_play)
        self.single_play.exit_game.connect(self.start_program)

        self.net_work = NetPlayer()
        self.menuWidget.network_clicked.connect(self.start_network_player)
        self.net_work.exit_clicked.connect(self.start_program)

    def start_network_player(self):
        # 启动人机游戏
        self.net_work.start_game()
        # 将菜单界面隐藏起来
        self.menuWidget.hide()

    def start_double_play(self):
        # 启动双人游戏
        self.double_play.enter_game()
        # 将菜单界面隐藏起来
        self.menuWidget.hide()

    def start_single_play(self):
        # 启动人机游戏
        self.single_play.enter_game()
        # 将菜单界面隐藏起来
        self.menuWidget.hide()

    def start_program(self):
        # 启动程序
        self.menuWidget.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Main()
    game.start_program()
    sys.exit(app.exec())
