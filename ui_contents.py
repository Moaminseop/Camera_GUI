import cv2, imutils, re
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from camera_function import EdgeFuncThread, VignetFuncThread, ResFuncThread

resFileName = None
edgeFileName = None
vignetFileName = None

imageRatio = None

startPoint = None
endPoint = None

class MainMenu(QWidget):
# mainContent의 이미지를 받아들이는 공간
    def __init__(self):
        super(MainMenu, self).__init__()
        self.resImageContent()
        self.edgeImageContent()
        self.vignetImageContent()
        self.resFileName = None
        self.edgeFileName = None
        self.vignetFileName = None
        self.imageSize = None


    def loadResImage(self):
        global resFileName 
        
        self.resFileName = QFileDialog.getOpenFileName(filter="Image (*.*) ")[0]
        # getOpenself.filename은 취소를 눌렀을 때 빈 QString을 반환한다. 
        # 이때 이 QString은 거짓으로 간주되므로 밑의 if문을 통해 실제로 값이 반환되었을 때에만 함수가 실행되도록 한다.
        if self.resFileName :
            resFileName = self.resFileName
            self.image = cv2.imread(self.resFileName)
            self.setResPhoto(self.image)


    def setResPhoto(self, image):
        global imageRatio
        width = 755
        self.tmp = image
        originImageSize = [int(image.shape[0]), int(image.shape[1])]
        imageRatio = originImageSize[1]/width
        image = imutils.resize(image, width)
        self.imageSize = image.shape
        print(self.imageSize)
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        self.view.setPixmap(QtGui.QPixmap.fromImage(image))
        self.view.getImageSize(self.imageSize)

    def resImageContent(self):
        self.view = Viewer()

        self.fileOpenBtn = QPushButton('SELECT IMAGE FOR RESOLUSTION', self)
        self.fileOpenBtn.setFont(QFont('Segoe UI', 12))
        self.fileOpenBtn.clicked.connect(self.loadResImage)
        self.fileOpenBtn.setMaximumWidth(350)
        self.fileOpenBtn.setStyleSheet(
            """
            QPushButton{
                background-color : rgba(20, 25, 30, 0.5); 
                color : white;
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
        self.contentVBox.addSpacing(10)

        # AlignHCenter를 통해 fileOpenBtn을 정렬
        self.contentVBox.addWidget(self.fileOpenBtn, alignment=QtCore.Qt.AlignHCenter)

    def loadEdgeImage(self):
        global edgeFileName 
        self.edgeFileName = QFileDialog.getOpenFileName(filter="Image (*.*) ")[0]
        # getOpenself.filename은 취소를 눌렀을 때 빈 QString을 반환한다. 
        # 이때 이 QString은 거짓으로 간주되므로 밑의 if문을 통해 실제로 값이 반환되었을 때에만 함수가 실행되도록 한다.
        if self.edgeFileName:
            edgeFileName = self.edgeFileName
            self.image = cv2.imread(self.edgeFileName)
            self.setEdgePhoto(self.image)


    def setEdgePhoto(self, image):
        self.tmp = image
        image = imutils.resize(image, width = 470)
        self.frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(self.frame, self.frame.shape[1], self.frame.shape[0], self.frame.strides[0], QImage.Format_RGB888)
        self.edgeImageLable.setPixmap(QtGui.QPixmap.fromImage(image)) 


    def edgeImageContent(self):
        self.edgeImageLable = QLabel(self)
        self.edgeImageLable.setAlignment(Qt.AlignCenter)
        self.edgeImageLable.setText("Edge Image Box")
        self.edgeImageLable.setFont(QFont('Segoe UI', 18))
        self.edgeImageLable.setGeometry(0, 0, 500, 400)
        self.edgeImageLable.setStyleSheet(
            """
            QLabel{
                color : white;
                border : 2px;
                border-style: dashed;
                border-color: white;
            }
            """
        )

        self.fileOpenEdgeBtn = QPushButton('SELECT IMAGE FOR EDGE', self)
        self.fileOpenEdgeBtn.setFont(QFont('Segoe UI', 12))
        self.fileOpenEdgeBtn.clicked.connect(self.loadEdgeImage)
        self.fileOpenEdgeBtn.setMaximumWidth(250)
        self.fileOpenEdgeBtn.setStyleSheet(
            """
            QPushButton{
                background-color : rgba(20, 25, 30, 0.5); 
                color : white;
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
        self.contentFrame.setGeometry(820, 0, 500, 400)
        
        self.contentVBox = QVBoxLayout(self.contentFrame)
        self.contentVBox.addWidget(self.edgeImageLable)
        self.contentVBox.addSpacing(3)
        self.contentVBox.addWidget(self.fileOpenEdgeBtn, alignment=QtCore.Qt.AlignHCenter)


    def loadVignetImage(self):
        global vignetFileName
        self.vignetFileName = QFileDialog.getOpenFileName(filter="Image (*.*) ")[0]
        # getOpenself.filename은 취소를 눌렀을 때 빈 QString을 반환한다. 
        # 이때 이 QString은 거짓으로 간주되므로 밑의 if문을 통해 실제로 값이 반환되었을 때에만 함수가 실행되도록 한다.
        if self.vignetFileName:
            vignetFileName = self.vignetFileName
            self.image = cv2.imread(self.vignetFileName)
            self.setVignetPhoto(self.image)


    def setVignetPhoto(self, image):
        self.tmp = image
        image = imutils.resize(image, width = 470)
        self.frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(self.frame, self.frame.shape[1], self.frame.shape[0], self.frame.strides[0], QImage.Format_RGB888)
        self.vignetImageLable.setPixmap(QtGui.QPixmap.fromImage(image)) 


    def vignetImageContent(self):
        self.vignetImageLable = QLabel(self)
        self.vignetImageLable.setAlignment(Qt.AlignCenter)
        self.vignetImageLable.setText("Vignetting Image Box")
        self.vignetImageLable.setFont(QFont('Segoe UI', 18))
        self.vignetImageLable.setGeometry(0, 0, 500, 400)
        self.vignetImageLable.setStyleSheet(
            """
            QLabel{
                color : white;
                border : 2px;
                border-style: dashed;
                border-color: white;
            }
            """
        )

        self.fileOpenResBtn = QPushButton('SELECT IMAGE FOR VIGNET', self)
        self.fileOpenResBtn.setFont(QFont('Segoe UI', 12))
        self.fileOpenResBtn.clicked.connect(self.loadVignetImage)
        self.fileOpenResBtn.setMaximumWidth(250)
        self.fileOpenResBtn.setStyleSheet(
            """
            QPushButton{
                background-color : rgba(20, 25, 30, 0.5); 
                color : white;
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
        self.contentFrame.setGeometry(820, 390, 500, 408)
        
        self.contentVBox = QVBoxLayout(self.contentFrame)
        self.contentVBox.addWidget(self.vignetImageLable)
        self.contentVBox.addSpacing(10)
        self.contentVBox.addWidget(self.fileOpenResBtn, alignment=QtCore.Qt.AlignHCenter)


class Viewer(QtWidgets.QGraphicsView): #뷰어의 역할을 해주는 것, 그래픽을 통해 좌표를 넘겨줌
    def __init__(self, parent=None):
        super().__init__(QtWidgets.QGraphicsScene(), parent)
        self.pixmap_item = self.scene().addPixmap(QtGui.QPixmap())
        self.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.rect_item = QGraphicsRectItem(QRectF(), self.pixmap_item)
        self.rect_item.setPen(QPen(QColor(0, 255, 0), 3, Qt.SolidLine))

        self.h = 0
        self.w = 0

        #이미지가 불려왔는지 체크하는 변수
        self.imageCheck = 0

    # 클래스 내부에서 외부 호출을 통해 이미지를 받는 함수
    def setPixmap(self, pixmap): 
        self.pixmap_item.setPixmap(pixmap)
        self.imageCheck = 1

    # 클래스 내부에서 외부 호출을 통해 이미지 크기를 받는 함수
    def getImageSize(self, imageSize):
        self.h = imageSize[0]
        self.w = imageSize[1]

    def mousePressEvent(self, event):
        self.pi = self.mapToScene(event.pos())
        super().mousePressEvent(event)
        # 이미지의 비율을 고려해 박스 시작 좌표를 넘겨준다.

    def mouseMoveEvent(self, event):
        pf = self.mapToScene(event.pos())
        if (self.pi - pf).manhattanLength() > QApplication.startDragDistance():
            self.pf = pf
            self.draw_rect()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        global startPoint, endPoint
        pf = self.mapToScene(event.pos())
        if (self.pi - pf).manhattanLength() > QApplication.startDragDistance():
            self.pf = pf
            self.draw_rect()
            # 이미지의 비율을 고려해 박스 끝 좌표를 넘겨준다.
            if self.imageCheck :
                startx = self.rect_item.rect().topLeft().x()
                starty = self.rect_item.rect().topLeft().y()

                endx = self.rect_item.rect().bottomRight().x()
                endy = self.rect_item.rect().bottomRight().y()

                startPoint = [[int(imageRatio * startx), int(imageRatio * starty)]]
                endPoint = [[int(imageRatio * endx), int(imageRatio * endy)]]

        super().mouseReleaseEvent(event)

    def draw_rect(self):

        Xais = self.pf.x()
        Yais = self.pf.y()

        if self.imageCheck :
            # 박스가 이미지 크기를 넘어가는 것을 막는 기능
            if int(self.pf.x()) <= 0:
                self.pf = QPointF(0, Yais)

            if int(self.pf.y()) <= 0:
                self.pf = QPointF(Xais, 0)

            if int(self.pf.x()) <= 0 and int(self.pf.y()) <= 0:
                self.pf = QPointF(0, 0)

            if int(self.pf.x()) >= self.w:
                self.pf = QPointF(self.w, Yais)

            if int(self.pf.y()) >= self.h:
                self.pf = QPointF(Xais, self.h)

            if int(self.pf.x()) >= self.w and int(self.pf.y()) >= self.h :
                self.pf = QPointF(self.w, self.h)

            if int(self.pf.y()) >= self.h and int(self.pf.x()) <= 0:
                self.pf = QPointF(0, self.h)

            if int(self.pf.x()) >= self.w and int(self.pf.y()) <= 0:
                self.pf = QPointF(self.w, 0)

            r = QRectF(self.pi, self.pf).normalized()
            r = self.rect_item.mapFromScene(r).boundingRect()
            self.rect_item.setRect(r)


class ResMenu(QWidget):
    def __init__(self):
        super(ResMenu, self).__init__()
        self.imageBox()
        self.interfaceContent()
        self.passFailChecker()

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
    
    def interfaceContent(self):
        self.analyzerLabel = QLabel(self)
        self.analyzerLabel.setText("ANALYZER")
        self.analyzerLabel.setFont(QFont('Segoe UI', 45))
        self.analyzerLabel.setStyleSheet(
            """
            QLabel{
                color : white;
            }
            """
        )

        self.resolutionLabel = QLabel('RES PARAMETER', self)
        self.resolutionLabel.setFont(QFont('Segoe UI', 25))
        self.resolutionLabel.setStyleSheet(
            """
            QLabel{
                width : 100px;
                height : 30px;
                color : white;
            }
            """
        )

        self.lineLabel = QLabel("Insert Line in Test Image")
        self.lineLabel.setFont(QFont('Segoe UI', 20))
        self.lineLabel.setStyleSheet(
            """
            QLabel{
                height : 20px;
                width: 80px;
                color : white;
            }
            """
        )

        self.lineText = QLineEdit(self)
        self.lineText.setFont(QFont('Segoe UI', 10))
        self.lineText.setStyleSheet(
            """
            QLineEdit{
                color : white;
            }
            """
        )

        self.directionLabel = QLabel("Select Test Direction")
        self.directionRadioBox1 = QRadioButton("Left -> Right Test") # 1
        self.directionRadioBox2 = QRadioButton("Right -> Left Test") # 2
        self.directionRadioBox3 = QRadioButton("Top-> Bottom Test") # 3
        self.directionRadioBox4 = QRadioButton("Bottom-> Top Test") # 4

        self.directionLabel.setFont(QFont('Segoe UI', 20))
        self.directionLabel.setStyleSheet(
            """
            QLabel{
                height : 20px;
                width: 80px;
                color : white;
            }
            """
        )

        self.directionRadioBox1.setFont(QFont('Segoe UI', 15))
        self.directionRadioBox1.setMaximumWidth(200)
        self.directionRadioBox1.setStyleSheet(
            """
            QRadioButton{
                color : white;
            }
            """
        )

        self.directionRadioBox2.setFont(QFont('Segoe UI', 15))
        self.directionRadioBox2.setMaximumWidth(200)
        self.directionRadioBox2.setStyleSheet(
            """
            QRadioButton{
                color : white;
            }
            """
        )

        self.directionRadioBox3.setFont(QFont('Segoe UI', 15))
        self.directionRadioBox3.setMaximumWidth(200)
        self.directionRadioBox3.setStyleSheet(
            """
            QRadioButton{
                color : white;
            }
            """
        )

        self.directionRadioBox4.setFont(QFont('Segoe UI', 15))
        self.directionRadioBox4.setMaximumWidth(200)
        self.directionRadioBox4.setStyleSheet(
            """
            QRadioButton{
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

        self.analyzBtn = QPushButton('ANALYZE', self)
        self.analyzBtn.setFont(QFont('Segoe UI', 12))
        self.analyzBtn.setMaximumWidth(150)
        self.analyzBtn.clicked.connect(self.analyzFunc)
        self.analyzBtn.setStyleSheet(
            """
            QPushButton{
                background-color : rgba(20, 25, 30, 0.5); 
                color : white;
                padding : 7px 20px;
                border : 0px;
                border-radius : 5px;
            }
            
            QPushButton::hover{ 
                background-color : rgba(20, 25, 30, 1); 
            }
            """
        )

        self.interfaceFrame = QFrame(self)
        self.interfaceFrame.setGeometry(870, 15, 400, 500)

        self.paramGrp = QGroupBox()
        self.paramGrpLayout = QVBoxLayout()
        self.paramGrpLayout.addWidget(self.lineLabel, alignment=QtCore.Qt.AlignHCenter)
        self.paramGrpLayout.addSpacing(-15)
        self.paramGrpLayout.addWidget(self.lineText, alignment=QtCore.Qt.AlignHCenter)
        self.paramGrpLayout.addSpacing(-5)
        self.paramGrpLayout.addWidget(self.directionLabel, alignment=QtCore.Qt.AlignHCenter)
        self.paramGrpLayout.addSpacing(-15)
        self.paramGrpLayout.addWidget(self.directionRadioBox3, alignment=QtCore.Qt.AlignHCenter)
        self.paramGrpLayout.addSpacing(-8)
        self.paramGrpLayout.addWidget(self.directionRadioBox4, alignment=QtCore.Qt.AlignHCenter)
        self.paramGrpLayout.addSpacing(-8)
        self.paramGrpLayout.addWidget(self.directionRadioBox1, alignment=QtCore.Qt.AlignHCenter)
        self.paramGrpLayout.addSpacing(-8)
        self.paramGrpLayout.addWidget(self.directionRadioBox2, alignment=QtCore.Qt.AlignHCenter)
        self.paramGrpLayout.addSpacing(10)
        self.paramGrpLayout.addWidget(self.analyzBtn, alignment=QtCore.Qt.AlignHCenter)
        self.paramGrp.setLayout(self.paramGrpLayout)

        self.interfaceContentVBox = QVBoxLayout(self.interfaceFrame)
        self.interfaceContentVBox.addWidget(self.analyzerLabel, alignment=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.interfaceContentVBox.addSpacing(-250)
        self.interfaceContentVBox.addWidget(self.resolutionLabel, alignment=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.interfaceContentVBox.addSpacing(-270)
        self.interfaceContentVBox.addWidget(self.paramGrp)

    def passFailChecker(self):
        self.pfCheckLabel = QLabel("PASS / FAIL CHECK")
        self.pfCheckLabel.setFont(QFont('Segoe UI', 25))
        self.pfCheckLabel.setStyleSheet(
            """
            QLabel{
                height : 20px;
                width: 80px;
                color : white;
            }
            """
        )

        self.passfailLabel = QLabel()
        self.passfailLabel.setFont(QFont('Segoe UI', 50))

        self.pfGrp = QGroupBox()
        self.pfGrpLayout = QVBoxLayout()
        self.pfGrpLayout.addWidget(self.passfailLabel, alignment=QtCore.Qt.AlignHCenter)
        self.pfGrp.setLayout(self.pfGrpLayout)

        self.interfaceFrame = QFrame(self)
        self.interfaceFrame.setGeometry(870, 510, 400, 250)
        self.interfaceContentVBox = QVBoxLayout(self.interfaceFrame)
        self.interfaceContentVBox.addWidget(self.pfCheckLabel, alignment=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.interfaceContentVBox.addSpacing(-100)
        self.interfaceContentVBox.addWidget(self.pfGrp)
        
    def analyzFunc(self):
        global pfDetect
        if resFileName:
            lineStr = self.lineText.text()
            direction = None
            line = []
            errorDetect = 1

            if self.directionRadioBox1.isChecked() :
                direction = [1]
            elif self.directionRadioBox2.isChecked() :
                direction = [2]
            elif self.directionRadioBox3.isChecked() :
                direction = [3]
            elif self.directionRadioBox4.isChecked() :
                direction = [4]

            try :
                line.append(int(lineStr))
            except :
                errorDetect = 0

            if startPoint and direction and errorDetect:
                resTest = ResFuncThread(self)
                img, pf = resTest.testRes(resFileName, startPoint, endPoint, line, direction)
                self.setPhoto(img)
                if pf == 0:
                    self.passfailLabel.setText("FAIL")
                    self.passfailLabel.setStyleSheet(
                        """
                        QLabel{
                            color : red;
                        }
                        """
                    )
                    print(pf)
                elif pf != 0:
                    self.passfailLabel.setText("PASS")
                    self.passfailLabel.setStyleSheet(
                        """
                        QLabel{
                            color : blue;
                        }
                        """
                    )
                    print(pf)


class EdgeMenu(QWidget):
    def __init__(self):
        super(EdgeMenu, self).__init__()
        self.imageBox()
        self.interfaceContent()
        self.passFailChecker()

    def setPhoto(self, image):
        self.tmp = image
        image = imutils.resize(image, width = 900)
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        self.imageLable.setPixmap(QtGui.QPixmap.fromImage(image))

    def imageBox(self):
        self.imageLable = QLabel(self)
        self.imageLable.setAlignment(Qt.AlignCenter)
        self.imageLable.setText("Edge Image")
        self.imageLable.setFont(QFont('Segoe UI', 18))
        self.imageLable.setGeometry(0, 0, 990, 780)
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
        self.contentFrame.setGeometry(0, 0, 950, 780)

        self.contentVBox = QVBoxLayout(self.contentFrame)
        self.contentVBox.addWidget(self.imageLable)

    def interfaceContent(self):
        self.resultBtn = QPushButton('ANALYZE \n EDGE ', self)
        self.resultBtn.setFont(QFont('Segoe UI', 40))
        self.resultBtn.setMaximumWidth(350)
        self.resultBtn.clicked.connect(self.resultFunc)
        self.resultBtn.setStyleSheet(
            """
            QPushButton{
                background-color : rgba(20, 25, 30, 0.5); 
                color : white;
                padding : 7px 20px;
                border : 0px;
                border-radius : 5px;
            }
            
            QPushButton::hover{ 
                background-color : rgba(20, 25, 30, 1); 
            }
            """
        )

        self.interfaceFrame = QFrame(self)
        self.interfaceFrame.setGeometry(1000, 15, 300, 400)

        self.interfaceContentVBox = QVBoxLayout(self.interfaceFrame)
        self.interfaceContentVBox.addWidget(self.resultBtn, alignment=QtCore.Qt.AlignHCenter)

    def passFailChecker(self):
        self.pfCheckLabel = QLabel("PASS / FAIL CHECK")
        self.pfCheckLabel.setFont(QFont('Segoe UI', 25))
        self.pfCheckLabel.setStyleSheet(
            """
            QLabel{
                height : 20px;
                width: 80px;
                color : white;
            }
            """
        )

        self.passfailLabel = QLabel()
        self.passfailLabel.setFont(QFont('Segoe UI', 50))

        self.pfGrp = QGroupBox()
        self.pfGrpLayout = QVBoxLayout()
        self.pfGrpLayout.addWidget(self.passfailLabel, alignment=QtCore.Qt.AlignHCenter)
        self.pfGrp.setLayout(self.pfGrpLayout)

        self.interfaceFrame = QFrame(self)
        self.interfaceFrame.setGeometry(1000, 400, 300, 300)
        self.interfaceContentVBox = QVBoxLayout(self.interfaceFrame)
        self.interfaceContentVBox.addWidget(self.pfCheckLabel, alignment=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.interfaceContentVBox.addSpacing(-150)
        self.interfaceContentVBox.addWidget(self.pfGrp)

    def resultFunc(self):
        if edgeFileName :
            eg = EdgeFuncThread(self)
            img, pf = eg.testRes(edgeFileName)
            self.setPhoto(img)
            if pf == 0:
                self.passfailLabel.setText("FAIL")
                self.passfailLabel.setStyleSheet(
                    """
                    QLabel{
                        color : red;
                    }
                    """
                )
                        
            elif pf == 1:
                self.passfailLabel.setText("PASS")
                self.passfailLabel.setStyleSheet(
                    """
                    QLabel{
                        color : blue;
                    }
                    """
                )



class VinettingMenu(QWidget):
    def __init__(self):
        super(VinettingMenu, self).__init__()
        self.vinetImageBox()
        self.interfaceContent()
        self.passFailChecker()

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
        self.imageLable.setText("Vignetting Image")
        self.imageLable.setFont(QFont('Segoe UI', 18))
        self.imageLable.setGeometry(0, 0, 990, 780)
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
        self.contentFrame.setGeometry(0, 0, 950, 780)

        self.contentVBox = QVBoxLayout(self.contentFrame)
        self.contentVBox.addWidget(self.imageLable)

    def interfaceContent(self):
        self.resultBtn = QPushButton('ANALYZE \n VIGNET ', self)
        self.resultBtn.setFont(QFont('Segoe UI', 40))
        self.resultBtn.setMaximumWidth(350)
        self.resultBtn.clicked.connect(self.vignetFunc)
        self.resultBtn.setStyleSheet(
            """
            QPushButton{
                background-color : rgba(20, 25, 30, 0.5); 
                color : white;
                padding : 7px 20px;
                border : 0px;
                border-radius : 5px;
            }
            
            QPushButton::hover{ 
                background-color : rgba(20, 25, 30, 1); 
            }
            """
        )

        self.interfaceFrame = QFrame(self)
        self.interfaceFrame.setGeometry(1000, 15, 300, 400)

        self.interfaceContentVBox = QVBoxLayout(self.interfaceFrame)
        self.interfaceContentVBox.addWidget(self.resultBtn, alignment=QtCore.Qt.AlignHCenter)

    def passFailChecker(self):
        self.pfCheckLabel = QLabel("PASS / FAIL CHECK")
        self.pfCheckLabel.setFont(QFont('Segoe UI', 25))
        self.pfCheckLabel.setStyleSheet(
            """
            QLabel{
                height : 20px;
                width: 80px;
                color : white;
            }
            """
        )

        self.passfailLabel = QLabel()
        self.passfailLabel.setFont(QFont('Segoe UI', 50))

        self.pfGrp = QGroupBox()
        self.pfGrpLayout = QVBoxLayout()
        self.pfGrpLayout.addWidget(self.passfailLabel, alignment=QtCore.Qt.AlignHCenter)
        self.pfGrp.setLayout(self.pfGrpLayout)

        self.interfaceFrame = QFrame(self)
        self.interfaceFrame.setGeometry(1000, 400, 300, 300)
        self.interfaceContentVBox = QVBoxLayout(self.interfaceFrame)
        self.interfaceContentVBox.addWidget(self.pfCheckLabel, alignment=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.interfaceContentVBox.addSpacing(-150)
        self.interfaceContentVBox.addWidget(self.pfGrp)


    def vignetFunc(self):
        if vignetFileName :
            vi = VignetFuncThread()
            img, pf = vi.vignetting_correction(vignetFileName)
            self.setPhoto(img)
            if pf == 0:
                self.passfailLabel.setText("FAIL")
                self.passfailLabel.setStyleSheet(
                    """
                    QLabel{
                        color : red;
                    }
                    """
                )
                        
            elif pf == 1:
                self.passfailLabel.setText("PASS")
                self.passfailLabel.setStyleSheet(
                    """
                    QLabel{
                        color : blue;
                    }
                    """
                )


class VinettingResMenu(QWidget):
    def __init__(self):
        super(VinettingResMenu, self).__init__()
        self.vinetResImageBox()


    def loadImage(self):
        self.filename = './data/vignette_result.jpg'
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

