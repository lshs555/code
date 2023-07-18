"""
人机对战类:人机对战
游戏的初始化
落子 玩家落子和电脑落子
判断输赢
切换棋子颜色
继续落子
游戏结束 退出到菜单界面
"""
import sys
from PyQt5.QtWidgets import QApplication
from DoublePlayer import DoublePlayer
from FiveAlgorithm import Algorithm


class SinglePlayer(DoublePlayer):
    def __init__(self):
        super(SinglePlayer, self).__init__()

    def down_chess(self, position: tuple):
        """
        重写落子方法：人机对战
        保证当前在游戏中
        核心类 用来落子 拿到结果：有胜负 没有胜负 None
        :param position: 落子的棋盘坐标
        :return:
        """
        if self.is_active is False:
            return
        res = self.game_core.down_chessman(
            x=position[0],
            y=position[1],
            color=self.current_color
        )
        if res is None:
            return
        # 成功落子
        # 添加记录
        self.history.append(position)
        # 显示棋子
        self.game_widget.down_chess(color=self.current_color, position=position)
        # 判断输赢
        if res == 'Down':
            # 继续落子
            self.switch_color()
            self.computer_down_chess()  # 让电脑落子
            return
        # 有输赢
        self.game_win(res)

    def computer_down_chess(self):
        # 电脑落子
        # 随机选择一个位置 落子到这个位置 核心类的判断 显示棋子 在history中添加棋子信息 判断当前游戏是否结束 有胜利显示胜利 没有胜利继续让人落子
        # 判断当前在游戏中
        if self.is_active is False:
            return
        position = Algorithm(self.game_core.chessboard).get_point
        res = self.game_core.down_chessman(
            x=position[0],
            y=position[1],
            color=self.current_color
        )
        if res is None:  # 落子失败
            return
        self.history.append(position)
        self.game_widget.down_chess(color=self.current_color, position=position)
        if res == 'Down':
            # 游戏继续
            self.switch_color()
            # 让玩家玩
            return
        self.game_win(res)

    def regret_chess(self):
        # 悔棋：当前在游戏中
        if self.is_active is False:  # 不在游戏中不能悔棋
            return
        # 少于两个棋子不能悔棋
        if len(self.history) <= 2:
            return
        # 一次性悔掉两个棋子
        for _ in range(2):
            # 在history中删除
            position = self.history.pop()  # 要悔掉棋子的棋盘坐标
            # 在game中悔棋
            res = self.game_core.regret(*position)  # True/False
            if res is False:
                return
            # 可以悔棋 在界面上删除棋子
            self.game_widget.regret()
            # self.switch_color()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = SinglePlayer()
    game.start_game()
    sys.exit(app.exec())
