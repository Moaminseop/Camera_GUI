import cv2, imutils, re
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from camera_function import VignetFuncThread, ResFuncThread
from ui_function import Viewer, LoadingScreen


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

            resTest = ResFuncThread(self)
            resTest.testRes('./data/setimage.png', startlist, endlist, line, direction)


class ResMenu(QWidget):
    def __init__(self):
        super(ResMenu, self).__init__()
        self.imageBox()
        self.imageButton()

    def loadImage(self):
        self.image = cv2.imread('./data/resresult.png')
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


class EdgeMenu(QWidget):
    def __init__(self):
        super(EdgeMenu, self).__init__()
        self.imageBox()

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
        if self.filename :
            self.vi = VignetFuncThread()
            self.vi.vignetting_correction(self.filename)


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

