import os
import sys
import pygame.mixer as mixer
from PyQt5.QtCore import QTimer, Qt, QSize, QEvent
from PyQt5.QtGui import QPixmap, QFont, QIcon, QImage, QCursor
from PyQt5.QtWidgets import QWidget, QToolTip, QLabel, QSystemTrayIcon, QMenuBar, QAction, QMenu, qApp, QApplication
import PyQt5.sip
from config import args, dic


class Pet(QWidget):
    def __init__(self):
        super(Pet, self).__init__()
        self.file_name = args.kl  # 文件夹名称
        self.file_list = sorted(os.listdir(self.file_name))  # 对文件夹里面的所有图片进行排序
        self.img = QImage().load(os.path.join(self.file_name, str(self.file_list[1])))  # 获取第一张图片作为托盘图标
        self.wt = 300
        self.ht = 300
        self.music_player = False
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
        self.pic_url = os.path.join(self.file_name, str(self.file_list[self.index]))
        self.pm = QPixmap(self.pic_url)
        self.lbl.setPixmap(self.pm)

    def init_window(self):
        """
        初始化窗口
        """
        self.setToolTip(dic[self.file_name])
        self.setGeometry(0, 400, self.wt, self.ht)  # 设置窗口和位置
        self.lbl = QLabel(self)  # 初始化一个QLabel对象
        self.index = 1
        self.pic_url = os.path.join(self.file_name, str(self.file_list[self.index]))
        self.pm = QPixmap(self.pic_url)  # 图像显示
        self.lbl.setPixmap(self.pm)  # 设置Qlabel为一个Pimap图片
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)  # 设置窗口置顶以及去掉边框
        self.setAutoFillBackground(False)  # 设置窗口背景透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.show()  # 显示窗口
        self.tp.setIcon(QIcon(os.path.join(self.file_name, str(self.file_list[1]))))  # 系统托盘图标
        self.timer = QTimer()
        self.timer.timeout.connect(self.act)

    def tray(self):
        """
        建立一个托盘
        """
        self.bar = QMenuBar(self)
        self.menu = self.bar.addMenu('菜单')

        self.pets = self.menu.addMenu('人物')
        bbl = QAction('芭芭拉', self)
        bbl.triggered.connect(self.bbl)
        kq = QAction('刻晴', self)
        kq.triggered.connect(self.kq)
        dlk = QAction('迪卢克', self)
        dlk.triggered.connect(self.dlk)
        kl = QAction('可莉', self)
        kl.triggered.connect(self.kl)
        gy = QAction('甘雨', self)
        gy.triggered.connect(self.gy)

        self.pets.addAction(bbl)
        self.pets.addAction(kq)
        self.pets.addAction(dlk)
        self.pets.addAction(kl)
        self.pets.addAction(gy)

        show = QAction('显示', self)
        show.triggered.connect(self.showwin)
        self.music = QAction('音乐开', self)
        self.music.triggered.connect(self.music_switch)
        quit = QAction('退出', self)
        quit.triggered.connect(self.quit)

        self.menu.addAction(show)
        self.menu.addAction(self.music)
        self.menu.addAction(quit)

        self.tp.setContextMenu(self.menu)
        self.tp.show()

    def reshow(self, name):
        """
        桌面宠物的替换
        """
        self.close()  # 关闭窗口
        self.lbl.deleteLater()  # 清空Label
        self.wt = 300
        self.ht = 300
        self.file_name = name
        self.file_list = sorted(os.listdir(self.file_name))
        self.img = QImage().load(os.path.join(self.file_name, str(self.file_list[1])))  # 获取第一张图片作为托盘图标

        # scale = 1.2  # 每次放到20%
        # img = QImage(self.pic_url)  # 创建图片实例
        # size = QSize(self.wt,self.ht)
        # pixImg = QPixmap.fromImage(
        #     img.scaled(size, Qt.IgnoreAspectRatio))  # 修改图片实例大小并从QImage实例中生成QPixmap实例以备放入QLabel控件中
        # self.pm = QPixmap(pixImg)  # 图像显示
        self.init_window()
        self.tp.show()

    def bbl(self):
        # 芭芭拉
        self.reshow('yuanshen/芭芭拉')
        self.timer.start(50)

    def gy(self):
        # 甘雨
        self.reshow('yuanshen/甘雨')
        self.timer.start(50)

    def kq(self):
        # 刻晴
        self.reshow('yuanshen/刻晴')
        self.timer.start(50)

    def dlk(self):
        # 迪卢克
        self.reshow('yuanshen/迪卢克')
        self.timer.start(60)

    def kl(self):
        # 可莉
        self.reshow('yuanshen/可莉')
        self.timer.start(60)

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

    def enterEvent(self, event):
        if event.type() == QEvent.Enter:
            self.paly_music(self.file_name)

    def music_switch(self):
        self.music_player = not self.music_player
        if self.music_player:
            self.music.setText('音乐关')
        else:
            self.music.setText('音乐开')

    def paly_music(self, s):
        if self.music_player:
            if s in ['bbl', 'kl', 'kq']:
                mixer.init()
                mixer.music.load('./music/' + s + '.mp3')
                if not mixer.music.get_busy():
                    mixer.music.play()


if __name__ == '__main__':
    # 创建程序和对象
    app = QApplication(sys.argv)
    pet = Pet()
    sys.exit(app.exec_())
