"""
网络配置窗口模块：配置网络连接
配置：姓名 ip地址 端口号  使用服务器 或 客户端模式
"""
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QApplication
import sys
from PyQt5.QtCore import *
from PyQt5.QtCore import QObject
import socket
import threading


class NetConfigWidget(QWidget):
    # 服务器按钮信号
    # 客户端按钮信号
    # 由于界面一开始不清楚是主机还是服务器  所以动态创建信号
    config_signal = pyqtSignal(str, str, str, str)  # 信号会携带参数当前是主机还是客户端 姓名 ip 端口号
    # 退出信号
    exit_signal = pyqtSignal()  # 当遇到退出事件时

    def __init__(self, parent=None):
        super(NetConfigWidget, self).__init__(parent=parent)
        self.server_button = None
        self.client_button = None
        self.port_input = None
        self.port_label = None
        self.ip_input = None
        self.ip_label = None
        self.name_input = None
        self.name_label = None
        self.init_ui()

    def init_ui(self):
        # 创建title 姓名 ip 端口号 按钮组件 并把他设置到窗口上
        self.setWindowTitle('网络配置')
        # 构造组件
        self.name_label = QLabel('姓  名：', parent=self)  # 纯文本
        self.name_input = QLineEdit('独孤求败', parent=self)  # 输入框  默认显示的值 和 父窗口
        self.ip_label = QLabel('ip地址：', parent=self)
        self.ip_input = QLineEdit('127.0.0.1', parent=self)
        self.port_label = QLabel('端口号：', parent=self)
        self.port_input = QLineEdit('8899', parent=self)
        # 客户端模式
        self.client_button = QPushButton('连接主机', parent=self)
        # 服务器模式
        self.server_button = QPushButton('我是主机', parent=self)

        # 将组件放在窗口中，使用网格将组件放在对应的位置上 然后应用到窗口中
        # 创建网格
        qgridlayout = QGridLayout()
        qgridlayout.addWidget(self.name_label, 0, 0)  # 0行0列
        qgridlayout.addWidget(self.name_input, 0, 1)  # 0行1列
        qgridlayout.addWidget(self.ip_label, 1, 0)
        qgridlayout.addWidget(self.ip_input, 1, 1)
        qgridlayout.addWidget(self.port_label, 2, 0)
        qgridlayout.addWidget(self.port_input, 2, 1)
        qgridlayout.addWidget(self.client_button, 3, 0)
        qgridlayout.addWidget(self.server_button, 3, 1)
        self.setLayout(qgridlayout)  # 设置窗口布局

        self.client_button.clicked.connect(self.client_connect_signal)
        self.server_button.clicked.connect(self.server_connect_signal)

    def client_connect_signal(self):
        # 当点击 连接主机 按钮是要绑定的方法
        # 功能 释放信号
        self.config_signal.emit(
            'client',
            self.name_input.text(),
            self.ip_input.text(),
            self.port_input.text()
        )
        print('client')

    def server_connect_signal(self):
        # 当点击 我是主机 按钮是要绑定的方法
        # 功能 释放信号
        self.config_signal.emit(
            'server',
            self.name_input.text(),
            self.ip_input.text(),
            self.port_input.text()
        )
        print('server')

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.close()  # 如果没有正常关闭 则主动关闭窗口
        self.exit_signal.emit()


# 服务器类
class NetServer(QObject):
    msg_signal = pyqtSignal(str)  # 服务器接收的客户端数据信号  str:数据内容
    """
    tcp
    有自己的ip 端口号 服务器名 该服务器所连接的客户端
    """
    def __init__(self, name, ip, port):
        super(NetServer, self).__init__()

        self.name = name
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket = None  # 客户端的socket

    def build_connect(self):
        # 构建监听事件
        self.socket.bind((self.ip, int(self.port)))  # ip:str   port:int
        self.socket.listen(1)  # 监听的数量
        # 使用线程方式开启函数
        th = threading.Thread(target=self.accept_connect)
        th.start()  # 开启线程 GIL
        # th.join()

    def accept_connect(self):
        # 接受客户端连接
        try:
            self.client_socket, addr = self.socket.accept()  # 接收连接
        except Exception as e:
            print('错误信息是：', e)
        while True:
            try:
                data = self.client_socket.recv(4096).decode()  # 接收客户端数据
                self.msg_signal.emit(data)  # 释放信号 告诉外部接收到了data
            except Exception as e:
                print('错误信息是：', e)

    def send(self, data):
        """
        将数据发送回客户端
        :param data: 服务器发送给客户端的数据
        :return:
        """
        # 保证有客户端是连接
        if self.client_socket is None:
            return
        self.client_socket.send(data.encode())  # 加密并发送

    def close(self):
        # 关闭当前的套接字对象
        self.socket.close()


# 客户端类
class NetClient(QObject):
    msg_signal = pyqtSignal(str)
    """
    创建自己的套接字对象 连接服务器  接收数据 发送数据
    name/ip/port
    """
    def __init__(self, name, ip, port):
        super(NetClient, self).__init__()
        self.name = name
        # 客户端要连接服务器 还需要知道服务器的ip port
        self.ip = ip  # 服务器的ip
        self.port = port  # 服务器的port
        # 创建客户端的套接字
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def build_connect(self):
        self.socket.connect((self.ip, int(self.port)))
        # 接收数据
        th = threading.Thread(target=self.recv)
        th.start()

    def recv(self):
        # 客户端接收服务器的数据
        while True:
            try:
                data = self.socket.recv(4096).decode()
                # 通过信号的方式 发出去数据
                self.msg_signal.emit(data)
            except Exception as e:
                print('错误信息是：', e)

    def send(self, data):
        # 发送数据
        self.socket.send(data.encode())

    def close(self):
        self.socket.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    net = NetConfigWidget()
    net.show()
    sys.exit(app.exec())
