import sys, os
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# class ImageLabel(QLabel):
#     def __init__(self):
#         super().__init__()
#         self.setAlignment(Qt.AlignCenter)
#         self.setText("Drop Image Here")
#         self.setFont(QFont('Segoe UI', 18))
#         self.setGeometry(15, 65, 640, 640)
#         self.setStyleSheet(
#             """
#             QLabel{
#                 color : white;
#                 border : 3px;
#                 border-style: dashed;
#                 border-color: white;
#             }
#             """
#         )

#     def setPixmap(self, image):
#         super().setPixmap(image)
        
class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.titleBar()
        self.content()
        self.initUI()

    def mousePressEvent(self, event): 
        self.offset = event.pos() 
    
    def mouseMoveEvent(self, event): 
        x = event.globalX() 
        y = event.globalY() 
        x_w = self.offset.x() 
        y_w = self.offset.y() 
        self.move(x-x_w, y-y_w)

    def initUI(self):
        self.setWindowTitle('Camver')
        self.resize(1280, 720)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("""
                            background-color : rgb(40, 44, 52);
                            """)

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
        
        self.titleBox = QFrame(self)
        self.titleBox.setGeometry(0, 0, 1280, 50)
        self.titleBox.setStyleSheet(
            ''' 
            QWidget{ 
                background-color : rgb(33, 37, 43); }
            ''')
        
        self.titleHBox= QHBoxLayout(self.titleBox) 
        self.titleHBox.addWidget(self.favicon_label)
        self.titleHBox.addWidget(self.app_label)
        self.titleHBox.addStretch(1)
        self.titleHBox.addWidget(self.btn_min)
        self.titleHBox.addWidget(self.btn_max)
        self.titleHBox.addWidget(self.btn_close)

    def content(self):
        self.setAcceptDrops(True)
        self.imageLable = QLabel(self)
        self.imageLable.setAlignment(Qt.AlignCenter)
        self.imageLable.setText("Drop Image Here")
        self.imageLable.setFont(QFont('Segoe UI', 18))
        self.imageLable.setGeometry(15, 65, 640, 640)
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
        

        # self.contentBox = QFrame(self)
        # self.contentBox.setGeometry(0, 50, 1280, 670)
        # self.contentBox.setStyleSheet(
        #     ''' 
        #     QWidget{ 

        #     }
        #     ''')
        
        self.contentHBox = QHBoxLayout()
        self.contentHBox.addWidget(self.imageLable)
        #self.contentHBox.addStretch(1)

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def drogEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.set_image(file_path)

            event.accept()
        else:
            event.ignore()

    def set_image(self, file_path):
        self.imageLable.setPixmap(QPixmap(file_path))

    def btn_close_clicked(self):
        self.close()

    def btn_min_clicked(self):
        self.showMinimized()
           

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
