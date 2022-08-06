import os
import sys
import pygame
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PIL import Image

dic = {'kq': '见光如我，斩尽牛杂',
       'kl': '哒哒哒 ～，啦啦啦～',
       'bbl': '演唱，开始',
       'wy': ' ',
       'ttbj':' '}

class Pet(QWidget):
    def __init__(self):
        super(Pet, self).__init__()
        # 初始化为显示可莉
        self.file_name = 'kl'  # 文件夹名称
        self.file_list = sorted(os.listdir('./' + self.file_name))  # 对文件夹里面的所有图片进行排序
        self.img = Image.open('./' + self.file_name + '/' + str(self.file_list[1]))  # 获取第一张图片作为托盘图标
        self.w, self.h = self.img.size[0], self.img.size[1]  # 获取图片大小

        self.init_window()
        self.tray()

        self.is_follow_mouse = False  # 初始化鼠标没有移动
        self.mouse_drag_pos = self.pos()

        # 每隔一段时间做个动作
        self.timer = QTimer()
        self.timer.timeout.connect(self.act)
        self.timer.start(50)

    def act(self):
        """
        读取图片不同的地址，实现动画效果
        """
        if self.key < len(self.file_list) - 1:
            self.key += 1
        else:
            self.key = 1
        self.pic_url = './' + self.file_name + '/' + str(self.file_list[self.key])
        self.pm = QPixmap(self.pic_url)
        self.lbl.setPixmap(self.pm)

    def init_window(self):
        """
        初始化窗口
        """
        QToolTip.setFont(QFont('SansSerif', 20))
        self.setToolTip(dic[self.file_name])
        self.setGeometry(0, 800 - self.h, self.w, self.h)  # 设置窗口和位置
        self.setWindowTitle('Pet')  # 设置窗口标题
        self.lbl = QLabel(self)  # 初始化一个QLabel对象
        self.key = 1
        self.pic_url = './' + self.file_name + '/' + str(self.file_list[self.key])
        self.pm = QPixmap(self.pic_url)  # 图像显示
        self.lbl.setPixmap(self.pm)  # 设置Qlabel为一个Pimap图片

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)  # 设置窗口置顶以及去掉边框
        self.setAutoFillBackground(False)  # 设置窗口背景透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # op = QtWidgets.QGraphicsOpacityEffect()
        # op.setOpacity(0)
        # self.lbl.setGraphicsEffect(op)
        self.show()  # 显示窗口

    def tray(self):
        """
        建立一个托盘
        """
        self.tp = QSystemTrayIcon(self)  # 初始化系统托盘
        self.tp.setToolTip('原来你也玩原神')
        self.tp.setIcon(QIcon('./' + self.file_name + '/' + str(self.file_list[1])))  # 系统托盘图标
        self.ation_quit = QAction('QUIT', self, triggered=self.quit)  # 托盘选项
        self.ation_kl = QAction('可莉', self, triggered=self.kl)
        self.ation_wy = QAction('枫原万叶', self, triggered=self.wy)
        self.ation_ttbj = QAction('兔兔伯爵', self, triggered=self.ttbj)
        self.ation_bbl = QAction('芭芭拉', self, triggered=self.bbl)
        self.ation_kq = QAction('刻晴', self, triggered=self.kq)
        self.tpMenu = QMenu(self)  # 初始化一个托盘菜单
        self.tpMenu.addAction(self.ation_kl)  # 添加托盘选项
        self.tpMenu.addAction(self.ation_wy)
        self.tpMenu.addAction(self.ation_kq)
        self.tpMenu.addAction(self.ation_bbl)
        self.tpMenu.addAction(self.ation_ttbj)
        self.tpMenu.addAction(self.ation_quit)
        self.tp.setContextMenu(self.tpMenu)
        self.tp.show()
        # self.tp.showMessage('desktoppet', '111', icon=0)

    def reshow(self, name):
        """
        桌面宠物的替换
        """
        self.close()        # 关闭窗口
        self.lbl.deleteLater()      # 清空Label
        self.file_name = name
        self.file_list = sorted(os.listdir('./' + self.file_name))
        self.img = Image.open('./' + self.file_name + '/' + str(self.file_list[1]))
        self.w, self.h = self.img.size[0], self.img.size[1]
        QToolTip.setFont(QFont('SansSerif', 20))
        self.setToolTip(dic[self.file_name])
        self.setGeometry(0, 800 - self.h, self.w, self.h)  # 设置窗口和位置
        self.setWindowTitle('Pet')  # 设置窗口标题
        self.lbl = QLabel(self)  # 初始化一个QLabel对象
        self.key = 1
        self.pic_url = './' + self.file_name + '/' + str(self.file_list[self.key])
        self.pm = QPixmap(self.pic_url)  # 图像显示
        self.lbl.setPixmap(self.pm)  # 设置Qlabel为一个Pimap图片
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)  # 设置窗口置顶以及去掉边框
        self.setAutoFillBackground(False)  # 设置窗口背景透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.show()  # 显示窗口
        self.tp.setIcon(QIcon('./' + self.file_name + '/' + str(self.file_list[1])))  # 系统托盘图标
        self.tp.show()
        # self.tp.showMessage('00', '111', icon=0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.act)

    def kl(self):
        """
        可莉
        """
        self.reshow('kl')
        self.timer.start(50)

    def wy(self):
        """
        万叶
        """
        self.reshow('wy')
        self.timer.start(100)

    def ttbj(self):
        """
        兔兔伯爵
        """
        self.reshow('ttbj')
        self.timer.start(45)

    def bbl(self):
        """
        芭芭拉
        """
        self.reshow('bbl')
        self.timer.start(50)

    def kq(self):
        """
        刻晴
        """
        self.reshow('kq')
        self.timer.start(50)
    def mousePressEvent(self, event):
        """
        鼠标左键事件
        """
        if event.button() == Qt.LeftButton:
            self.is_follow_mouse = True
            self.mouse_drag_pos = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))


    def mouseMoveEvent(self, event):
        """
        鼠标移动事件
        """
        if Qt.LeftButton and self.is_follow_mouse:
            self.move(event.globalPos() - self.mouse_drag_pos)
            xy = self.pos()
            self.w, self.h = xy.x(), xy.y()
            event.accept()

    def mouseReleaseEvent(self, event):
        """
        鼠标松开事件
        """
        self.is_follow_mouse = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def quit(self):
        """
        退出程序
        """
        self.close()
        sys.exit()

    def enterEvent(self, event):
        if event.type() == QEvent.Enter:
            self.paly_music(self.file_name)


    def paly_music(self, s):
        if s in ['bbl','kl','kq']:
            pygame.mixer.init()
            pygame.mixer.music.load('./music/' + s + '.mp3')
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play()




if __name__ == '__main__':
    # 创建程序和对象
    app = QApplication(sys.argv)
    pet = Pet()
    sys.exit(app.exec_())
