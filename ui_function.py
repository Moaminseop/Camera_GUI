import sys, time
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class Viewer(QtWidgets.QGraphicsView): #뷰어의 역할을 해주는 것, 그래픽을 통해 좌표를 넘겨줌
    def __init__(self, parent=None):
        super().__init__(QtWidgets.QGraphicsScene(), parent)
        self.pixmap_item = self.scene().addPixmap(QtGui.QPixmap())
        self.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.rect_item = QGraphicsRectItem(QRectF(), self.pixmap_item)
        self.rect_item.setPen(QPen(QColor(0, 255, 0), 3, Qt.SolidLine))

        #외부에서 좌표를 입력받는 라벨을 설정
        x, y = 0, 0
        self.initPos = "x:{0}, y:{1}".format(x, y)

        self.startLabel = QLineEdit(self.initPos, self)
        self.endLabel = QLineEdit(self.initPos, self)

    def setPixmap(self, pixmap): # 클래스 내부에서 외부 호출을 통해 이미지를 받는 함수
        self.pixmap_item.setPixmap(pixmap)

    def mousePressEvent(self, event):
        self.pi = self.mapToScene(event.pos())
        super().mousePressEvent(event)
        self.startXais = event.x()
        self.startYais = event.y()
        startPos = "x:{0: .0f}, y:{1: .0f}".format(self.startXais, self.startYais)
        self.startLabel.setText(startPos)

    def mouseMoveEvent(self, event):
        pf = self.mapToScene(event.pos())
        if (self.pi - pf).manhattanLength() > QApplication.startDragDistance():
            self.pf = pf
            self.draw_rect()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        pf = self.mapToScene(event.pos())
        self.endXais = self.pf.x()
        self.endYais = self.pf.y()
        endPos = "x:{0: .0f}, y:{1: .0f}".format(self.endXais, self.endYais)
        self.endLabel.setText(endPos)
        if (self.pi - pf).manhattanLength() > QApplication.startDragDistance():
            self.pf = pf
            self.draw_rect()
        super().mouseReleaseEvent(event)

    def draw_rect(self):
        xais = self.pf.x()
        yais = self.pf.y()

        # 박스가 - 좌표로 가는것을 막는 예외처리
        if int(self.pf.x()) <= 0:
            self.pf = QPointF(0, yais)

        if int(self.pf.y()) <= 0:
            self.pf = QPointF(xais, 0)

        if int(self.pf.x()) <= 0 and int(self.pf.y()) <= 0:
            self.pf = QPointF(0, 0)

        r = QRectF(self.pi, self.pf).normalized()
        r = self.rect_item.mapFromScene(r).boundingRect()
        self.rect_item.setRect(r)




class LoadingScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(200, 200)
        self.setWindowFlags(Qt.FramelessWindowHint) 

        self.loadingLabel = QLabel(self)

        self.movie = QMovie('./image/loading.gif')

        self.loadingLabel.setMovie(self.movie)
        self.startAnimation()
        self.show()

        timer = QTimer(self)
        t = time
        t.sleep(3)

    def startAnimation(self):
        self.movie.start()

    def endAnimation(self):
        self.movie.stop()
        self.close()

    