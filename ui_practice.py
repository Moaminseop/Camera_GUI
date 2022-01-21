import sys, os
from ui_contents import MainMenu, ResMenu, EdgeMenu, VinettingMenu, VinettingResMenu
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.titleBar()
        self.sideBar()
        self.initUI()
        self.contents()


# 마우스를 통해 창을 이동할 수 있게 만드는 함수들
    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton:
            self.m_flag=True
            self.m_Position=event.globalPos()-self.pos()
            event.accept()
            
    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:  
            self.move(QMouseEvent.globalPos()-self.m_Position)
            QMouseEvent.accept()
            
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag=False


# 초기 ui설정
    def initUI(self):
        self.setWindowTitle('Camver')
        self.resize(1180, 875)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("""
                            background-color : rgb(40, 44, 52);
                            """)


# titleBar 설정
    def titleBar(self):
        self.app_label = QLabel('Camver', self)
        self.app_label.setFont(QFont('Segoe UI', 13))
        self.app_label.setStyleSheet(
            '''
            QLabel{ 
                color : #ffffff; 
                background-color : rgb(33, 37, 43); 
                margin-bottom : px; }
            ''')

        self.favicon_label = QLabel(self)
        self.favicon_label.setPixmap(QPixmap('./image/icon/favicon.png').scaled(25, 25))
        self.favicon_label.setStyleSheet(
            '''
            QLabel{ 
                background-color : rgb(33, 37, 43); 
                margin-right : 10px; 
                margin-left : 2px;
                margin-top : 2px;
                margin-bottom : px; }
            ''')

        self.btn_close = QPushButton(self) 
        self.btn_close.setStyleSheet(
            '''
            QPushButton{ 
                background-color : rgb(33, 37, 43); 
                border : 0px; 
                border-radius : 3px;
                margin-top : 2px; }
            QPushButton::hover { background-color : #000000 }
            ''')
        
        self.btn_close.setIcon(QIcon('./image/icon/icon_close.png'))
        self.btn_close.setIconSize(QSize(20, 20))
        self.btn_close.clicked.connect(self.btn_close_clicked)

        self.btn_min = QPushButton(self) 
        self.btn_min.setStyleSheet(
            '''
            QPushButton{ background-color : rgb(33, 37, 43); 
            border : 0px; 
            border-radius : 3px;
            margin-top : 2px; }
            QPushButton::hover { background-color : #000000 }
            ''')
        self.btn_min.setIcon(QIcon('./image/icon/icon_min.png'))
        self.btn_min.setIconSize(QSize(20, 20))
        self.btn_min.clicked.connect(self.btn_min_clicked)

      
        self.btn_max = QPushButton(self) 
        self.btn_max.setStyleSheet(
            '''
            QPushButton{ 
                background-color : rgb(33, 37, 43); 
                border : 0px; 
                border-radius : 3px;
                margin-top : 2px; }
            ''')
        self.btn_max.setIcon(QIcon('./image/icon/icon_max.png'))
        self.btn_max.setIconSize(QSize(20, 20))

        self.btn_max.setCheckable(True)
        
        self.titleFrame = QFrame(self)
        self.titleFrame.setGeometry(0, 0, 1180, 50)
        self.titleFrame.setStyleSheet(
            ''' 
            QWidget{ 
                background-color : rgb(33, 37, 43); }
            ''')
        
        self.titleHBox= QHBoxLayout(self.titleFrame) 
        self.titleHBox.addWidget(self.favicon_label)
        self.titleHBox.addWidget(self.app_label)
        self.titleHBox.addStretch(1)
        self.titleHBox.addWidget(self.btn_min)
        self.titleHBox.addWidget(self.btn_max)
        self.titleHBox.addWidget(self.btn_close)

    def sideBar(self):
        self.btnMenu = QPushButton(self)
        self.btnMenu.setIcon(QIcon('./image/icon/menu.png'))
        self.btnMenu.setIconSize(QSize(45, 45))
        self.btnMenu.setToolTip('메인 메뉴')
        self.btnMenu.setStyleSheet(
            '''
            QPushButton{ 
                background-color : rgb(33, 37, 43); 
                border : 0px; 
                border-radius : 3px;
                margin-top : 10px; }
            QPushButton::hover { background-color : #ffffff }
            ''')

        self.btnResortion = QPushButton(self)
        self.btnResortion.setIcon(QIcon('./image/icon/resortion.png'))
        self.btnResortion.setIconSize(QSize(45, 45))
        self.btnResortion.setToolTip('해상력 결과 확인')
        self.btnResortion.setStyleSheet(
            '''
            QPushButton{ 
                background-color : rgb(33, 37, 43); 
                border : 0px; 
                border-radius : 3px;
                margin-top : 10px; }
            QPushButton::hover { background-color : #ffffff }
            ''')

        self.btnEdge = QPushButton(self)
        self.btnEdge.setIcon(QIcon('./image/icon/edge.png'))
        self.btnEdge.setIconSize(QSize(45, 45))
        self.btnEdge.setToolTip('엣지 결과 확인')
        self.btnEdge.setStyleSheet(
            '''
            QPushButton{ 
                background-color : rgb(33, 37, 43); 
                border : 0px; 
                border-radius : 3px;
                margin-top : 10px; }
            QPushButton::hover { background-color : #ffffff }
            ''')

        self.btnVignet = QPushButton(self)
        self.btnVignet.setIcon(QIcon('./image/icon/vignetting.png'))
        self.btnVignet.setIconSize(QSize(45, 45))
        self.btnVignet.setToolTip('비네팅 이미지 입력')
        self.btnVignet.setStyleSheet(
            '''
            QPushButton{ 
                background-color : rgb(33, 37, 43); 
                border : 0px; 
                border-radius : 3px;
                margin-top : 10px; }
            QPushButton::hover { background-color : #ffffff }
            ''')
        
        self.btnWhite = QPushButton(self)
        self.btnWhite.setIcon(QIcon('./image/icon/whiteBalance.png'))
        self.btnWhite.setIconSize(QSize(45, 45))
        self.btnWhite.setToolTip('비네팅 결과 확인')
        self.btnWhite.setStyleSheet(
            '''
            QPushButton{ 
                background-color : rgb(33, 37, 43); 
                border : 0px; 
                border-radius : 3px;
                margin-top : 10px; }
            QPushButton::hover { background-color : #ffffff }
            ''')

        self.sideFrame = QFrame(self)
        self.sideFrame.setGeometry(0, 50, 60, 850)
        self.sideFrame.setStyleSheet(
            ''' 
            QWidget{ 
                background-color : rgb(33, 37, 43); }
            ''')

        
        self.sideVBox = QVBoxLayout(self.sideFrame)
        self.sideVBox.addWidget(self.btnMenu)
        self.sideVBox.addWidget(self.btnResortion)
        self.sideVBox.addWidget(self.btnEdge)
        self.sideVBox.addWidget(self.btnVignet)
        self.sideVBox.addWidget(self.btnWhite)
        self.sideVBox.addStretch(1)

        self.btnMenu.clicked.connect(self.mainMClicked)
        self.btnResortion.clicked.connect(self.mainRClicked)
        self.btnEdge.clicked.connect(self.mainEClicked)
        self.btnVignet.clicked.connect(self.mainVClicked)
        self.btnWhite.clicked.connect(self.mainWClicked)

    def btn_close_clicked(self):
        self.close()

    def btn_min_clicked(self):
        self.showMinimized()



    def contents(self):
        self.contentsFrame = QFrame(self)
        self.contentsFrame.setGeometry(70, 65, 1050, 1000)
        self.contentsVBox = QVBoxLayout(self.contentsFrame)

        #stackedWidget 사용법 
        self.stkedWidget = QStackedWidget()
        self.stkedWidget.addWidget(MainMenu())
        self.stkedWidget.addWidget(ResMenu())
        self.stkedWidget.addWidget(EdgeMenu())
        self.stkedWidget.addWidget(VinettingMenu())
        self.stkedWidget.addWidget(VinettingResMenu())

        self.stkedWidget.setCurrentIndex(0) #초기 인덱스 0번으로 하여서 mainMenu가 보이도록 한다
        self.contentsVBox.addWidget(self.stkedWidget) # 위젯을 보이도록 설정한다.


    #pyqtSlot을 사용하여 각각의 버튼이 클릭되었을때의 화면이 보이도록 한다.
    @pyqtSlot()
    def mainMClicked(self):
        self.stkedWidget.setCurrentIndex(0)

    @pyqtSlot()
    def mainRClicked(self):
        self.stkedWidget.setCurrentIndex(1)

    @pyqtSlot()
    def mainEClicked(self):
        self.stkedWidget.setCurrentIndex(2)

    @pyqtSlot()
    def mainVClicked(self):
        self.stkedWidget.setCurrentIndex(3)
    
    @pyqtSlot()
    def mainWClicked(self):
        self.stkedWidget.setCurrentIndex(4)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
