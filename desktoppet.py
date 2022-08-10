import os
import random
import sys
import time

import pygame.mixer as mixer
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap, QFont, QIcon, QImage, QCursor
from PyQt5.QtWidgets import QSystemTrayIcon, QMenuBar, QAction, QMenu, qApp, QApplication,QMainWindow
import PyQt5.sip
from config import args, dic


class Pet(QMainWindow):
    def __init__(self):
        super(Pet, self).__init__()
        self.role_name = args.kl  # 文件夹名称
        self.pre_path = args.path
        self.file_path = self.pre_path + self.role_name
        self.file_list = sorted(os.listdir(self.file_path))  # 对文件夹里面的所有图片进行排序
        self.img = QImage().load(os.path.join(self.file_path, str(self.file_list[1])))  # 获取第一张图片作为托盘图标
        self.wt = 300
        self.ht = 300
        self.audio_player = False
        self.bgmusic_player = False
        self.tp = QSystemTrayIcon(self)  # 初始化系统托盘
        self.tp.setToolTip('原来你也玩原神')
        self.init_window()
        self.timer.start(50)
        self.tray()

        self.is_follow_mouse = False  # 初始化鼠标没有移动
        self.mouse_drag_pos = self.pos()

    def act(self):
        """
        读取图片不同的地址，实现动画效果
        """
        if self.index < len(self.file_list) - 1:
            self.index += 1
        else:
            self.index = 1
        self.pic_url = os.path.join(self.file_path, str(self.file_list[self.index]))
        self.pm = QPixmap(self.pic_url)
        self.lbl.setPixmap(self.pm)

    def init_window(self):
        """
        初始化窗口
        """
        # self.setToolTip(dic[self.role_name])
        self.setGeometry(0, 400, self.wt, self.ht)  # 设置窗口和位置

        # 初始化一个QLabel对象
        self.lbl = QtWidgets.QLabel(self)
        self.lbl.setStyleSheet("QLabel{background-color :black;}")
        self.lbl.setScaledContents(True)
        self.setCentralWidget(self.lbl)


        self.index = 1
        self.pic_url = os.path.join(self.file_path, str(self.file_list[self.index]))
        self.pm = QPixmap(self.pic_url)  # 图像显示
        self.lbl.setPixmap(self.pm)  # 设置Qlabel为一个Pimap图片
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)  # 设置窗口置顶以及去掉边框
        self.setAutoFillBackground(False)  # 设置窗口背景透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.show()  # 显示窗口
        self.tp.setIcon(QIcon(os.path.join(self.file_path, str(self.file_list[1]))))  # 系统托盘图标
        self.timer = QTimer()
        self.timer.timeout.connect(self.act)

    def tray(self):
        """
        建立一个托盘
        """
        self.bar = QMenuBar(self)
        self.menu = self.bar.addMenu('菜单')

        self.pets = self.menu.addMenu('人物')

        # self.pets.addAction(QAction(r, self,triggered=lambda: self.reshow(r)))

        bbl = QAction('芭芭拉', self)
        bbl.triggered.connect(lambda: self.reshow('芭芭拉'))
        self.pets.addAction(bbl)
        kq = QAction('刻晴', self)
        kq.triggered.connect(lambda: self.reshow('刻晴'))
        self.pets.addAction(kq)
        dlk = QAction('迪卢克', self)
        dlk.triggered.connect(lambda: self.reshow('迪卢克'))
        self.pets.addAction(dlk)
        kl = QAction('可莉', self)
        kl.triggered.connect(lambda: self.reshow('可莉'))
        self.pets.addAction(kl)
        gy = QAction('甘雨', self)
        gy.triggered.connect(lambda: self.reshow('甘雨'))
        self.pets.addAction(gy)
        q = QAction('琴', self)
        q.triggered.connect(lambda: self.reshow('琴'))
        self.pets.addAction(q)

        self.audio = QAction('语音开', self)
        self.audio.triggered.connect(self.audio_switch)
        self.menu.addAction(self.audio)

        self.bgmusics = self.menu.addMenu('背景音乐')
        bg_md = QAction('蒙徳', self)
        bg_md.triggered.connect(lambda: self.bg_music('蒙徳'))
        self.bgmusics.addAction(bg_md)
        bg_ly = QAction('璃月', self)
        bg_ly.triggered.connect(lambda: self.bg_music('璃月'))
        self.bgmusics.addAction(bg_ly)
        bg_dq = QAction('稻妻', self)
        bg_dq.triggered.connect(lambda: self.bg_music('稻妻'))
        self.bgmusics.addAction(bg_dq)
        bg_off = QAction('关闭', self)
        bg_off.triggered.connect(lambda: self.bg_music('关闭'))
        self.bgmusics.addAction(bg_off)

        show = QAction('显示', self)
        show.triggered.connect(self.showwin)
        self.menu.addAction(show)

        quit = QAction('退出', self)
        quit.triggered.connect(self.quit)
        self.menu.addAction(quit)

        self.tp.setContextMenu(self.menu)
        self.tp.show()

    def reshow(self, role_name):
        """
        桌面宠物的替换
        """
        print(role_name)
        self.close()  # 关闭窗口
        self.lbl.deleteLater()  # 清空Label
        self.role_name = role_name
        self.wt = 300
        self.ht = 300
        self.file_path = self.pre_path + role_name
        self.file_list = sorted(os.listdir(self.file_path))
        self.img = QImage().load(os.path.join(self.file_path, str(self.file_list[1])))  # 获取第一张图片作为托盘图标

        # scale = 1.2  # 每次放到20%
        # img = QImage(self.pic_url)  # 创建图片实例
        # size = QSize(self.wt,self.ht)
        # pixImg = QPixmap.fromImage(
        #     img.scaled(size, Qt.IgnoreAspectRatio))  # 修改图片实例大小并从QImage实例中生成QPixmap实例以备放入QLabel控件中
        # self.pm = QPixmap(pixImg)  # 图像显示
        self.init_window()
        self.tp.show()
        self.timer.start(50)

    def mousePressEvent(self, event):
        # 鼠标左键事件
        if event.button() == Qt.LeftButton:
            self.is_follow_mouse = True
            self.mouse_drag_pos = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))

    def mouseMoveEvent(self, event):
        # 鼠标移动事件
        if Qt.LeftButton and self.is_follow_mouse:
            self.move(event.globalPos() - self.mouse_drag_pos)
            xy = self.pos()
            self.wt, self.ht = xy.x(), xy.y()
            event.accept()

    def mouseReleaseEvent(self, event):
        # 鼠标松开事件
        self.is_follow_mouse = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def quit(self):
        # 退出程序
        self.close()
        sys.exit()

    def contextMenuEvent(self, event):
        # 定义菜单
        menu = QMenu(self)
        quitAction = menu.addAction("退出")
        hide = menu.addAction("隐藏")
        # 使用exec_()方法显示菜单。从鼠标右键事件对象中获得当前坐标。mapToGlobal()方法把当前组件的相对坐标转换为窗口（window）的绝对坐标。
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == quitAction:
            qApp.quit()
        if action == hide:
            # 通过设置透明度方式隐藏宠物
            self.setWindowOpacity(0)

    def showwin(self):
        self.setWindowOpacity(1)

    def audio_switch(self):
        self.audio_player = not self.audio_player
        self.audio.setText('语音关') if self.audio_player else self.audio.setText('语音开')
        while self.audio_player:
            audio_list = os.listdir(f'./music/{self.role_name}')
            random_audio = audio_list[random.randint(0, len(audio_list) - 1)]
            mixer.init()
            mixer.music.load(f'./music/{self.role_name}/{random_audio}')
            if not mixer.music.get_busy():
                mixer.music.play()
            time.sleep(random.randint(15, 100))
        else:
            mixer.music.stop()

    def bg_music(self, area):
        if area == '关闭':
            mixer.Sound(f'./music/{self.area}/background.mp3').stop()
        else:
            mixer.init()
            mixer.Sound(f'./music/{area}/background.mp3').play()
            self.area = area


if __name__ == '__main__':
    # 创建程序和对象
    app = QApplication(sys.argv)
    pet = Pet()
    sys.exit(app.exec_())
