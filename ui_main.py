from sqlite3 import InterfaceError
import sys, os
import cv2, imutils
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

        self.filename = None
        self.tmp = None


    def loadImage(self):
        self.filename = QFileDialog.getOpenFileName(filter="Image (*.*) ")[0]
        # getOpenFileName은 취소를 눌렀을 때 빈 QString을 반환한다. 
        # 이때 이 QString은 거짓으로 간주되므로 밑의 if문을 통해 실제로 값이 반환되었을 때에만 함수가 실행되도록 한다.
        if self.filename :
            self.image = cv2.imread(self.filename)
            self.setPhoto(self.image)

    def setPhoto(self, image):
        self.tmp = image
        image = imutils.resize(image, width = 750)
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        self.imageLable.setPixmap(QtGui.QPixmap.fromImage(image))


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
        self.btnVignet.clicked.connect(self.mainVClicked)
        self.btnWhite.clicked.connect(self.mainWClicked)

    def contents(self):
        self.contentsFrame = QFrame(self)
        self.contentsFrame.setGeometry(70, 65, 1050, 1000)
        self.contentsVBox = QVBoxLayout(self.contentsFrame)

        #stackedWidget 사용법 
        self.stkedWidget = QStackedWidget()
        self.stkedWidget.addWidget(MainMenu())
        self.stkedWidget.addWidget(ResMenu())
        self.stkedWidget.addWidget(VinettingMenu())

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
    def mainVClicked(self):
        self.stkedWidget.setCurrentIndex(2)
    
    @pyqtSlot()
    def mainWClicked(self):
        self.stkedWidget.setCurrentIndex(0)

    # 드래그 앤 드롭의 구현
    # def dragEnterEvent(self, event):
    #     if event.mimeData().hasImage:
    #         event.accept()
    #     else:
    #         event.ignore()

    # def dragMoveEvent(self, event):
    #     if event.mimeData().hasImage:
    #         event.accept()
    #     else:
    #         event.ignore()

    # def drogEvent(self, event):
    #     if event.mimeData().hasImage:
    #         event.setDropAction(Qt.CopyAction)
    #         file_path = event.mimeData().urls()[0].toLocalFile()
    #         self.set_image(file_path)

    #         event.accept()
    #     else:
    #         event.ignore()

    def set_image(self, file_path):
        self.imageLable.setPixmap(QPixmap(file_path))

    def btn_close_clicked(self):
        self.close()

    def btn_min_clicked(self):
        self.showMinimized()

    


class MainMenu(QWidget):
# mainContent의 이미지를 받아들이는 공간
    def __init__(self):
        super(MainMenu, self).__init__()
        self.imageContent()
        self.interfaceContent()
        self.filename = None
        self.tmp = None


    def loadImage(self):
        self.filename = QFileDialog.getOpenFileName(filter="Image (*.*) ")[0]
        # getOpenFileName은 취소를 눌렀을 때 빈 QString을 반환한다. 
        # 이때 이 QString은 거짓으로 간주되므로 밑의 if문을 통해 실제로 값이 반환되었을 때에만 함수가 실행되도록 한다.
        if self.filename :
            self.image = cv2.imread(self.filename)
            self.setPhoto(self.image)

    def setPhoto(self, image):
        self.tmp = image
        image = imutils.resize(image, width = 750)
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        self.imageLable.setPixmap(QtGui.QPixmap.fromImage(image))

    def imageContent(self):
        self.imageLable = QLabel(self)
        self.imageLable.setAlignment(Qt.AlignCenter)
        self.imageLable.setText("Drop Image Here")
        self.imageLable.setFont(QFont('Segoe UI', 18))
        self.imageLable.setGeometry(0, 0, 750, 750)
        self.imageLable.setStyleSheet(
            """
            QLabel{
                color : white;
                border : 3px;
                border-style: dashed;
                border-color: white;
            }
            """
        )

        self.fileOpenBtn = QPushButton('SELECT IMAGE', self)
        self.fileOpenBtn.setFont(QFont('Segoe UI', 12))
        self.fileOpenBtn.clicked.connect(self.loadImage)
        self.fileOpenBtn.setMaximumWidth(250)
        self.fileOpenBtn.setStyleSheet(
            """
            QPushButton{
                background-color : rgba(20, 25, 30, 0.5); 
                color : white;
                margin-top : 5px;
                padding : 7px 20px;
                border : 0px;
                border-radius : 5px;
            }
            
            QPushButton::hover{ 
                background-color : rgba(20, 25, 30, 1); 
            }
            """
        )
        

        self.contentFrame = QFrame(self)
        self.contentFrame.setGeometry(0, 0, 800, 800)
        
        self.contentVBox = QVBoxLayout(self.contentFrame)
        self.contentVBox.addWidget(self.imageLable)
        self.contentVBox.addWidget(self.fileOpenBtn, alignment=QtCore.Qt.AlignHCenter) # AlignHCenter를 통해 fileOpenBtn을 정렬

