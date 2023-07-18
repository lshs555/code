"""
双人对战类:双人对战
游戏的初始化
落子
判断输赢
切换棋子颜色
继续落子
游戏结束 退出到菜单界面
"""
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import QApplication
from GameWidget import GameWidget
from GameCore import GameCore
import sys


class DoublePlayer(QObject):
    # 定义退出信号
    exit_game = pyqtSignal()

    def __init__(self, parent=None):
        super(DoublePlayer, self).__init__(parent=parent)
        # 实例化一个游戏界面
        self.game_widget = GameWidget()
        # 游戏核心
        self.game_core = GameCore()
        # 初始化棋子颜色
        self.current_color = 'black'
        # 记录当前的游戏状态 进行中  未开始/已结束
        self.is_active = False  # 默认未开始
        # 列表 记录当前的棋局
        self.history = []  # 落子历史记录
        # 绑定按钮
        # 点击返回按钮之后 释放信号关闭页面
        self.game_widget.goback_clicked.connect(self.stop_game)
        # 开始
        self.game_widget.start_clicked.connect(self.start_game)
        # 悔棋
        self.game_widget.regret_clicked.connect(self.regret_chess)
        # 认输
        self.game_widget.lose_clicked.connect(self.lose_game)
        # 落子
        self.game_widget.position_signal.connect(self.down_chess)
        # 背景音乐
        self.music = QSound('source/bg_music.wav')

    @staticmethod
    def get_reverse_color(color: str) -> str:
        # 传入一个颜色 返回另一个颜色
        if color == 'black':
            return 'white'
        else:
            return 'black'

    def switch_color(self):
        # 转换当前棋子的颜色
        self.current_color = self.get_reverse_color(self.current_color)

    def stop_game(self):
        # 游戏结束 将当前的窗口关闭 退回到菜单界面
        # 需要借助信号 exit_game
        # 执行方法时 释放信号
        self.exit_game.emit()
        # 关掉当前游戏窗口
        self.game_widget.close()
        # 关闭背景音乐
        self.music.stop()

    def start_game(self):
        # 开始游戏：
        self.init_game()  # 初始化游戏
        # 改变游戏状态 is_active
        self.is_active = True

    def enter_game(self):
        # 开始游戏：
        self.init_game()  # 初始化游戏
        # 显示游戏窗口
        self.game_widget.show()
        # 播放背景音乐
        self.music.play()

    def init_game(self):
        # 初始化游戏界面 初始化游戏逻辑 history清空 默认棋子设置为黑色
        self.game_widget.reset()
        self.game_core.init_game()
        self.history.clear()
        self.current_color = 'black'

    def down_chess(self, position: tuple):
        # 状态位 is_active 判断当前游戏是否正在进行 若进行即可落子 否则返回
        # 落子： 游戏核心类落子 界面落子
        if self.is_active is False:
            return
        # 从信号中拿到 position 坐标元组
        res = self.game_core.down_chessman(
            x=position[0],
            y=position[1],
            color=self.current_color)
        # res 有三种结果 black write Down
        # print(res)
        # 判断当前的落子是否成功
        if res is None:
            return
        # 落子成功
        # 添加到历史记录里
        self.history.append(position)
        # 显示落子
        self.game_widget.down_chess(color=self.current_color, position=position)
        # 对落子的结果判断
        if res == 'Down':
            # 没有输赢
            # 换颜色 继续落子
            self.switch_color()
            return
        # 出现了胜利的一方 res返回的一方
        # 展示胜利的一方
        self.game_win(res)

    def game_win(self, res):
        # 游戏胜利：将游戏状态转为已结束 展示胜利标签
        self.is_active = False
        self.game_widget.show_win(color=res)

    def regret_chess(self):
        # 悔棋：当前在游戏中
        if self.is_active is False:  # 不在游戏中不能悔棋
            return
        # 少于两个棋子不能悔棋
        if len(self.history) <= 2:
            return
        # 一次性悔掉一个棋子
        for _ in range(1):
            # 在history中删除
            position = self.history.pop()  # 要悔掉棋子的棋盘坐标
            # 在game中悔棋
            res = self.game_core.regret(*position)  # True/False
            if res is False:
                return
            # 可以悔棋 在界面上删除棋子
            self.game_widget.regret()
            self.switch_color()

    def lose_game(self):
        # 认输：检查游戏状态 改变游戏状态 贴图（棋子转换）
        if self.is_active is False:
            return
        self.is_active = False
        self.game_widget.show_win(self.get_reverse_color(self.current_color))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = DoublePlayer()
    game.start_game()
    sys.exit(app.exec())
