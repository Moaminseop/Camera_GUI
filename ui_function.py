import sys
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *



class ui_functions(QWidget):
    def btn_close_clicked(self):
        self.close()

    def btn_min_clicked(self):
        self.showMinimized()

    def btn_restore_clicked(self):
        if self.btn_max.isChecked() == 1:
            self.showMaximized()
            self.btn_max.setIcon(QIcon('./image/icon/icon_restore.png'))
            self.size = 0
            print("max")

        else:
            self.showNormal()
            self.btn_max.setIcon(QIcon('./image/icon/icon_max.png'))
            self.size = 1
            print("min")