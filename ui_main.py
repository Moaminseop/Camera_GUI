from sqlite3 import InterfaceError
import sys, os
import cv2, imutils, numpy, re, math
from scipy.ndimage import gaussian_filter1d
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
    def mainVClicked(self):
        self.stkedWidget.setCurrentIndex(2)
    
    @pyqtSlot()
    def mainWClicked(self):
        self.stkedWidget.setCurrentIndex(3)

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

    
class Viewer(QtWidgets.QGraphicsView): #뷰어의 역할을 해주는 것, 그래픽을 통해 좌표를 넘겨줌
    
    def __init__(self, parent=None):
        super().__init__(QtWidgets.QGraphicsScene(), parent)
        self.pixmap_item = self.scene().addPixmap(QtGui.QPixmap()) #scene은 내장함수
        self.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.setBackgroundRole(QtGui.QPalette.Dark)
        self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)
        self.rubberBandChanged.connect(self.onRubberBandChanged)
        self.last_rect = QtCore.QPointF()


        #외부에서 좌표를 입력받는 라벨을 설정
        x, y = 0, 0
        self.initPos = "x:{0}, y:{1}".format(x, y)

        self.startLabel = QLineEdit(self.initPos, self)
        self.endLabel = QLineEdit(self.initPos, self)
        self.setMouseTracking(True)
        
    def setPixmap(self, pixmap):
        self.pixmap_item.setPixmap(pixmap)

    
    @QtCore.pyqtSlot(QtCore.QRect, QtCore.QPointF, QtCore.QPointF)
    def onRubberBandChanged(self, rubberBandRect, fromScenePoint, toScenePoint):
        if rubberBandRect.isNull():
            pixmap = self.pixmap_item.pixmap()
            rect = self.pixmap_item.mapFromScene(self.last_rect).boundingRect().toRect()
            if not rect.intersected(pixmap.rect()).isNull():
                crop_pixmap = pixmap.copy(rect)
                label = QtWidgets.QLabel(pixmap=crop_pixmap)
                dialog = QtWidgets.QDialog(self)
                lay = QtWidgets.QVBoxLayout(dialog)
                lay.addWidget(label)
                dialog.exec_()
            self.last_rect = QtCore.QRectF()
        else:
            self.last_rect = QtCore.QRectF(fromScenePoint, toScenePoint)

            #입력받고싶은 좌표를 함수 내부에서 설정 
            self.startXais = fromScenePoint.x()
            self.startYais = fromScenePoint.y()
            self.endXais = toScenePoint.x()
            self.endYais = toScenePoint.y()

            startPos = "x:{0: .0f}, y:{1: .0f}".format(self.startXais, self.startYais)
            endPos = "x:{0: .0f}, y:{1: .0f}".format(self.endXais, self.endYais)
            self.startLabel.setText(startPos)
            self.endLabel.setText(endPos)

     

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
        # getOpenself.filename은 취소를 눌렀을 때 빈 QString을 반환한다. 
        # 이때 이 QString은 거짓으로 간주되므로 밑의 if문을 통해 실제로 값이 반환되었을 때에만 함수가 실행되도록 한다.
        if self.filename:
            self.image = cv2.imread(self.filename)
            self.setPhoto(self.image)

    def setPhoto(self, image):
        self.tmp = image
        image = imutils.resize(image, width = 760)
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        cv2.imwrite('setimage.png', frame)
        self.view.setPixmap(QtGui.QPixmap.fromImage(image))

    def imageContent(self):

        self.view = Viewer()

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
        self.contentVBox.addWidget(self.view)
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

        self.startLine = self.view.startLabel
        self.endLine = self.view.endLabel
        self.lineText = QLineEdit(self)
        self.directionText = QLineEdit(self)

        self.startLine.setMaximumWidth(100)
        self.startLine.setStyleSheet(
            """
            QLineEdit{
                color : white;
            }
            """
        )

        self.endLine.setMaximumWidth(100)
        self.endLine.setStyleSheet(
            """
            QLineEdit{
                color : white;
            }
            """
        )

        self.lineText.setMaximumWidth(100)
        self.lineText.setStyleSheet(
            """
            QLineEdit{
                color : white;
            }
            """
        )

        self.directionText.setMaximumWidth(100)
        self.directionText.setStyleSheet(
            """
            QLineEdit{
                color : white;
            }
            """
        )

        self.edgeCBox = QCheckBox('Edge', self)
        self.edgeCBox.setFont(QFont('Segoe UI', 12))
        self.edgeCBox.setStyleSheet(
            """
            QCheckBox{
                width : 30px;
                height : 30px;
                font-size : 22px;
                color : white;
            }
            """
        )

        self.analyzBtn = QPushButton('Analyze', self)
        self.analyzBtn.setFont(QFont('Segoe UI', 12))
        self.analyzBtn.setMaximumWidth(100)
        self.analyzBtn.clicked.connect(self.analyzFunc)
        self.analyzBtn.setStyleSheet(
            """
            QPushButton{
                color : white;
                width : 50px;
            }

            QPushButton::hover{ 
                background-color : rgba(20, 25, 30, 1); 
            }
            """
        )

        self.analyzerLabel = QLabel(self)
        self.analyzerLabel.setText("Analyzer")
        self.analyzerLabel.setFont(QFont('Segoe UI', 30))
        self.analyzerLabel.setStyleSheet(
            """
            QLabel{
                color : white;
            }
            """
        )

        self.interfaceFrame = QFrame(self)
        self.interfaceFrame.setGeometry(850, 0, 200, 500)

        self.interfaceContentVBox = QVBoxLayout(self.interfaceFrame)
        self.interfaceContentVBox.addWidget(self.analyzerLabel)
        
        self.interfaceContentVBox.addWidget(self.resolutionCBox)
        self.interfaceContentVBox.addWidget(self.startLine)
        self.interfaceContentVBox.addWidget(self.endLine)
        self.interfaceContentVBox.addWidget(self.lineText)
        self.interfaceContentVBox.addWidget(self.directionText)

        self.interfaceContentVBox.addWidget(self.edgeCBox)

        self.interfaceContentVBox.addWidget(self.analyzBtn, alignment=QtCore.Qt.AlignHCenter)

    def analyzFunc(self):
        if self.filename:
            self.startPoint = self.startLine.text()
            self.endPoint = self.endLine.text()
            lineStr = self.lineText.text()
            directionStr = self.directionText.text()

            start = re.findall(r'\d+', self.startPoint)
            intstart = list(map(int, start))
            end = re.findall(r'\d+', self.endPoint)
            intend = list(map(int, end))

            startlist = []
            startlist.append(intstart)

            endlist = []
            endlist.append(intend)

            line = []
            line.append(int(lineStr))

            direction = []
            direction.append(int(directionStr))

            testRes('setimage.png', startlist, endlist, line, direction)


