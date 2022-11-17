#!/usr/bin/python3
# -*- coding:utf-8 -*-
# project:      # 音乐 播放器
# user:Administrator
# Author: Sheild
# createtime: 2022/3/19 19:58

import sys
import threading
from threading import Thread
from PyQt5 import QtCore, QtGui, QtWidgets
from os import getenv, mkdir, makedirs, remove, listdir
from sys import exit
from time import sleep
from subprocess import call
from decimal import Decimal
from shutil import copyfile, rmtree
from requests import post, get
from random import randint
from ast import literal_eval
from qtawesome import icon
from PyQt5.QtWidgets import QLabel, QListWidgetItem, QLineEdit, QComboBox, QMenu, QAction, QMainWindow, QWidget, \
    QGridLayout, QTabWidget, QListWidget, QPushButton, QProgressBar, QMessageBox, QApplication, QFileDialog, \
    QStatusBar, QGraphicsOpacityEffect
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, QMutex, QRect, QPoint, Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap, QCursor

apdata = getenv("APPDATA")
data = str(apdata) + '\music'


# 基础 功能 实现  重构 窗口功能
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

    # def closeEvent(self, event):
    #     reply = QtWidgets.QMessageBox.question(self, '提示',
    #                                            "是否要退出程序？",
    #                                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
    #                                            QtWidgets.QMessageBox.No)
    #     if reply == QtWidgets.QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()

    def mousePressEvent(self, event):
        global big
        big = False

        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            # self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        global big
        big = False
        if Qt.LeftButton and self.m_flag:
            self.setWindowState(Qt.WindowNoState)
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        global big
        big = False
        self.m_flag = False
        # self.setCursor(QCursor(Qt.ArrowCursor))

    def big(self):
        global big
        print('最大化：{}'.format(big))
        if not big:
            self.setWindowState(Qt.WindowMaximized)
            big = True
        elif big:
            self.setWindowState(Qt.WindowNoState)
            big = False

    def mini(self):
        self.showMinimized()


class MyQLabel(QtWidgets.QLabel):
    # 自定义信号, 注意信号必须为类属性
    button_clicked_signal = QtCore.pyqtSignal()

    def enterEvent(self, event):
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def leaveEvent(self, event):
        self.setCursor(QCursor(Qt.ArrowCursor))

    def __init__(self, parent=None):
        super(MyQLabel, self).__init__(parent)

    def mouseReleaseEvent(self, QMouseEvent):
        self.button_clicked_signal.emit()
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        pass

    def mousePressEvent(self, event):
        self.setCursor(QCursor(Qt.ArrowCursor))

    def connect_customized_slot(self, func):
        self.button_clicked_signal.connect(func)


