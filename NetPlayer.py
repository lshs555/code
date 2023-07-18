"""
联机对战
"""
import json
import sys

from PyQt5.QtMultimedia import QSound
from GameWidgetPlus import GameWidgetPlus
from GameCore import GameCore
from NetConfigWidget import NetConfigWidget, NetClient, NetServer
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMessageBox, QApplication


class NetPlayer(QObject):
    exit_clicked = pyqtSignal()  # 结束游戏的信号  游戏返回时抛出

    def __init__(self, parent=None):
        super(NetPlayer, self).__init__(parent=parent)
        # 游戏界面
        self.game_widget = GameWidgetPlus()
        # 游戏核心 输赢判断
        self.game_core = GameCore()
        # 网络配置对话框
        self.netconfig = NetConfigWidget()
        # 棋子的颜色
        self.m_color = 'black'
        # 当前游戏状态
        self.is_active = False
        # 存储棋子的历史列表
        self.history = []  # 落子历史记录
        # 创建套接字对象
        self.net_object = None  # 初始值为None
        # 绑定
        self.netconfig.config_signal.connect(self.receive_config)
        self.netconfig.exit_signal.connect(self.exit_clicked)

        self.game_widget.goback_clicked.connect(self.stop_game)
        self.game_widget.start_clicked.connect(self.restart)
        self.game_widget.lose_clicked.connect(self.lose_game)
        self.game_widget.regret_clicked.connect(self.regret_game)
        self.game_widget.urge_clicked.connect(self.urge)
        self.game_widget.position_signal.connect(self.down_chess)

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

    # 展示网络配置窗口
    def start_game(self):
        # 点击菜单中的联机对战 展示网络配置界面
        self.netconfig.show()

    def receive_config(self, net_type, name, ip, port):
        """
        接收配置进行网络对象的配置
        展示游戏界面  建立tcp连接  动态的创建
        服务器：build_listen  绑定自己的ip地址 进入监听 接收消息
        客户端：build_connect  连接服务器 接收消息
        :param net_type: 网络类型 server client
        :param name: 输入框中的name
        :param ip: IP地址
        :param port: 端口号
        :return:
        """
        if net_type == 'client':
            # 表示点击了连接主机按钮
            self.net_object = NetClient(name=name, ip=ip, port=port)
        elif net_type == 'server':
            self.net_object = NetServer(name=name, ip=ip, port=port)
        else:
            return

        self.game_widget.show()
        # 连接tcp
        self.net_object.build_connect()  # 多态
        self.net_object.msg_signal.connect(self.parse)  # 将接收到的信号绑定处理函数
        # 将配置界面隐藏
        self.netconfig.hide()

    # 开始游戏 初始化游戏
    def _start_game(self):
        # 初始化游戏 界面初始化 核心初始化  棋盘初始化 状态调整为True
        self.init_game()
        self.is_active = True

    def init_game(self):
        # 初始化游戏界面 初始化游戏逻辑 history清空 默认棋子设置为黑色
        self.game_widget.reset()
        self.game_core.init_game()
        self.history.clear()
        self.current_color = 'black'

    def stop_game(self):
        # 结束游戏：关闭窗口 释放结束信号 关闭套接字对象并删除资源 将网络对象设置为None
        self.game_widget.close()
        self.exit_clicked.emit()
        self.net_object.close()  # 关闭当前套接字对象
        del self.net_object
        self.net_object = None

    # 落子
    def down_chess(self, position):
        if self.is_active is False:  # 判断当前是否在游戏中
            return
        # 判断当前棋子颜色和我的棋子颜色是否一致 如果一致才能落子
        if self.m_color != self.current_color:
            return
        res = self.game_core.down_chessman(x=position[0], y=position[1], color=self.current_color)
        if res is None:  # 落子失败
            return
        # 落子成功
        self.game_widget.down_chess(color=self.m_color, position=position)
        # 添加历史记录
        self.history.append(position)
        self.switch_color()  # 转换棋子颜色
        if res != 'Down':
            # 有结果
            self.game_win(res)
        # 游戏没有胜利的一方 发出一个数据 在对面棋盘展示落子
        msg = {'msg_type': 'position',
               'x': position[0],
               'y': position[1]}  # 用来存放发出的数据
        self.net_object.send(json.dumps(msg))  # json.loads()

    # 对手落棋
    def _down_chess(self, position):
        if self.is_active is False:
            return
        res = self.game_core.down_chessman(position[0], position[1], self.current_color)
        # 服务器 self.current_color
        if res is None:
            return
        self.game_widget.down_chess(self.current_color, position)
        self.history.append(position)  # 添加对手的棋子
        self.switch_color()
        if res != 'Down':
            self.game_widget.show_win(res)

    # 判断输赢
    def game_win(self, color):
        self.game_widget.show_win(color=color)
        self.is_active = False

    # 悔棋
    def regret_game(self):
        # 判断是否在游戏中
        if self.is_active is False:
            return
        # 判断是否是我的回合 如果不是我的回合 就不能悔棋
        if self.m_color != self.current_color:
            # 弹出消息框 当前不是你的回合 不能悔棋
            QMessageBox.warning(self.game_widget, '消息提示', '当前不是你的回合 不能悔棋')
            return
        # 保证界面上至少有一个棋子
        if len(self.history) <= 1:
            return
        # 发送悔棋请求
        msg = {'msg_type': 'regret'}
        self.net_object.send(json.dumps(msg))

    # 接收悔棋
    def _regret_game(self):
        # 同意悔棋之后调用方法
        # 判断是否在游戏中
        if self.is_active is False:
            return
        # 保证界面上至少有一个棋子
        if len(self.history) <= 1:
            return
        # 悔两颗棋子`
        for _ in range(2):
            position = self.history.pop()
            if not self.game_core.regret(position[0], position[1]):
                return
            self.game_widget.regret()

    # 认输
    def lose_game(self):
        self.game_win(self.get_reverse_color(self.m_color))
        msg = {'msg_type': 'lose'}
        self.net_object.send(json.dumps(msg))

    def restart(self):
        # 重新开始游戏
        msg = {'msg_type': 'restart'}
        self.net_object.send(json.dumps(msg))

    def urge(self):
        # 催促按钮
        # 播放声音
        if self.is_active is False:
            return
        QSound.play('source/cuicu.wav')
        # 发送催促消息
        msg = {'msg_type': 'urge'}
        self.net_object.send(json.dumps(msg))

    def parse(self, data):
        # 拿到消息 做出不同的处理
        try:
            msg = json.loads(data)
        except Exception as e:
            print('错误的消息类型:', e)
            return
        if msg['msg_type'] == 'position':
            self._down_chess(position=(msg['x'], msg['y']))
        elif msg['msg_type'] == 'restart':
            result = QMessageBox.information(self.game_widget, '开始游戏提示', '对方请求开始游戏，是否同意？',
                                             QMessageBox.Yes | QMessageBox.No)
            if result == QMessageBox.Yes:
                # 同意开始游戏
                # 我开始游戏
                self._start_game()
                self.m_color = 'white'  # 切换对手棋子颜色
                # 组织数据发送给对方 对方也开始游戏
                msg = {'msg_type': 'response', 'action': 'restart', 'action_result': 'Yes'}
                self.net_object.send(json.dumps(msg))
            elif result == QMessageBox.No:
                # 不同意
                msg = {'msg_type': 'response', 'action': 'restart', 'action_result': 'No'}
                self.net_object.send(json.dumps(msg))

        elif msg['msg_type'] == 'regret':
            result = QMessageBox.information(self.game_widget, '悔棋请求', '对方请求悔棋，你是否同意？',
                                             QMessageBox.Yes | QMessageBox.No)
            if result == QMessageBox.Yes:
                # 同意悔棋
                self._regret_game()
                # 发送相应
                msg = {'msg_type': 'response', 'action': 'regret', 'action_result': 'Yes'}
                self.net_object.send(json.dumps(msg))
            else:
                # 不同意
                msg = {'msg_type': 'response', 'action': 'regret', 'action_result': 'No'}
                self.net_object.send(json.dumps(msg))
        elif msg['msg_type'] == 'lose':
            self.game_win(self.m_color)
        elif msg['msg_type'] == 'response':
            if msg['action'] == 'restart':
                # 重开游戏响应
                if msg['action_result'] == 'Yes':
                    self._start_game()
                    self.m_color = 'black'
                else:
                    QMessageBox.warning(self.game_widget, '消息提示', '对方拒绝重新开始')

            elif msg['action'] == 'regret':
                if msg['action_result'] == 'Yes':
                    # 同意悔棋
                    self._regret_game()
                else:
                    # 不同意悔棋
                    QMessageBox.warning(self.game_widget, '消息提示', '对方拒绝悔棋')

        elif msg['msg_type'] == 'urge':
            QSound.play('source/cuicu.wav')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = NetPlayer()
    game.start_game()
    sys.exit(app.exec())
