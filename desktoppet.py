import os
import random
import sys
import pygame.mixer as mixer
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap, QIcon, QImage, QCursor
from PyQt5.QtWidgets import QSystemTrayIcon, QMenuBar, QAction, QMenu, QApplication, QMainWindow
import PyQt5.sip
import datetime
import yaml

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, 'png'))
sys.path.append(os.path.join(BASE_DIR, 'music'))
sys.path.append(os.path.join(BASE_DIR, 'config.yaml'))
with open(os.path.join(BASE_DIR, 'config.yaml'), 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)
mixer.init()


def greeting(time):
    if 10 >= time >= 4:
        return '早上好.mp3'
    elif 14 >= time >= 11:
        return '中午好.mp3'
    elif 24 >= time > 17:
        return '晚上好.mp3'
    else:
        return False


class Pet(QMainWindow):
    def __init__(self):
        super(Pet, self).__init__()
        self.audio_player = config['audio']
        self.role_name = config['role']
        self.music_path = config['music_path']
        self.img_path = config['img_path']
        self.bg_music = config['bg_music']
        desktop = QApplication.desktop()
        screenRect = desktop.screenGeometry()
        self.screenheight, self.screenwidth = screenRect.height(), screenRect.width()

        self.file_path = os.path.join(BASE_DIR, self.img_path, self.role_name)
        self.file_list = sorted(os.listdir(self.file_path))  # 对文件夹里面的所有图片进行排序
        self.img = QImage().load(os.path.join(BASE_DIR, self.file_path, str(self.file_list[1])))  # 获取第一张图片作为托盘图标
        if self.bg_music:
            mixer.music.load(os.path.join(BASE_DIR, self.music_path, self.bg_music, 'background.mp3'))
            mixer.music.play(-1)
        self.scale = config['frame_scale'][self.role_name][1]
        self.wt = 300
        self.ht = 300
        self.pos_x = random.randint(0, self.screenwidth)
        self.pos_y = random.randint(0, self.screenheight)
        self.now_time = datetime.datetime.now().hour
        self.talk_path = [os.path.join(BASE_DIR, self.music_path, self.role_name, i) for i in
                          os.listdir(os.path.join(BASE_DIR, self.music_path, self.role_name)) if i.startswith('闲聊')]
        self.know_path = [os.path.join(BASE_DIR, self.music_path, self.role_name, i) for i in
                          os.listdir(os.path.join(BASE_DIR, self.music_path, self.role_name)) if i.startswith('想要了解')]
        self.tp = QSystemTrayIcon(self)  # 初始化系统托盘
        self.tp.setToolTip('原来你也玩原神')
        self.tray()
        self.init_window()
        self.timer.start(config['frame_scale'][self.role_name][0])
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
        self.pic_url = os.path.join(BASE_DIR, self.file_path, str(self.file_list[self.index]))
        self.pm = QPixmap(self.pic_url, "0", Qt.AvoidDither | Qt.ThresholdDither | Qt.ThresholdAlphaDither).scaled(
            int(self.scale * self.wt), int(self.scale * self.wt))
        self.resize(self.pm.size())
        self.setMask(self.pm.mask())
        self.lbl.setPixmap(self.pm)

    def init_window(self):
        """
        初始化窗口
        """
        self.setGeometry(0, 400, self.pos_x, self.pos_y)  # 设置窗口和位置

        self.lbl = QtWidgets.QLabel(self)  # 初始化一个QLabel对象
        self.lbl.setScaledContents(True)
        self.setCentralWidget(self.lbl)

        self.index = 1
        self.pic_url = os.path.join(BASE_DIR, self.file_path, str(self.file_list[self.index]))
        self.pm = QPixmap(self.pic_url, "0", Qt.AvoidDither | Qt.ThresholdDither | Qt.ThresholdAlphaDither).scaled(
            int(self.scale * self.wt), int(self.scale * self.wt))
        self.resize(self.pm.size())
        self.setMask(self.pm.mask())
        self.lbl.setPixmap(self.pm)  # 设置Qlabel为一个Pimap图片

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)  # 设置窗口置顶以及去掉边框
        self.setAutoFillBackground(False)  # 设置窗口背景透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.show()  # 显示窗口
        self.tp.setIcon(QIcon(os.path.join(BASE_DIR, self.file_path, str(self.file_list[1]))))  # 系统托盘图标
        self.timer = QTimer()
        self.timer.timeout.connect(self.act)
        if self.audio_player:
            self.role_music.setText('人物语音～')
            greet = greeting(self.now_time)
            if greet:
                audio = mixer.Sound(os.path.join(BASE_DIR, self.music_path, self.role_name, greet))
                audio.set_volume(0.5)
                audio.play()

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
        q = QAction('琴', self)
        q.triggered.connect(lambda: self.reshow('琴'))
        self.pets.addAction(q)
        self.pets.addAction(bbl)
        dlk = QAction('迪卢克', self)
        dlk.triggered.connect(lambda: self.reshow('迪卢克'))
        self.pets.addAction(dlk)
        kl = QAction('可莉', self)
        kl.triggered.connect(lambda: self.reshow('可莉'))
        self.pets.addAction(kl)
        mn = QAction('莫娜', self)
        mn.triggered.connect(lambda: self.reshow('莫娜'))
        self.pets.addAction(mn)
        dan = QAction('迪奥娜', self)
        dan.triggered.connect(lambda: self.reshow('迪奥娜'))
        self.pets.addAction(dan)
        fxe = QAction('菲谢尔', self)
        fxe.triggered.connect(lambda: self.reshow('菲谢尔'))
        self.pets.addAction(fxe)
        abd = QAction('阿贝多', self)
        abd.triggered.connect(lambda: self.reshow('阿贝多'))
        self.pets.addAction(abd)
        bnt = QAction('班尼特', self)
        bnt.triggered.connect(lambda: self.reshow('班尼特'))
        self.pets.addAction(bnt)
        yl = QAction('优菈', self)
        yl.triggered.connect(lambda: self.reshow('优菈'))
        self.pets.addAction(yl)

        kq = QAction('刻晴', self)
        kq.triggered.connect(lambda: self.reshow('刻晴'))
        self.pets.addAction(kq)
        gy = QAction('甘雨', self)
        gy.triggered.connect(lambda: self.reshow('甘雨'))
        self.pets.addAction(gy)
        ht = QAction('胡桃', self)
        ht.triggered.connect(lambda: self.reshow('胡桃'))
        self.pets.addAction(ht)
        qq = QAction('七七', self)
        qq.triggered.connect(lambda: self.reshow('七七'))
        self.pets.addAction(qq)
        zl = QAction('钟离', self)
        zl.triggered.connect(lambda: self.reshow('钟离'))
        self.pets.addAction(zl)
        x = QAction('魈', self)
        x.triggered.connect(lambda: self.reshow('魈'))
        self.pets.addAction(x)
        xq = QAction('行秋', self)
        xq.triggered.connect(lambda: self.reshow('行秋'))
        self.pets.addAction(xq)
        ddly = QAction('达达利亚', self)
        ddly.triggered.connect(lambda: self.reshow('达达利亚'))
        self.pets.addAction(ddly)

        wy = QAction('枫原万叶', self)
        wy.triggered.connect(lambda: self.reshow('枫原万叶'))
        self.pets.addAction(wy)
        bcsz = QAction('八重神子', self)
        bcsz.triggered.connect(lambda: self.reshow('八重神子'))
        self.pets.addAction(bcsz)
        xg = QAction('宵宫', self)
        xg.triggered.connect(lambda: self.reshow('宵宫'))
        self.pets.addAction(xg)
        xh = QAction('珊瑚宫心海', self)
        xh.triggered.connect(lambda: self.reshow('珊瑚宫心海'))
        self.pets.addAction(xh)
        zy = QAction('早柚', self)
        zy.triggered.connect(lambda: self.reshow('早柚'))
        self.pets.addAction(zy)
        sllh = QAction('神里绫华', self)
        sllh.triggered.connect(lambda: self.reshow('神里绫华'))
        self.pets.addAction(sllh)
        hlyd = QAction('荒泷一斗', self)
        hlyd.triggered.connect(lambda: self.reshow('荒泷一斗'))
        self.pets.addAction(hlyd)
        ldjj = QAction('雷电将军', self)
        ldjj.triggered.connect(lambda: self.reshow('雷电将军'))
        self.pets.addAction(ldjj)
        sllr = QAction('神里绫人', self)
        sllr.triggered.connect(lambda: self.reshow('神里绫人'))
        self.pets.addAction(sllr)
        yl1 = QAction('夜兰', self)
        yl1.triggered.connect(lambda: self.reshow('夜兰'))
        self.pets.addAction(yl1)

        self.bgmusics = self.menu.addMenu('音乐')
        self.md_music = QAction('蒙德～', self) if self.bg_music == '蒙德' else QAction('蒙德', self)

        self.md_music.triggered.connect(lambda: self.set_audio(self.md_music.text()))
        self.bgmusics.addAction(self.md_music)

        self.ly_music = QAction('璃月～', self) if self.bg_music == '璃月' else QAction('璃月', self)
        self.ly_music.triggered.connect(lambda: self.set_audio(self.ly_music.text()))
        self.bgmusics.addAction(self.ly_music)

        self.dq_music = QAction('稻妻～', self) if self.bg_music == '稻妻' else QAction('稻妻', self)
        self.dq_music.triggered.connect(lambda: self.set_audio(self.dq_music.text()))
        self.bgmusics.addAction(self.dq_music)

        self.role_music = QAction('人物语音～', self) if self.audio_player else QAction('人物语音', self)
        # self.role_music.triggered.connect(self.role_audio)
        self.role_music.triggered.connect(lambda: self.set_audio(self.role_music.text()))
        self.bgmusics.addAction(self.role_music)
        self.music_off = QAction('关闭所有', self)
        self.music_off.triggered.connect(lambda: self.set_audio(self.music_off.text()))
        self.bgmusics.addAction(self.music_off)

        show = QAction('显示', self)
        show.triggered.connect(self.showwin)
        self.menu.addAction(show)

        quit = QAction('退出', self)
        quit.triggered.connect(self.quit)
        self.menu.addAction(quit)

        self.tp.setContextMenu(self.menu)
        self.tp.show()

    def reshow(self, name):
        """
        桌面宠物的替换
        """
        self.talk_path = [os.path.join(BASE_DIR, self.music_path, name, i) for i in
                          os.listdir(os.path.join(BASE_DIR, self.music_path, name)) if i.startswith('闲聊')]
        self.know_path = [os.path.join(BASE_DIR, self.music_path, name, i) for i in
                          os.listdir(os.path.join(BASE_DIR, self.music_path, name)) if i.startswith('想要了解')]
        if mixer.get_busy():
            mixer.stop()
        self.role_name = name
        config['role'] = name
        self.scale = config['frame_scale'][self.role_name][1]
        self.pos_x = random.randint(0, self.screenwidth)
        self.pos_y = random.randint(0, self.screenheight)
        self.file_path = os.path.join(BASE_DIR, self.img_path, self.role_name)
        self.file_list = sorted(os.listdir(self.file_path))
        self.img = QImage().load(os.path.join(BASE_DIR, self.file_path, str(self.file_list[1])))  # 获取第一张图片作为托盘图标
        self.init_window()
        self.tp.show()
        self.timer.start(config['frame_scale'][self.role_name][0])

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
            self.pos_x, self.pos_y = xy.x(), xy.y()
            event.accept()

    def mouseReleaseEvent(self, event):
        # 鼠标松开事件
        self.is_follow_mouse = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def keyPressEvent(self, event):
        # command & Q   ==>quit
        if event.key() == Qt.Key_Q and event.modifiers() == Qt.ControlModifier:
            self.quit()
        # command & +   ==>bigger
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_Equal:  # 两键组合
            self.scale += 0.01
        # command & -   ==>smaller
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_Minus:  # 两键组合
            self.scale -= 0.01
        config['frame_scale'][self.role_name][1] = self.scale

    def quit(self):
        # 退出程序
        with open(os.path.join(BASE_DIR, 'config.yaml'), 'w') as f:
            yaml.dump(config, f, default_flow_style=False, encoding='utf-8', allow_unicode=True)
        self.close()
        sys.exit()

    def contextMenuEvent(self, event):
        # 定义菜单
        menu = QMenu(self)
        konwing = menu.addAction("了解")
        talking = menu.addAction("闲聊")
        hide = menu.addAction("隐藏")
        quitAction = menu.addAction("退出")
        # 使用exec_()方法显示菜单。从鼠标右键事件对象中获得当前坐标。mapToGlobal()方法把当前组件的相对坐标转换为窗口（window）的绝对坐标。
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == quitAction:
            # qApp.quit()
            # mixer.Sound(os.path.join(BASE_DIR, music_path, role_name,'晚安.mp3')).play()
            self.quit()
        elif action == hide:
            # 通过设置透明度方式隐藏宠物
            self.setWindowOpacity(0)
        elif action == talking and self.audio_player and not mixer.get_busy():
            mixer.Sound(self.talk_path[random.randint(0, len(self.talk_path) - 1)]).play()
        elif action == konwing and self.audio_player and not mixer.get_busy():
            mixer.Sound(self.know_path[random.randint(0, len(self.know_path) - 1)]).play()

    def showwin(self):
        self.setWindowOpacity(1)

    # def role_audio(self):
    #     if not self.audio_player:
    #         self.role_music.setText('人物语音～')
    #         self.music_off.setText('关闭所有')
    #     else:
    #         self.role_music.setText('人物语音')
    #         # self.music_off.setText('关闭所有～')
    #         if mixer.get_busy():
    #             mixer.stop()
    #         if mixer.music.get_busy():
    #             mixer.music.stop()
    #     self.audio_player = not self.audio_player
    #     config['audio'] = self.audio_player

    def set_audio(self, area):
        """
        :param area: 输入相应的状态
        :return:
        """

        all_music = [self.md_music, self.ly_music, self.dq_music, self.role_music, self.music_off]

        # 判断是否为关闭所有
        if '关闭所有' in area:
            if '～' in area: # 之前为关闭所有 接下来需要取消关闭所有
                self.music_off.setText('关闭所有')
                pass
            else:   # 接下来需要关闭所有
                self.music_off.setText('关闭所有～')
                self.audio_player = False
                config['bg_music'] = False
                [m.setText(m.text().replace('～','')) for m in all_music[:-1]] # 修改对应的状态显示
                if mixer.get_busy():    # 关闭语音音效
                    mixer.stop()
                if mixer.music.get_busy():  # 关闭背景音效
                    mixer.music.stop()
        else: # 只是局部操作 [蒙德 璃月 稻妻]    [人物语音] 两者相互独立的
            if '～' in area:  # ～表示之前为选中状态 需要执行取消选中操作
                if area == '人物语音～':
                    self.role_music.setText('人物语音')
                    self.audio_player = False
                    if mixer.get_busy():  # 关闭语音音效
                        mixer.stop()
                else:
                    for m in all_music[:-2]:
                        m.setText(area[:-1]) if m.text() == area else m.setText(m.text().replace('～',''))
                    if mixer.music.get_busy():  # 关闭背景音效
                        mixer.music.stop()
            else:
                self.music_off.setText('关闭所有')
                if area == '人物语音':
                    self.role_music.setText('人物语音～')
                    self.audio_player = True
                else:
                    for m in all_music[:-2]:
                        m.setText(area+'～') if m.text() == area else m.setText(m.text().replace('～',''))
                    if mixer.music.get_busy():
                        mixer.music.stop()
                    mixer.music.load(os.path.join(BASE_DIR, self.music_path, area, 'background.mp3'))
                    mixer.music.play(-1)
                    config['bg_music'] = area
        config['audio'] = self.audio_player



        # if area == '关闭所有':
        #     self.music_off.setText('关闭所有～') if self.music_off.text() == '关闭所有' else self.music_off.setText('关闭所有')
        #     self.role_music.setText('人物语音')
        #     self.md_music.setText('蒙德')
        #     self.ly_music.setText('璃月')
        #     self.dq_music.setText('稻妻')
        #     config['bg_music'], config['audio'] = False, False
        #     if mixer.get_busy():
        #         mixer.stop()
        #     if mixer.music.get_busy():
        #         mixer.music.stop()
        # else:
        #     if area == '蒙德':
        #         self.md_music.setText('蒙德～') if self.md_music.text() == '蒙德' else self.md_music.setText('蒙德')
        #         self.ly_music.setText('璃月')
        #         self.dq_music.setText('稻妻')
        #         self.music_off.setText('关闭所有')
        #     elif area == '璃月':
        #         self.md_music.setText('蒙德')
        #         self.ly_music.setText('璃月～') if self.ly_music.text() == '璃月' else self.ly_music.setText('璃月')
        #         self.dq_music.setText('稻妻')
        #         self.music_off.setText('关闭所有')
        #     elif area == '稻妻':
        #         self.md_music.setText('蒙德')
        #         self.ly_music.setText('璃月')
        #         self.dq_music.setText('稻妻～') if self.dq_music.text() == '稻妻' else self.dq_music.setText('稻妻')
        #         self.music_off.setText('关闭所有')
        #
        #     status = [self.md_music.text(), self.ly_music.text(), self.dq_music.text()]
        #     # print(status)
        #     if status == ['蒙德', '璃月', '稻妻']:
        #         if mixer.music.get_busy():
        #             mixer.music.stop()
        #     if '蒙德～' in status or '璃月～' in status or '稻妻～' in status:
        #         if mixer.music.get_busy():
        #             mixer.music.stop()
        #         mixer.music.load(os.path.join(BASE_DIR, self.music_path, area, 'background.mp3'))
        #         mixer.music.play(-1)



if __name__ == '__main__':
    # 创建程序和对象
    app = QApplication(sys.argv)
    pet = Pet()
    sys.exit(app.exec_())
