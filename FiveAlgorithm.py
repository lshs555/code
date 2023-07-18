from PyQt5.QtCore import QObject


# 人机算法
class Algorithm(QObject):
    def __init__(self, chessboard):
        """
        构造函数
        :param chessboard: 传入的时当前的棋盘  二位列表
        """
        super(Algorithm, self).__init__()
        self.chessboard = chessboard

    # 随机算法
    # 在棋盘列表中随机选一个空位置 返回这个空位置的坐标
    # 电脑：如何自己连成五子  防止玩家连成五子
    @property
    def get_point(self):
        # # 返回当前棋盘中的随机的一个空位置None
        # while True:
        #     x_com = random.randint(0, 18)  # 唯一一个不是左闭右开的方法
        #     y_com = random.randint(0, 18)
        #     if self.chessboard[y_com][x_com] is None:
        #         return x_com, y_com
        # 记录白棋的分数
        white_score = [[0 for _ in range(19)] for _ in range(19)]
        # 记录黑棋的分数
        black_score = [[0 for _ in range(19)] for _ in range(19)]

        # 遍历棋盘上所有空位，在每个位置模拟落子
        # 每一行
        for j in range(19):
            # 每一列
            for i in range(19):
                if self.chessboard[j][i] is None:
                    # 当前位置是空的
                    # 模拟落白子
                    self.chessboard[j][i] = 'white'
                    # 落子后判断 当前位置落 白子 分数是多少
                    white_score[j][i] = self.get_point_score(x=i, y=j, color='white')
                    self.chessboard[j][i] = None
                    # 模拟落黑子
                    self.chessboard[j][i] = 'black'
                    black_score[j][i] = self.get_point_score(x=i, y=j, color='black')
                    self.chessboard[j][i] = None
        # 将二维列表转换成一维列表 找到最大值 再复原该位置的坐标
        r_white_score = []
        r_black_score = []
        for i in white_score:
            r_white_score.extend(i)
        for j in black_score:
            r_black_score.extend(j)
        # 电脑落子是白子
        # 将两个棋盘合并 优先取最大值的方式
        # score_list = []  # 合并后的总棋盘
        # for i in range(19 * 19):
        #     if r_white_score[i] > r_black_score[i]:
        #         score_list.append(r_white_score[i])
        #     else:
        #         score_list.append(r_black_score[i])
        score_list = [max(x, y) for x, y in zip(r_white_score, r_black_score)]
        # 找到当前列表中的最大值和其下标
        index = score_list.index(max(score_list))
        # 2, 1   21
        # 1, 1   20
        # 0, 1   19
        x = index % 19
        y = index // 19
        return x, y

    def get_point_score(self, x, y, color):
        """
        返回得分：传入一个点坐标 和对应的颜色 分析战局 计算该棋子在当前点位下棋的话 能得的分数（竖直，水平，左斜，右斜）
        :param x: 横坐标
        :param y: 纵坐标
        :param color: 模拟棋子颜色
        :return: 返回最大分数
        """
        # 用来存储当前颜色棋子 的四个分数 每条线上的分数 （相邻的同色棋子的个数）
        color_score = [0, 0, 0, 0]  # - | / \
        blank_score = [0, 0, 0, 0]  # 空白棋子也可以算一分（计算之后就会停）
        # 统计每条线上棋子 的分数（五子之内）
        # 横向为例-------------------------------------------------
        # 从当前坐标节点开始寻找
        # 向右寻找
        # 判断棋子颜色color
        # 赵第一个相邻的棋子颜色是否同色  如果是同色棋子 加一分 color_score
        # 继续向右寻找，直到出现异色棋子或者空白（终止条件）

        # 如果找到棋子的颜色是异色的直接终止
        # 如果找到的是None 空位置 让blank_score加一 终止寻找
        # 横纵坐标i，j
        i = x  # 列
        j = y  # 行
        while i <= 18:
            if self.chessboard[j][i] == color:
                # color_score 分数加一分
                color_score[0] += 1
            elif self.chessboard[j][i] is None:
                # 遇到空白位置 空白分数加一分
                blank_score[0] += 1
                break
            else:
                # 遇到异色棋子
                break
            # 在五个子内遍历
            if i >= x+5:
                break
            i += 1

        # 向左寻找
        i = x  # 列
        j = y  # 行
        while i >= 0:
            if self.chessboard[j][i] == color:
                color_score[0] += 1
            elif self.chessboard[j][i] is None:
                blank_score[0] += 1
                break
            else:
                break
            if i <= x-5:
                break
            i -= 1  # 继续循环 直到退出循环

        # ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||纵向
        i = x  # 列
        j = y  # 行
        # 向下寻找
        while j <= 18:
            if self.chessboard[j][i] == color:
                # color_score 分数加一分
                color_score[1] += 1
            elif self.chessboard[j][i] is None:
                # 遇到空白位置 空白分数加一分
                blank_score[1] += 1
                break
            else:
                # 遇到异色棋子
                break
            # 在五个子内遍历
            if j >= y + 5:
                break
            j += 1

        # 向上寻找
        i = x  # 列
        j = y  # 行
        while j >= 0:
            if self.chessboard[j][i] == color:
                color_score[1] += 1
            elif self.chessboard[j][i] is None:
                blank_score[1] += 1
                break
            else:
                break
            if j <= y - 5:
                break
            j -= 1  # 继续循环 直到退出循环

        # //////////////////////////////////////////////////////////斜向上
        i = x  # 列
        j = y  # 行
        # 向右上寻找
        while j >= 0 and i <= 18:
            if self.chessboard[j][i] == color:
                # color_score 分数加一分
                color_score[2] += 1
            elif self.chessboard[j][i] is None:
                # 遇到空白位置 空白分数加一分
                blank_score[2] += 1
                break
            else:
                # 遇到异色棋子
                break
            # 在五个子内遍历
            if j <= y - 5:  # or i >= x + 5:
                break
            j -= 1
            i += 1

        # 向左下寻找
        i = x  # 列
        j = y  # 行
        while j <= 18 and i >= 0:
            if self.chessboard[j][i] == color:
                color_score[2] += 1
            elif self.chessboard[j][i] is None:
                blank_score[2] += 1
                break
            else:
                break
            if j >= y + 5:  # or i <= x - 5:
                break
            j += 1  # 继续循环 直到退出循环
            i -= 1

        # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\斜向下
        i = x  # 列
        j = y  # 行
        # 向左上寻找
        while j >= 0 and i >= 0:
            if self.chessboard[j][i] == color:
                # color_score 分数加一分
                color_score[3] += 1
            elif self.chessboard[j][i] is None:
                # 遇到空白位置 空白分数加一分
                blank_score[3] += 1
                break
            else:
                # 遇到异色棋子
                break
            # 在五个子内遍历
            if j <= y - 5:  # or i >= x + 5:
                break
            j -= 1
            i -= 1

        # 向右下寻找
        i = x  # 列
        j = y  # 行
        while j <= 18 and i <= 18:
            if self.chessboard[j][i] == color:
                color_score[3] += 1
            elif self.chessboard[j][i] is None:
                blank_score[3] += 1
                break
            else:
                break
            if j >= y + 5:  # or i <= x - 5:
                break
            j += 1  # 继续循环 直到退出循环
            i += 1

        # 如果color_score 某一个维度的分数大于等于5 此时就已经有结果了
        # 返回很大的一个数
        for i in color_score:
            if i > 5:
                return 1000
        score = [color_score[i] + blank_score[i] for i in range(4)]
        return max(score)
