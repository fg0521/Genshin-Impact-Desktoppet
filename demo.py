import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QBitmap, QPainter, QPixmap, QCursor, QMovie
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QMessageBox, QApplication, QVBoxLayout, QWidget, \
    QLabel, QGridLayout, QLineEdit, QTextEdit, QFormLayout, QComboBox

'''
PyQt5 装载Gif动画 案例
QMovie
'''


class LoadingGifDemo(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置定位和左上角坐标
        # self.setGeometry(300, 300, 360, 260)
        # 设置窗口标题
        self.setWindowTitle('异形窗口 的演示')
        # 设置窗口图标
        # self.setWindowIcon(QIcon('../web.ico'))
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # self.setStyleSheet('''background-color:black; ''')
        self.label = QLabel("", self)
        self.setFixedSize(658, 494)
        # self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 窗口无边框
        self.setAttribute(Qt.WA_TranslucentBackground)  # 窗口透明
        # self.setAutoFillBackground(False)  # 设置窗口背景透明
        # self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.movie = QMovie('/Users/maoyufeng/slash/project/yuanshen-desktoppet/gif/keli.gif')
        self.label.setMovie(self.movie)
        self.movie.start()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    # 设置应用图标
    app.setWindowIcon(QIcon('../web.ico'))
    w = LoadingGifDemo()

    w.show()
    sys.exit(app.exec_())