# mainContent의 interface 메뉴
    def interfaceContent(self):
        self.resolutionCBox = QCheckBox('Resolution', self)
        self.resolutionCBox.setFont(QFont('Segoe UI', 12))
        self.resolutionCBox.setStyleSheet(
            """
            QCheckBox{
                width : 30px;
                height : 30px;
                font-size : 22px;
                color : white;
            }
            """
        )

        self.vignettingCBox = QCheckBox('Vignetting', self)
        self.vignettingCBox.setFont(QFont('Segoe UI', 12))
        self.vignettingCBox.setStyleSheet(
            """
            QCheckBox{
                width : 30px;
                height : 30px;
                font-size : 22px;
                color : white;
            }
            """
        )

        self.whiteBalanceCBox = QCheckBox('WhiteBalance', self)
        self.whiteBalanceCBox.setFont(QFont('Segoe UI', 12))
        self.whiteBalanceCBox.setStyleSheet(
            """
            QCheckBox{
                width : 30px;
                height : 30px;
                font-size : 22px;
                color : white;
            }
            """
        )

        self.focusCBox = QCheckBox('Focus', self)
        self.focusCBox.setFont(QFont('Segoe UI', 12))
        self.focusCBox.setStyleSheet(
            """
            QCheckBox{
                width : 30px;
                height : 30px;
                font-size : 22px;
                color : white;
            }
            """
        )


        self.analyzerLabel = QLabel(self)
        self.analyzerLabel.setText("Analyzer")
        self.analyzerLabel.setFont(QFont('Segoe UI', 30))

        self.interfaceFrame = QFrame(self)
        self.interfaceFrame.setGeometry(830, 0, 200, 500)

        self.interfaceContentVBox = QVBoxLayout(self.interfaceFrame)
        self.interfaceContentVBox.addWidget(self.analyzerLabel)
        self.interfaceContentVBox.addWidget(self.resolutionCBox)
        self.interfaceContentVBox.addWidget(self.vignettingCBox)
        self.interfaceContentVBox.addWidget(self.whiteBalanceCBox)
        self.interfaceContentVBox.addWidget(self.focusCBox)


class ResMenu(QWidget):
    def __init__(self):
        super(ResMenu, self).__init__()
        

    def interfaceContent(self):
        self.resolutionCBox = QCheckBox('Resolution', self)
        self.resolutionCBox.setFont(QFont('Segoe UI', 12))
        self.resolutionCBox.setStyleSheet(
            """
            QCheckBox{
                width : 30px;
                height : 30px;
                font-size : 22px;
                color : white;
            }
            """
        )

        self.vignettingCBox = QCheckBox('Vignetting', self)
        self.vignettingCBox.setFont(QFont('Segoe UI', 12))
        self.vignettingCBox.setStyleSheet(
            """
            QCheckBox{
                width : 30px;
                height : 30px;
                font-size : 22px;
                color : white;
            }
            """
        )

        self.whiteBalanceCBox = QCheckBox('WhiteBalance', self)
        self.whiteBalanceCBox.setFont(QFont('Segoe UI', 12))
        self.whiteBalanceCBox.setStyleSheet(
            """
            QCheckBox{
                width : 30px;
                height : 30px;
                font-size : 22px;
                color : white;
            }
            """
        )

        self.focusCBox = QCheckBox('Focus', self)
        self.focusCBox.setFont(QFont('Segoe UI', 12))
        self.focusCBox.setStyleSheet(
            """
            QCheckBox{
                width : 30px;
                height : 30px;
                font-size : 22px;
                color : white;
            }
            """
        )


        self.analyzerLabel = QLabel(self)
        self.analyzerLabel.setText("Analyzer")
        self.analyzerLabel.setFont(QFont('Segoe UI', 30))

        self.interfaceFrame = QFrame(self)
        self.interfaceFrame.setGeometry(900, 65, 200, 500)

        self.interfaceContentVBox = QVBoxLayout(self.interfaceFrame)
        self.interfaceContentVBox.addWidget(self.analyzerLabel)
        self.interfaceContentVBox.addWidget(self.resolutionCBox)
        self.interfaceContentVBox.addWidget(self.vignettingCBox)
        self.interfaceContentVBox.addWidget(self.whiteBalanceCBox)
        self.interfaceContentVBox.addWidget(self.focusCBox)

class EdgeMenu(QWidget):
    def __init__(self):
        super(EdgeMenu, self).__init__()

    def imageBox(self):
        self.imageLable = QLabel(self)
        self.imageLable.setAlignment(Qt.AlignCenter)
        self.imageLable.setText("Edge Image")
        self.imageLable.setFont(QFont('Segoe UI', 18))
        self.imageLable.setGeometry(0, 0, 750, 750)
        self.imageLable.setStyleSheet(
            """
            QLabel{
                color : white;
                border : 3px;
                border-style: dashed;
                border-color: white;
            }
            """
        )

        self.contentFrame = QFrame(self)
        self.contentFrame.setGeometry(0, 0, 800, 800)
        
        self.contentVBox = QVBoxLayout(self.contentFrame)
        self.contentVBox.addWidget(self.imageLable)

class VinettingMenu(QWidget):
    def __init__(self):
        super(VinettingMenu, self).__init__()
        self.imageBox()
        self.pass_fail_check()

    def imageBox(self):
        self.imageLable = QLabel(self)
        self.imageLable.setAlignment(Qt.AlignCenter)
        self.imageLable.setText("Vinetting Image")
        self.imageLable.setFont(QFont('Segoe UI', 18))
        self.imageLable.setGeometry(0, 0, 750, 750)
        self.imageLable.setStyleSheet(
            """
            QLabel{
                color : white;
                border : 3px;
                border-style: dashed;
                border-color: white;
            }
            """
        )

        self.contentFrame = QFrame(self)
        self.contentFrame.setGeometry(0, 0, 800, 800)
        
        self.contentVBox = QVBoxLayout(self.contentFrame)
        self.contentVBox.addWidget(self.imageLable)

    def pass_fail_check(self):
        self.pass_fail = QLabel(self)
        self.pass_fail.setText("Vinetting Check")
        self.pass_fail.setFont(QFont('Segoe UI', 30))

        self.pass_fail_frame = QFrame(self)
        self.pass_fail_frame.setGeometry(830, 0, 200, 500)

        self.interfaceContentVBox = QVBoxLayout(self.pass_fail_frame)
        self.interfaceContentVBox.addWidget(self.pass_fail)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
