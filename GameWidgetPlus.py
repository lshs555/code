"""
游戏界面添加了催促按钮的模块
"""
import sys
from GameWidget import GameWidget
from MyButton import MyButton
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication


class GameWidgetPlus(GameWidget):
    urge_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super(GameWidgetPlus, self).__init__(parent=parent)
        self.urge_button = None

    def create_button(self):
        super(GameWidgetPlus, self).create_button()
        self.urge_button = MyButton(
            'source/催促按钮_normal.png',
            'source/催促按钮_hover.png',
            'source/催促按钮_press.png',
            parent=self
        )
        self.urge_button.show()
        self.urge_button.move(650, 455)
        self.urge_button.clicked.connect(self.urge_clicked)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = GameWidgetPlus()
    game.show()
    sys.exit(app.exec())