class ResMenu(QWidget):
    def __init__(self):
        super(ResMenu, self).__init__()
        self.imageBox()
        self.imageButton()

    def loadImage(self):
        self.image = cv2.imread('resresult.png')
        self.setPhoto(self.image)

    def setPhoto(self, image):
        self.tmp = image
        image = imutils.resize(image, width = 750)
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        self.imageLable.setPixmap(QtGui.QPixmap.fromImage(image))


    def imageBox(self):
        self.imageLable = QLabel(self)
        self.imageLable.setAlignment(Qt.AlignCenter)
        self.imageLable.setText("Resolution Image\n No image detected")
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
        self.contentFrame.setGeometry(0, 0, 780, 780)
        
        self.contentVBox = QVBoxLayout(self.contentFrame)
        self.contentVBox.addWidget(self.imageLable)
    
    def imageButton(self):
        self.imageBtn = QPushButton('Image load', self)
        self.imageBtn.setFont(QFont('Segoe UI', 15))
        self.imageBtn.clicked.connect(self.loadImage)
        self.interfaceFrame = QFrame(self)
        self.interfaceFrame.setGeometry(830, 0, 200, 500)

        self.interfaceContentVBox = QVBoxLayout(self.interfaceFrame)
        self.interfaceContentVBox.addWidget(self.imageBtn)

    