# 界面美化
class UiMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.RowLength = 0
        # self.setupUi(MainWindow())
        # t1 = Thread(target=self.action)
        # t1.setDaemon(True)
        # t1.start()
        self.start()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1023, 758)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(0, 50, 1024, 601))
        self.label_1.setText("")
        self.label_1.setObjectName("label")

        try:
            pix_img = QPixmap(str('1.jpg'))
            pix = pix_img.scaled(1024, 700, Qt.KeepAspectRatio)
            self.label_1.setPixmap(pix)
        except:
            pass

        self.widget_left = QtWidgets.QWidget(self.centralwidget)
        self.widget_left.setGeometry(QtCore.QRect(0, 60, 243, 591))
        self.widget_left.setObjectName("widget_left")
        self.widget_left.setStyleSheet('''
             QWidget#left_widget{
             background:#2B2B2B;
             border-top:1px solid #222225;
             border-bottom:1px solid #222225;
             border-left:1px solid #222225;
             border-right:1px solid #444444;

             }''')

        self.label_smallpic = MyQLabel(self.widget_left)
        self.label_smallpic.setGeometry(QtCore.QRect(22, 180, 200, 200))
        self.label_smallpic.setText("")
        self.label_smallpic.setObjectName("label_smallpic")
        self.label_smallpic.connect_customized_slot(self.show)
        pix_img = QPixmap(str(data + '/backdown.png'))
        pix = pix_img.scaled(200, 200, Qt.KeepAspectRatio)
        self.label_smallpic.setPixmap(pix)
        self.label_pagenum = QtWidgets.QLabel(self.widget_left)
        self.label_pagenum.setGeometry(QtCore.QRect(22, 500, 210, 16))
        self.label_pagenum.setObjectName("label_pagenum")
        self.shuru2 = QtWidgets.QLineEdit(self.widget_left)
        self.shuru2.setText('5')
        self.shuru2.setGeometry(QtCore.QRect(77, 80, 78, 20))
        self.shuru2.setObjectName("shuru2")
        self.label_5 = QtWidgets.QLabel(self.widget_left)
        self.label_5.setGeometry(QtCore.QRect(11, 80, 54, 21))
        self.label_5.setObjectName("label_5")
        self.sure = QtWidgets.QPushButton(self.widget_left)
        self.sure.setGeometry(QtCore.QRect(165, 80, 67, 23))
        self.sure.setObjectName("sure")
        # self.sure.clicked.connect(self.page)
        self.sure.setStyleSheet(
            '''QPushButton{background:#3C3F41;border-radius:5px;}QPushButton:hover{background:#F2BCAE;}''')

        self.widget_down = QtWidgets.QWidget(self.centralwidget)
        self.widget_down.setGeometry(QtCore.QRect(0, 650, 1024, 81))
        self.widget_down.setObjectName("widget_down")
        self.horizontalSlider = QtWidgets.QSlider(self.widget_down)
        self.horizontalSlider.setGeometry(QtCore.QRect(330, 52, 375, 20))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)

        self.horizontalSlider.setObjectName("horizontalSlider")

        self.widget_control = QtWidgets.QWidget(self.widget_down)
        self.widget_control.setGeometry(QtCore.QRect(264, 0, 485, 51))
        self.widget_control.setObjectName("widget_control")
        self.label3 = QtWidgets.QLabel(self.widget_down)
        self.label3.setGeometry(QtCore.QRect(803, 30, 111, 21))
        self.label3.setObjectName("label_3")
        self.right_playconsole_layout = QGridLayout()  # 播放控制部件网格布局层
        self.widget_control.setLayout(self.right_playconsole_layout)

        self.console_button_1 = QPushButton(icon('fa.backward', color='#3FC89C'), "")
        # self.console_button_1.clicked.connect(self.last)
        self.console_button_1.setStyleSheet(
            '''QPushButton{background:#222225;border-radius:5px;}QPushButton:hover{background:#3684C8;}''')

        self.console_button_2 = QPushButton(icon('fa.forward', color='#3FC89C'), "")
        # self.console_button_2.clicked.connect(self.nextion)
        self.console_button_2.setStyleSheet(
            '''QPushButton{background:#222225;border-radius:5px;}QPushButton:hover{background:#3684C8;}''')

        self.console_button_3 = QPushButton(icon('fa.pause', color='#3FC89C', font=18), "")
        # self.console_button_3.clicked.connect(self.pause)
        self.console_button_3.setStyleSheet(
            '''QPushButton{background:#222225;border-radius:5px;}QPushButton:hover{background:#3684C8;}''')

        self.console_button_4 = QPushButton(icon('fa.volume-down', color='#3FC89C', font=18), "")
        # self.console_button_4.clicked.connect(self.voicedown)
        self.console_button_4.setStyleSheet(
            '''QPushButton{background:#222225;border-radius:5px;}QPushButton:hover{background:#3684C8;}''')

        self.console_button_5 = QPushButton(icon('fa.volume-up', color='#3FC89C', font=18), "")
        # self.console_button_5.clicked.connect(self.voiceup)
        self.console_button_5.setStyleSheet(
            '''QPushButton{background:#222225;border-radius:5px;}QPushButton:hover{background:#3684C8;}''')

        self.console_button_6 = QPushButton(icon('fa.align-center', color='#3FC89C', font=18), "")
        # self.console_button_6.clicked.connect(self.playmode)
        self.console_button_6.setStyleSheet(
            '''QPushButton{background:#222225;border-radius:5px;}QPushButton:hover{background:#3684C8;}''')

        self.console_button_3.setIconSize(QSize(30, 30))

        self.right_playconsole_layout.addWidget(self.console_button_4, 0, 0)

        self.right_playconsole_layout.addWidget(self.console_button_1, 0, 1)
        self.right_playconsole_layout.addWidget(self.console_button_3, 0, 2)

        self.right_playconsole_layout.addWidget(self.console_button_2, 0, 3)

        self.right_playconsole_layout.addWidget(self.console_button_5, 0, 4)

        self.right_playconsole_layout.addWidget(self.console_button_6, 0, 5)
        self.right_playconsole_layout.setAlignment(Qt.AlignCenter)  # 设置布局内部件居中显示

        # self.down_layout.addWidget(self.right_playconsole_widget, 1, 0, 1, 4)

        self.widget_control.setStyleSheet('''
            QPushButton{
                border:none;
            }
        ''')

        self.pushButton = MyQLabel(self.widget_down)
        self.pushButton.setGeometry(QtCore.QRect(11, 10, 67, 61))
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.connect_customized_slot(self.show)

        self.label_leftnum = QtWidgets.QLabel(self.widget_down)
        self.label_leftnum.setGeometry(QtCore.QRect(286, 60, 45, 16))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_leftnum.setFont(font)
        self.label_leftnum.setObjectName("label_leftnum")
        self.label_2 = QtWidgets.QLabel(self.widget_down)
        self.label_2.setGeometry(QtCore.QRect(704, 60, 54, 16))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_name = QtWidgets.QLabel(self.widget_down)
        self.label_name.setGeometry(QtCore.QRect(88, 20, 177, 16))
        self.label_name.setObjectName("label_name")
        self.label_singer = QtWidgets.QLabel(self.widget_down)
        self.label_singer.setGeometry(QtCore.QRect(88, 50, 166, 16))
        self.label_singer.setObjectName("label_singer")
        self.widget_down.setStyleSheet('''
        QWidget#widget_down{
        color:#D0D0D0;
        background:#222225;
        border-bottom:1px solid #222225;
        border-right:1px solid #222225;
        border-top:1px solid #444444;
        border-bottom-right-radius:10px;
        border-bottom-left-radius:10px;

        }
        ''')

        self.widget_right = QtWidgets.QWidget(self.centralwidget)
        self.widget_right.setGeometry(QtCore.QRect(242, 50, 782, 601))
        self.widget_right.setObjectName("widget_right")
        self.right_layout = QGridLayout()
        self.widget_right.setLayout(self.right_layout)  # 设置右侧部件布局为网格

        self.tabWidget = QTabWidget(self)
        self.tabWidget.setGeometry(QtCore.QRect(242, 50, 782, 610))
        op = QGraphicsOpacityEffect()
        op.setOpacity(0.9)

        self.tabWidget.setGraphicsEffect(op)

        self.tabWidget.setStyleSheet('''QWidget#tab{background-color:#212226;color:white}\
                                 QTabBar::tab{background-color:#3C3F41;color:#BBBBBB}\
                                 QTabBar::tab::selected{background-color:#212226;color:white}\
                                 QTabWidget::pane{
                                        border: -1px;
                                        top:-2px;
                                        left: 1px;
                                    }
                                 ''')

        self.tab = QWidget()
        self.tab.setObjectName("tab")
        self.tab_layout = QGridLayout()
        self.tab.setLayout(self.tab_layout)
        self.listwidget = QListWidget(self.tab)
        self.tab.setWindowOpacity(0.8)

        self.label361 = QLabel(self)
        self.label361.setText("")
        self.label361.setStyleSheet("color:#6DDF6D")
        self.tab_layout.addWidget(self.label361, 0, 1, 1, 1)

        self.button_1235 = QPushButton(icon('fa.download', color='#D0D0D0', font=24), "下载全部")
        # self.button_1235.clicked.connect(self.downloadalls)
        self.button_1235.setStyleSheet(
            '''QPushButton{background:#222225;border-radius:5px;}QPushButton:hover{background:#303030;}''')
        self.tab_layout.addWidget(self.button_1235, 0, 2, 1, 1)

        self.button_1236 = QPushButton(icon('fa.trash-o', color='#D0D0D0', font=24), "清空列表")
        # self.button_1236.clicked.connect(self.dell)
        self.button_1236.setStyleSheet(
            '''QPushButton{background:#222225;border-radius:5px;}QPushButton:hover{background:#303030;}''')
        self.tab_layout.addWidget(self.button_1236, 0, 3, 1, 1)

        self.listwidget.doubleClicked.connect(lambda: self.change_func(self.listwidget))
        self.listwidget.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.listwidget.customContextMenuRequested[QPoint].connect(self.myListWidgetContext)
        self.listwidget.setStyleSheet('''QListWidget{color:black}''')

        self.listwidget.setObjectName("listWidget")
        # self.tab.setStyleSheet('''QWidget{background:transparent};QListWidget{color:black}''')
        self.tab_layout.addWidget(self.listwidget, 1, 0, 1, 4)
        self.tabWidget.addTab(self.tab, "     搜索页     ")

        self.tab2 = QWidget()
        self.tab2.setObjectName("tab")
        self.tab2_layout = QGridLayout()
        self.tab2.setLayout(self.tab2_layout)
        self.listwidget2 = QListWidget(self.tab2)
        self.listwidget2.doubleClicked.connect(lambda: self.change_funcse(self.listwidget2))
        self.listwidget2.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.listwidget2.customContextMenuRequested[QPoint].connect(self.myListWidgetContext2)

        self.listwidget2.setObjectName("listWidget2")
        self.listwidget2.setContextMenuPolicy(3)
        self.tab2_layout.addWidget(self.listwidget2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab2, "     最近播放     ")

        self.tab3 = QWidget()
        self.tab3.setObjectName("tab")
        self.tab3_layout = QGridLayout()
        self.tab3.setLayout(self.tab3_layout)

        self.label223 = QLabel(self)
        # self.label5.setScaledContents(True)
        pix_img = QPixmap(str(data + '/backdown.png'))
        pix = pix_img.scaled(100, 100, Qt.KeepAspectRatio)
        self.label223.setPixmap(pix)
        # self.label5.setMaximumSize(1,1)
        self.tab3_layout.addWidget(self.label223, 0, 0, 1, 1)

        self.button_1237 = QPushButton(icon('fa.play', color='#FFFFFF', font=24), "播放全部")
        # self.button_1237.clicked.connect(self.allplaylove)
        self.button_1237.setStyleSheet(
            '''QPushButton{background:#EC4141;border-radius:5px;}QPushButton:hover{background:#E92121;}''')
        self.tab3_layout.addWidget(self.button_1237, 0, 1, 1, 1)

        self.button_1235 = QPushButton(icon('fa.download', color='#D0D0D0', font=24), "下载全部")
        # self.button_1235.clicked.connect(self.downloadalllove)
        self.button_1235.setStyleSheet(
            '''QPushButton{background:#222225;border-radius:5px;}QPushButton:hover{background:#303030;}''')
        self.tab3_layout.addWidget(self.button_1235, 0, 2, 1, 1)

        self.button_1236 = QPushButton(icon('fa.trash-o', color='#D0D0D0', font=24), "清空列表")
        # self.button_1236.clicked.connect(self.delove)
        self.button_1236.setStyleSheet(
            '''QPushButton{background:#222225;border-radius:5px;}QPushButton:hover{background:#303030;}''')
        self.tab3_layout.addWidget(self.button_1236, 0, 3, 1, 1)

        self.listwidget3 = QListWidget(self.tab3)
        self.listwidget3.doubleClicked.connect(lambda: self.change_funclove(self.listwidget3))
        self.listwidget3.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.listwidget3.customContextMenuRequested[QPoint].connect(self.myListWidgetContext3)

        self.listwidget3.setObjectName("listWidget3")
        self.tab3_layout.addWidget(self.listwidget3, 1, 0, 1, 4)
        self.tabWidget.addTab(self.tab3, "     喜爱的歌     ")

        self.tab5 = QWidget()
        self.tab5.setObjectName("tab5")
        self.tab5_layout = QGridLayout()
        self.tab5.setLayout(self.tab5_layout)
        self.listwidget5 = QListWidget(self.tab5)
        self.listwidget5.doubleClicked.connect(lambda: self.change(self.listwidget5))
        self.listwidget5.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.listwidget5.customContextMenuRequested[QPoint].connect(self.myListWidgetContext5)

        self.button_12351 = QPushButton(icon('fa.download', color='#D0D0D0', font=24), "添加目录")
        # self.button_12351.clicked.connect(self.add)
        self.button_12351.setStyleSheet(
            '''QPushButton{background:#222225;border-radius:5px;}QPushButton:hover{background:#303030;}''')
        self.tab5_layout.addWidget(self.button_12351, 0, 2, 1, 1)

        self.button_12361 = QPushButton(icon('fa.trash-o', color='#D0D0D0', font=24), "清空列表")
        # self.button_12361.clicked.connect(self.dellocal)
        self.button_12361.setStyleSheet(
            '''QPushButton{background:#222225;border-radius:5px;}QPushButton:hover{background:#303030;}''')
        self.tab5_layout.addWidget(self.button_12361, 0, 3, 1, 1)

        self.listwidget5.setObjectName("listWidget5")
        self.tab5_layout.addWidget(self.listwidget5, 1, 0, 1, 4)
        self.tabWidget.addTab(self.tab5, "     本地歌曲     ")

        self.right_layout.addWidget(self.tabWidget, 3, 0, 100, 100)

        self.widget_up = QtWidgets.QWidget(self.centralwidget)
        self.widget_up.setGeometry(QtCore.QRect(0, 0, 1024, 51))
        self.widget_up.setObjectName("widget_up")
        self.shuru = QtWidgets.QLineEdit(self.widget_up)
        self.shuru.setGeometry(QtCore.QRect(220, 10, 221, 31))
        self.shuru.setObjectName("shuru")
        # self.shuru.returnPressed.connect(self.correct)
        self.pushButton_search = QtWidgets.QPushButton(self.widget_up)
        self.pushButton_search.setIcon(icon('fa.search', color='white'))
        self.pushButton_search.setGeometry(QtCore.QRect(407, 10, 34, 31))
        self.pushButton_search.setObjectName("pushButton_search")
        # self.pushButton_search.clicked.connect(self.correct)
        self.pushButton_search.setStyleSheet(
            'QPushButton{color:white;border-radius:5px;}QPushButton:hover{background:green;}')

        self.cb = QtWidgets.QComboBox(self.widget_up)
        self.cb.setGeometry(QtCore.QRect(594, 10, 122, 31))
        self.cb.setObjectName("comboBox")
        self.cb.addItems(['酷狗', '网易云', 'qq', '酷我', '虾米', '百度', '一听'])
        # self.up_layout.addWidget(self.cb, 0, 180, 1, 30)
        # self.cb.currentIndexChanged[int].connect(self.print)

        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(0, 50, 1024, 601))
        font = QtGui.QFont()
        font.setFamily("Microsoft Himalaya")
        self.widget.setFont(font)
        self.widget.setObjectName("widget")

        self.label_picbig = MyQLabel(self.widget)
        self.label_picbig.setGeometry(QtCore.QRect(55, 160, 300, 300))
        self.label_picbig.setText("")
        self.label_picbig.setObjectName("label_picbig")
        self.label_picbig.connect_customized_slot(self.show)

        pix_img = QPixmap(str(data + '/backdown.png'))
        pix = pix_img.scaled(300, 300, Qt.KeepAspectRatio)
        self.label_picbig.setPixmap(pix)

        self.label_showname = QtWidgets.QLabel(self.widget)
        self.label_showname.setGeometry(QtCore.QRect(440, 10, 1000, 41))
        font = QtGui.QFont()
        font.setFamily("幼圆")
        font.setPointSize(28)
        self.label_showname.setFont(font)
        self.label_showname.setObjectName("label_showname")
        self.label_showsinger = QtWidgets.QLabel(self.widget)
        self.label_showsinger.setGeometry(QtCore.QRect(462, 70, 1000, 30))
        font = QtGui.QFont()
        font.setFamily("幼圆")
        font.setPointSize(20)
        self.label_showsinger.setFont(font)
        self.label_showsinger.setObjectName("label_showsinger")
        self.listwidget_lrc = QtWidgets.QListWidget(self.widget)
        self.listwidget_lrc.setGeometry(QtCore.QRect(396, 110, 422, 461))

        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setGeometry(QtCore.QRect(22, 20, 67, 61))
        font = QtGui.QFont()
        font.setPointSize(40)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_2.setText("")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.show)
        self.pushButton_2.setIcon(icon('fa.caret-down', color='white', font=90))
        self.pushButton_2.setStyleSheet(
            '''QPushButton{background:#222225;border-radius:5px;}QPushButton:hover{background:#29292C;}''')

        self.pushButton_love = QtWidgets.QPushButton(self.widget)
        self.pushButton_love.setIcon(icon('fa.heart', color='#3FC89C', font=24))
        self.pushButton_love.setStyleSheet(
            '''QPushButton{background:#222225;border-radius:5px;}QPushButton:hover{background:#3684C8;}''')
        self.pushButton_love.setGeometry(QtCore.QRect(55, 490, 45, 41))
        # self.pushButton_love.clicked.connect(self.lovesong)
        font = QtGui.QFont()
        font.setPointSize(14)

        self.pushButton_love.setFont(font)
        self.pushButton_love.setText("")
        self.pushButton_love.setObjectName("pushButton_love")
        self.pushButton_download = QtWidgets.QPushButton(self.widget)
        self.pushButton_download.setGeometry(QtCore.QRect(121, 490, 45, 41))
        self.pushButton_download.setIcon(icon('fa.download', color='#3FC89C', font=24))
        self.pushButton_download.setStyleSheet(
            '''QPushButton{background:#222225;border-radius:5px;}QPushButton:hover{background:#3684C8;}''')
        # self.pushButton_download.clicked.connect(self.down)

        self.widget.setHidden(True)

        self.listwidget_lrc.setObjectName("listWidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1034, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # 以上可以修改
        self.centralwidget.setStyleSheet('''
             QWidget#centralwidget{
             color:#222225;
             background:#222225;
             border-top:1px solid #222225;
             border-bottom:1px solid #222225;
             border-right:1px solid #222225;
             border-left:1px solid #222225;
             border-top-left-radius:10px;
             border-top-right-radius:10px;
             border-bottom-left-radius:10px;
             border-bottom-right-radius:10px;
             }
             QListWidget{background-color:#2B2B2B;color:#222225}
         /*垂直滚动条*/
         QScrollBar:vertical{
             width:12px;
             border:1px solid #2B2B2B;
             margin:0px,0px,0px,0px;
             padding-top:0px;
             padding-bottom:0px;
         }
         QScrollBar::handle:vertical{
             width:3px;
             background:#4B4B4B;
             min-height:3;
         }
         QScrollBar::handle:vertical:hover{
             background:#3F3F3F;
             border:0px #3F3F3F;
         }
         QScrollBar::sub-line:vertical{
             width:0px;
             border-image:url(:/Res/scroll_left.png);
             subcontrol-position:left;
         }
         QScrollBar::sub-line:vertical:hover{
             height:0px;
             background:#222225;
             subcontrol-position:top;
         }
         QScrollBar::add-line:vertical{
             height:0px;
             border-image:url(:/Res/scroll_down.png);
             subcontrol-position:bottom;
         }
         QScrollBar::add-line:vertical:hover{
             height:0px;
             background:#3F3F3F;
             subcontrol-position:bottom;
         }
         QScrollBar::add-page:vertical{
             background:#2B2B2B;
         }
         QScrollBar::sub-page:vertical{
             background:#2B2B2B;
         }
         QScrollBar::up-arrow:vertical{
             border-style:outset;
             border-width:0px;
         }
         QScrollBar::down-arrow:vertical{
             border-style:outset;
             border-width:0px;
         }

         QScrollBar:horizontal{
             height:12px;
             border:1px #2B2B2B;
             margin:0px,0px,0px,0px;
             padding-left:0px;
             padding-right:0px;
         }
         QScrollBar::handle:horizontal{
             height:16px;
             background:#4B4B4B;
             min-width:20;
         }
         QScrollBar::handle:horizontal:hover{
             background:#3F3F3F;
             border:0px #3F3F3F;
         }
         QScrollBar::sub-line:horizontal{
             width:0px;
             border-image:url(:/Res/scroll_left.png);
             subcontrol-position:left;
         }
         QScrollBar::sub-line:horizontal:hover{
             width:0px;
             background:#2B2B2B;
             subcontrol-position:left;
         }
         QScrollBar::add-line:horizontal{
             width:0px;
             border-image:url(:/Res/scroll_right.png);
             subcontrol-position:right;
         }
         QScrollBar::add-line:horizontal:hover{
             width:0px;
             background::#2B2B2B;
             subcontrol-position:right;
         }
         QScrollBar::add-page:horizontal{
                    background:#2B2B2B;
         }
         QScrollBar::sub-page:horizontal{
                     background:#2B2B2B;
         }
        QListView, QLineEdit { 
    color: #D2D2D2; 
    background-color:#29292C;
    selection-color: #29292C; 
    border: 2px groove #29292C; 
    border-radius: 10px; 
    padding: 2px 4px; 
} 
QLineEdit:focus { 
    color: #D2D2D2; 
    selection-color: #29292C; 
    border: 2px groove #29292C; 
    border-radius: 10px; 
    padding: 2px 4px; 
} 
        QComboBox {
border: 1px solid rgb(117, 118, 118);
        border-radius: 5px;
        background: #2E2B2D; 
        color:white;
padding: 1px 2px 1px 2px;
}
        QLabel{color:white}
        QPushButton{color:white}
             ''')

        self.widget_up.setStyleSheet('''
             QWidget#widget_up{
             background:#222225;
             border-top:1px solid #222225;
             border-bottom:1px solid #AD2121;
             border-left:1px solid #222225;
             border-top-left-radius:10px;
             border-top-right-radius:10px;
             }
             ''')

        self.close_widget = QtWidgets.QWidget(self.centralwidget)
        self.close_widget.setGeometry(QtCore.QRect(940, 0, 90, 30))
        self.close_widget.setObjectName("close_widget")
        self.close_layout = QGridLayout()  # 创建左侧部件的网格布局层
        self.close_widget.setLayout(self.close_layout)  # 设置左侧部件布局为网格

        self.left_close = QPushButton("")  # 关闭按钮
        self.left_close.clicked.connect(MainWindow.close)
        self.left_visit = QPushButton("")  # 空白按钮
        self.left_visit.clicked.connect(MainWindow.big)
        self.left_mini = QPushButton("")  # 最小化按钮
        self.left_mini.clicked.connect(MainWindow.mini)
        self.close_layout.addWidget(self.left_mini, 0, 0, 1, 1)
        self.close_layout.addWidget(self.left_close, 0, 2, 1, 1)
        self.close_layout.addWidget(self.left_visit, 0, 1, 1, 1)
        self.left_close.setFixedSize(15, 15)  # 设置关闭按钮的大小
        self.left_visit.setFixedSize(15, 15)  # 设置按钮大小
        self.left_mini.setFixedSize(15, 15)  # 设置最小化按钮大小
        self.left_close.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.left_visit.setStyleSheet(
            '''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''')
        self.left_mini.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')

        MainWindow.setWindowOpacity(0.95)  # 设置窗口透明度
        MainWindow.setAttribute(Qt.WA_TranslucentBackground)
        MainWindow.setWindowFlag(Qt.FramelessWindowHint)  # 隐藏边框

        self.widget.setStyleSheet('''
             QPushButton{border:none;color:#D0D0D0;}
             QPushButton#left_label{
             border:none;
             border-bottom:1px solid white;
             font-size:18px;
             font-weight:700;
             font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
             }
             QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}
             QWidget#widget{
             background:#2B2B2B;
             border-top:1px solid #222225;
             border-bottom:1px solid #222225;
             border-left:1px solid #222225;
             border-right:1px solid #444444;

             }
             ''')

    def start(self):
        pass
        # try:
        #
        #     try:
        #         self.work = startThread()
        #         self.work.start()
        #         self.work.trigger.connect(self.dispng)
        #     except:
        #         print('默认图片下载错误')
        #         pass
        #
        #     try:
        #         self.work22 = barThread()
        #         self.work22.start()
        #         self.work22.trigger.connect(self.disbar)
        #     except:
        #         print('12')
        #
        #     try:
        #         pix_img = QPixmap(str(data + '/backdown.png'))
        #         pix = pix_img.scaled(300, 300, Qt.KeepAspectRatio)
        #         self.label_picbig.setPixmap(pix)
        #         pix = pix_img.scaled(200, 300, Qt.KeepAspectRatio)
        #         self.label_smallpic.setPixmap(pix)
        #         pix = pix_img.scaled(61, 67, Qt.KeepAspectRatio)
        #         self.pushButton.setPixmap(pix)
        #     except:
        #         pass
        # except:
        #     pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    MainWindow = MainWindow()  # QtWidgets.QMainWindow()
    ui = UiMainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())
