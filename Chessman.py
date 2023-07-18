from PyQt5.QtWidgets import QLabel, QApplication
from PyQt5.QtGui import QPixmap
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import QPoint


class Chessman(QLabel):
    def __init__(self, color='black', parent=None):
        super(Chessman, self).__init__(parent=parent)
        # 存当前棋子颜色
        self.color = color

        # 设置棋子图片
        if self.color == 'black':
            self.chess = QPixmap('source/黑子.png')
        else:
            self.chess = QPixmap('source/白子.png')
        # 显示图片
        self.setPixmap(self.chess)
        # 设置棋子大小
        self.setFixedSize(self.chess.size())

        # 初始化棋子坐标位置
        self.x = 0
        self.y = 0

    def set_index(self, x, y):
        """
        用来设置棋子在棋盘中的位置
        :return:
        """
        self.x = x
        self.y = y

    def move(self, a0: QtCore.QPoint):
        super(Chessman, self).move(QPoint(a0.x() - 15, a0.y() - 15))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    chess = Chessman(color='white')
    # chess.move(QPoint(10, 20))
    chess.show()

    sys.exit(app.exec())