def testRes(imgAddress, start, end, line , direction): # 이미지 주소와 ROI의 좌상단픽셀, ROI의 우하단픽셀위치, 줄 수,검사방향을 입력받습니다.
    img = cv2.imread(imgAddress)
    height, width, channel = img.shape
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    result = [] # 1 or 0 으로 각 영역의 pass or fail 여부를 의미합니다.
    for x in range(len(start)):
        result.append(1)

    countedlimit = []  # 해상력 한계치의 좌표를 의미합니다.
    for x in range(len(start)):
        countedlimit.append([])

    # 흑백으로 변환된 이미지로부터 픽셀 밝기의 범위중앙값을 계산합니다. (white255, black0)
    min = 255
    max = 0
    for y in range(0, height):
        for x in range(0, width):
            if (img_gray[y,x] > max):
                max = img_gray[y,x]
            if (img_gray[y,x] < min):
                min = img_gray[y,x]
    mean = int((min+max)/2)

    # ROI의 좌측상단에서 세로로 한줄씩 오른쪽으로 이동하며 해상력을 테스트합니다.

    for i in range(len(start)):
        if (direction[i] == 1): # 검사방향 : 왼쪽 > 오른쪽
            countedline = 0
            # 한 줄만이라도 모든 판단선을 검출하지 못했을시 break
            for x in range(start[i][0], end[i][0]):
                countedline = 0
                countedlimit[i] = x
                for y in range(start[i][1], end[i][1]):
                    if ((img_gray[y-1,x]>mean) and (img_gray[y,x]<=mean)):
                        countedline+=1
                if countedline<line[i]:
                    if(x < (start[i][0]+end[i][0])/2):
                        result[i]=0
                    # else:
                    #     result[i]=[1]
                    break

        if (direction[i] == 2): # 검사방향 : 오른쪽 > 왼쪽
            countedline = 0
            # 한 줄만이라도 모든 판단선을 검출하지 못했을시 break
            for x in range(end[i][0], start[i][0], -1):
                countedline = 0
                countedlimit[i] = x
                for y in range(start[i][1], end[i][1]):
                    if ((img_gray[y-1,x]>mean) and (img_gray[y,x]<=mean)):
                        countedline+=1
                if countedline<line[i]:
                    if(x > (start[i][0]+end[i][0])/2):
                        result[i]=0
                    # else:
                    #     result[i]=[1]
                    break

        if (direction[i] == 3): # 검사방향 : 위 > 아래
            countedline = 0
            # 한 줄만이라도 모든 판단선을 검출하지 못했을시 break
            for y in range(start[i][1], end[i][1]):
                countedline = 0
                countedlimit[i] = y
                for x in range(start[i][0], end[i][0]):
                    if ((img_gray[y,x-1]>mean) and (img_gray[y,x]<=mean)):
                        countedline+=1
                if countedline<line[i]:
                    if(y < (start[i][1]+end[i][1])/2):
                        result[i]=0
                    # else:
                    #     result[i]=[1]
                    break

        if (direction[i] == 4): # 검사방향 : 아래 > 위
            countedline = 0
            # 한 줄만이라도 모든 판단선을 검출하지 못했을시 break
            for y in range( end[i][1],start[i][1],-1):
                countedline = 0
                countedlimit[i] = y
                for x in range(start[i][0], end[i][0]):
                    if ((img_gray[y,x-1]>mean) and (img_gray[y,x]<=mean)):
                        countedline+=1
                if countedline<line[i]:
                    if(y > (start[i][1]+end[i][1])/2):
                        result[i]=0
                    # else:
                    #     result[i]=[1]
                    break

    # 계산된 countedx와 ROI를 그림에 표시합니다.
    for i in range(len(start)):
        cv2.rectangle(img, start[i], end[i], (0, 255, 0), thickness = 2)
        if (direction[i] == 1) or (direction[i] == 2):
            for y in range(start[i][1], end[i][1]):
                img[y, countedlimit[i]] = 255,0,0
                img[y, int((start[i][0]+end[i][0])/2)] = 0,255,0
        elif (direction[i] == 3) or (direction[i] == 4):
            for x in range(start[i][0], end[i][0]):
                img[countedlimit[i],x] = 255,0,0
                img[int((start[i][1] + end[i][1])/2), x] = 0,255,0

    # cv.imshow(imgAddress, img)
    cv2.imwrite("resresult.png", img)

    pf = 0
    for i in range(len(result)-1):
        pf = result[i] and result[i+1]

    return pf


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
        self.vinetImageBox()


    def loadImage(self):
        self.filename = QFileDialog.getOpenFileName(filter="Image (*.*) ")[0]
        # getOpenself.filename은 취소를 눌렀을 때 빈 QString을 반환한다. 
        # 이때 이 QString은 거짓으로 간주되므로 밑의 if문을 통해 실제로 값이 반환되었을 때에만 함수가 실행되도록 한다.
        if self.filename:
            self.image = cv2.imread(self.filename)
            self.setPhoto(self.image)

    def setPhoto(self, image):
        self.tmp = image
        image = imutils.resize(image, width = 990)
        self.frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(self.frame, self.frame.shape[1], self.frame.shape[0], self.frame.strides[0], QImage.Format_RGB888)
        self.imageLable.setPixmap(QtGui.QPixmap.fromImage(image))


    def vinetImageBox(self):
        
        self.imageLable = QLabel(self)
        self.imageLable.setAlignment(Qt.AlignCenter)
        self.imageLable.setText("Vignetting Image Box")
        self.imageLable.setFont(QFont('Segoe UI', 18))
        self.imageLable.setGeometry(0, 0, 990, 750)
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

        self.vignetAnalyzeBtn = QPushButton('ANALYZE VIGNET', self)
        self.vignetAnalyzeBtn.setFont(QFont('Segoe UI', 12))
        self.vignetAnalyzeBtn.clicked.connect(self.vignetFunc)
        self.vignetAnalyzeBtn.setMaximumWidth(300)
        self.vignetAnalyzeBtn.setStyleSheet(
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
        self.contentFrame.setGeometry(0, 0, 1040, 800)
        
        self.contentVBox = QVBoxLayout(self.contentFrame)
        self.contentVBox.addWidget(self.imageLable)
        self.contentVBox.addWidget(self.fileOpenBtn, alignment=QtCore.Qt.AlignHCenter)
        self.contentVBox.addWidget(self.vignetAnalyzeBtn, alignment=QtCore.Qt.AlignHCenter)

    def vignetFunc(self):
        im = cv2.imread(self.filename)
        if self.filename :
            vignetting_correction(im)

class VinettingResMenu(QWidget):
    def __init__(self):
        super(VinettingResMenu, self).__init__()
        self.vinetResImageBox()


    def loadImage(self):
        self.filename = 'vignette_result.jpg'
        # getOpenself.filename은 취소를 눌렀을 때 빈 QString을 반환한다. 
        # 이때 이 QString은 거짓으로 간주되므로 밑의 if문을 통해 실제로 값이 반환되었을 때에만 함수가 실행되도록 한다.
        self.image = cv2.imread(self.filename)
        if not self.image is None:
            self.setPhoto(self.image)

    def setPhoto(self, image):
        self.tmp = image
        image = imutils.resize(image, width = 990)
        self.frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(self.frame, self.frame.shape[1], self.frame.shape[0], self.frame.strides[0], QImage.Format_RGB888)
        self.imageLable.setPixmap(QtGui.QPixmap.fromImage(image))


    def vinetResImageBox(self):
        
        self.imageLable = QLabel(self)
        self.imageLable.setAlignment(Qt.AlignCenter)
        self.imageLable.setText("Vignetting Image Box")
        self.imageLable.setFont(QFont('Segoe UI', 18))
        self.imageLable.setGeometry(0, 0, 990, 750)
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

        self.fileOpenBtn = QPushButton('LOAD IMAGE', self)
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

        self.vignetAnalyzeRes = QLabel('PASS / FAIL', self)
        self.vignetAnalyzeRes.setFont(QFont('Segoe UI', 12))
        self.vignetAnalyzeRes.setMaximumWidth(300)
        self.vignetAnalyzeRes.setMaximumHeight(40)
        self.vignetAnalyzeRes.setStyleSheet(
            """
            QLabel{
                background-color : rgba(20, 25, 30, 0.5); 
                color : white;
                margin-top : 5px;
                padding : 7px 20px;
                border : 0px;
                border-radius : 5px;
            }
            
            """
        )
        

        self.contentFrame = QFrame(self)
        self.contentFrame.setGeometry(0, 0, 1040, 800)
        
        self.contentVBox = QVBoxLayout(self.contentFrame)
        self.contentVBox.addWidget(self.imageLable)
        self.contentVBox.addWidget(self.fileOpenBtn, alignment=QtCore.Qt.AlignHCenter)
        self.contentVBox.addWidget(self.vignetAnalyzeRes, alignment=QtCore.Qt.AlignHCenter)

    def vignetFunc(self):
        im = cv2.imread(self.filename)
        if self.filename :
            vignetting_correction(im)


def check_monotonically_increase(parameter_tup):
    """a, b, c가 [0,1]에서 g(r)를 단조롭게 증가시킬 수 있는지 확인한다."""

    a, b, c = parameter_tup
    if c == 0:
        if a >= 0 and a + 2 * b >= 0 and not(a == 0 and b == 0):
            return True
        return False
    if c < 0:
        if b**2 > 3 * a * c:
            q_plus = (-2 * b + math.sqrt(4 * b**2 - 12 * a * c)) / (6 * c)
            q_minus = (-2 * b - math.sqrt(4 * b**2 - 12 * a * c)) / (6 * c)
            if q_plus <= 0 and q_minus >= 1:
                return True
        return False
    if c > 0:
        if b**2 < 3 * a * c:
            return True
        elif b**2 == 3 * a * c:
            if b >= 0 or 3 * c + b <= 0:
                return True
        else:
            q_plus = (-2 * b + math.sqrt(4 * b**2 - 12 * a * c)) / (6 * c)
            q_minus = (-2 * b - math.sqrt(4 * b**2 - 12 * a * c)) / (6 * c)
            if q_plus <= 0 or q_minus >= 1:
                return True
        return False


def calc_discrete_entropy(cm_x, cm_y, max_distance, parameter_tup, im):
    """
    주어진 파라미터의 게인 함수로 사진의 밝기를 조절한 후 이산 엔트로피를 계산한다.
    """

    print(parameter_tup)

    a, b, c = parameter_tup
    row, col = im.shape

    histogram = [0 for i in range(256)]

    for i in range(col):
        for j in range(row):

            # 현재 픽셀에서 사진의 질량 중심까지의 거리와 해당하는 r 값을 계산합니다.
            distance = math.sqrt((i - cm_x)**2 + (j - cm_y)**2)
            r = distance / max_distance

            # 게인 함수 평가 및 픽셀 밝기 값 조정
            g = 1 + a * r**2 + b * r**4 + c * r**6
            intensity = im[j, i] * g

            # 밝기 값을 해당 히스토그램 빈에 매핑합니다
            bin = 255 * math.log(1 + intensity) / math.log(256)
            floor_bin = math.floor(bin)
            ceil_bin = math.ceil(bin)

            # 조정 후 밝기 값이 255를 초과하는 경우, 상단 끝에 히스토그램 빈을 추가하기만 하면 됩니다.
            if bin > len(histogram) - 1:
                for k in range(len(histogram), ceil_bin + 1):
                    histogram.append(0)

            histogram[floor_bin] += 1 + floor_bin - bin
            histogram[ceil_bin] += ceil_bin - bin

    # Gausssian 커널을 사용하여 히스토그램 평활
    histogram = gaussian_filter1d(histogram, 4)

    histogram_sum = sum(histogram)
    H = 0

    # Calculate discrete entropy
    for i in range(len(histogram)):
        p = histogram[i] / histogram_sum
        if p != 0:
            H += p * math.log(p)

    return -H


def find_parameters(cm_x, cm_y, max_distance, im):
    """
    이미지의 질량 중심과 이미지의 가장 먼 꼭짓점에서 질량 중심까지의 거리를 고려할 때 이미지의 엔트로피를 최소화할 수 있는 a, b, c를 찾습니다.
    """

    a = b = c = 0
    delta = 2
    min_H = None

    # 실행시간 최소화하기 위해 탐색 세트 설정
    explored = set()

    while delta > 1 / 256:
        initial_tup = (a, b, c)

        for parameter_tup in [(a + delta, b, c), (a - delta, b, c),
                              (a, b + delta, c), (a, b - delta, c),
                              (a, b, c + delta), (a, b, c - delta)]:

            if parameter_tup not in explored:
                explored.add(parameter_tup)

                if check_monotonically_increase(parameter_tup):
                    curr_H = calc_discrete_entropy(
                        cm_x, cm_y, max_distance, parameter_tup, im)

                    # if the entropy is lower than current minimum, set parameters to current ones
                    if min_H is None or curr_H < min_H:
                        min_H = curr_H
                        a, b, c = parameter_tup

        # if the current parameters minimize the entropy with the current delta, reduce the delta
        if initial_tup == (a, b, c):
            delta /= 2

    return a, b, c


def vignetting_correction(im):
    """
    이산 엔트로피를 최소화할 수 있는 파라미터를 사용하여 영상의 vigneting을 수정합니다.
    """

    # RGB이미지를 grayscale로 변경
    imgray = cv2.transform(im, numpy.array([[0.2126, 0.7152, 0.0722]]))
    row, col = imgray.shape

    # 그림의 무게 중심 계산
    cm_x = sum(j * imgray[i, j] for i in range(row) for j in range(col)
               ) / sum(imgray[i, j] for i in range(row) for j in range(col))
    cm_y = sum(i * imgray[i, j] for i in range(row) for j in range(col)
               ) / sum(imgray[i, j] for i in range(row) for j in range(col))
    max_distance = math.sqrt(max(
        (vertex[0] - cm_x)**2 + (vertex[1] - cm_y)**2 for vertex in [[0, 0], [0, row], [col, 0], [col, row]]))

    # 이미지 크기가 너무 큰 경우 축소 이미지를 사용하여 파라미터를 가져오고 초기 이미지에 적용하여 실행 시간을 절약합니다.
    if col > 500:
        ratio = col / 500
        imgray_sm = cv2.resize(imgray, (500, round(row / ratio)))
        a, b, c = find_parameters(
            cm_x / ratio, cm_y / ratio, max_distance / ratio, imgray_sm)
    else:
        a, b, c = find_parameters(cm_x, cm_y, max_distance, imgray)

    # 원래 이미지 수정 및 비네팅 여부 판별
    judgment = 0
    for i in range(col):
        for j in range(row):
            distance = math.sqrt((i - cm_x)**2 + (j - cm_y)**2)
            r = distance / max_distance
            g = 1 + a * r**2 + b * r**4 + c * r**6
            if(g > 2): judgment += 1
            for k in range(3):
                modified = im[j, i][k] * g

                # 수정 후 밝기가 255보다 크면 255로 설정합니다.
                if modified > 255:
                    modified = 255
                im[j, i][k] = modified
    if(judgment >= 1):
        print("비네팅이 존재하여 수정 하여 저장하였습니다.")
        cv2.imwrite("vignette_result.jpg", im) #저장하기
    else :
        print("비네팅이 없습니다.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
