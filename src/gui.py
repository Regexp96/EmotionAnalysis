from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QApplication, QDialog
from PyQt5.QtGui import QPixmap
from PySide2.QtCore import Signal, QObject, QEvent

import src.main


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("감성단어분석기")
        Form.resize(789, 503)
        self.img = QPixmap()
        # self.img.scaled(321, 211, QtCore.Qt.KeepAspectRatio)

        self.graphicsView_5 = QtWidgets.QLabel(Form)
        self.graphicsView_5.setGeometry(QtCore.QRect(270, 230, 241, 181))
        self.graphicsView_5.setObjectName("graphicsView_5")
        self.graphicsView_5.setPixmap(self.img)

        self.graphicsView_4 = QtWidgets.QLabel(Form)
        self.graphicsView_4.setGeometry(QtCore.QRect(530, 230, 241, 181))
        self.graphicsView_4.setObjectName("graphicsView_4")
        self.graphicsView_4.setPixmap(self.img)

        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(620, 430, 151, 23))
        self.pushButton.setText("경로를 선택하십시오")
        self.pushButton.setShortcut("")
        self.pushButton.setObjectName("pushButton")

        self.buttonBox = QtWidgets.QDialogButtonBox(Form)
        self.buttonBox.setGeometry(QtCore.QRect(360, 460, 411, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.main_graphics = QtWidgets.QLabel(Form)
        self.main_graphics.setGeometry(QtCore.QRect(240, 10, 321, 211))
        self.main_graphics.setObjectName("graphicsView")
        self.main_graphics.setPixmap(self.img)

        self.graphicsView_6 = QtWidgets.QLabel(Form)
        self.graphicsView_6.setGeometry(QtCore.QRect(10, 230, 241, 181))
        self.graphicsView_6.setObjectName("graphicsView_6")
        self.graphicsView_6.setPixmap(self.img)

        self.lineEdit = QtWidgets.QLabel(Form)
        self.lineEdit.setGeometry(QtCore.QRect(260, 430, 341, 20))
        self.lineEdit.setObjectName("lineEdit")

        self.pushButton.clicked.connect(self.pushButtonClicked)
        self.buttonBox.accepted.connect(self.accept)
        # self.clickable(self.main_graphics).connect(self.img_clicked)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))


    def accept(self):
        fname = self.lineEdit.text()
        #src.main.run(fname)
        print("끝")
        self.img.load('output/emotionmodel.png')
        self.main_graphics.setPixmap(self.img.scaled(321, 211))

        self.img.load('output/wordcloud.png')
        self.graphicsView_4.setPixmap(self.img.scaled(241, 181))

        self.img.load('output/pie_chart.png')
        self.graphicsView_5.setPixmap(self.img.scaled(241, 181))

        self.img.load('output/radar_chart.png')
        self.graphicsView_6.setPixmap(self.img.scaled(241, 181))

        print("aaa")

    def img_clicked(self):
        print('s')

    def pushButtonClicked(self):
        fname = QFileDialog.getOpenFileName()
        self.lineEdit.setText(fname[0])

    # def clickable(self, widget):
    #     global FILE_LIST
    #
    #     class Filter(QObject):
    #         clicked = Signal()
    #
    #         def eventFilter(self, obj, event):
    #             if obj == widget:
    #                 if event.type() == QEvent.MouseButtonRelease:
    #                     if obj.rect().contains(event.pos()):
    #                         self.clicked.emit()
    #                         # The developer can opt for .emit(obj) to get the object within the slot.
    #                         return True
    #
    #             return False
    #
    #     filter = Filter(widget)
    #     widget.installEventFilter(filter)
    #     return filter.clicked

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
