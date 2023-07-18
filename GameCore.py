"""
游戏核心类：描述游戏的逻辑
需要一种数据格式来存储棋盘信息：判断输赢
每次落子都更新这个棋盘信息，并且判断输赢
重置游戏：将棋盘信息清空
悔棋：将棋盘中最后一颗棋子拿掉

"""
from PyQt5.QtCore import QObject


class GameCore(QObject):
    """
    游戏核心类：
    使用二维列表记录棋盘信息，判断游戏输赢，重置棋盘，每次落子更新棋盘信息，悔棋
    """
    def __init__(self):
        super(GameCore, self).__init__()
        # 创建一个二维列表（空棋盘）
        # self.chessboard = []
        # for i in range(19):
        #     row = []
        #     for j in range(19):
        #         row.append(None)
        #     self.chessboard.append(row)
        self.chessboard = [[None for _ in range(19)] for _ in range(19)]

    def print_chessboard(self):
        print(self.chessboard)

    def init_game(self):
        """
        初始化游戏
        :return:
        """
        # self.chessboard = [[None for _ in range(19)] for _ in range(19)]
        for i in range(19):
            for j in range(19):
                self.chessboard[i][j] = None

    def regret(self, x: int, y: int):
        """
        悔棋:传入悔掉哪个位置的棋子
        :param x: 横坐标
        :param y: 纵坐标
        :return: bool 悔棋成功与否
        """
        # 当棋盘中没有棋子时悔棋失败 当传入x y位置没有棋子悔棋失败
        if self.chessboard[y][x] is None:
            return False
        else:
            # 当前位置有棋子
            self.chessboard[y][x] = None
            return True

    def down_chessman(self, x: int, y: int, color: str):
        """
        落子：落子颜色，
        :param x:
        :param y:
        :param color: 落子坐标（棋盘坐标）
        :return:
        """
        # 判断当前位置是否有棋子，有则直接返回
        if self.chessboard[y][x] is not None:
            return
        self.chessboard[y][x] = color
        res = self.judge_win(x, y, color)
        return res

    def judge_win(self, x: int, y: int, color: str):
        """
        判断输赢：传入一个坐标，判断当前位置的 横向 纵向 斜向有无五子连珠
        :param x:
        :param y:
        :param color:
        :return: bool 游戏结束  或 游戏继续
        """
        # 判断横向上有无五子连珠
        count = 1  # 记录横向上有无五子连珠
        # 横向向右检索
        # 当前棋子坐标 x，y
        i = x + 1
        while i <= 18:
            if self.chessboard[y][i] is None or self.chessboard[y][i] != color:
                # 当前位置的棋子 右边第一个位置 没有棋子或这棋子颜色和当前棋子的颜色不一致
                # 表明右边没有棋子
                break
            # 右边第一个位置有颜色相同的棋子
            count += 1
            i += 1
        # 横向向左索引
        i = x - 1
        while i >= 0:
            if self.chessboard[y][i] is None or self.chessboard[y][i] != color:
                break
            # 否则左边还有红色棋子
            count += 1
            i -= 1  # 继续向左索引
        if count >= 5:
            # 已经构成五子连珠 返回胜利棋子的颜色
            return color

        # 纵向
        count = 1  # 初始化计数
        # 向上
        j = y - 1
        while j >= 0:
            if self.chessboard[j][x] is None or self.chessboard[j][x] != color:
                break
            count += 1
            j -= 1
        # 向下
        j = y + 1
        while j <= 18:
            if self.chessboard[j][x] is None or self.chessboard[j][x] != color:
                break
            count += 1
            j += 1
        if count >= 5:
            return color

        # 左斜/
        count = 1  # 初始化计数
        # 左斜：右斜向上/
        i = x + 1
        j = y - 1
        while i <= 18 and j >= 0:
            if self.chessboard[j][i] is None or self.chessboard[j][i] != color:
                break
            count += 1
            i += 1
            j -= 1
        # 左斜：左斜向下/
        i = x - 1
        j = y + 1
        while j <= 18 and i >= 0:
            if self.chessboard[j][i] is None or self.chessboard[j][i] != color:
                break
            count += 1
            j += 1
            i -= 1
        if count >= 5:
            return color

        # 右斜
        count = 1  # 初始化计数
        # 右斜：右斜向下\
        i = x + 1
        j = y + 1
        while i <= 18 and j <= 18:
            if self.chessboard[j][i] is None or self.chessboard[j][i] != color:
                break
            count += 1
            i += 1
            j += 1
        # 右斜：左斜向上\
        i = x - 1
        j = y - 1
        while j >= 0 and i >= 0:
            if self.chessboard[j][i] is None or self.chessboard[j][i] != color:
                break
            count += 1
            j -= 1
            i -= 1
        if count >= 5:
            return color

        # 如果没有判断出输赢 继续下棋
        return 'Down'


if __name__ == '__main__':
    game = GameCore()
    print(game.down_chessman(0, 0, 'Black'))
    print(game.down_chessman(0, 1, 'Black'))
    print(game.down_chessman(0, 2, 'Black'))
    print(game.down_chessman(0, 3, 'Black'))
    print(game.down_chessman(0, 4, 'Black'))
