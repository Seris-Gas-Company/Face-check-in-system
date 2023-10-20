# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Teacher_Form.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Teacher_Form(object):
    def setupUi(self, Teacher_Form):
        Teacher_Form.setObjectName("Teacher_Form")
        Teacher_Form.resize(416, 275)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Teacher_Form.sizePolicy().hasHeightForWidth())
        Teacher_Form.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../icon/APP_icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Teacher_Form.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(Teacher_Form)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout.addWidget(self.pushButton_4)
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.verticalLayout.addWidget(self.pushButton_5)
        Teacher_Form.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Teacher_Form)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 416, 22))
        self.menubar.setObjectName("menubar")
        Teacher_Form.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Teacher_Form)
        self.statusbar.setObjectName("statusbar")
        Teacher_Form.setStatusBar(self.statusbar)

        self.retranslateUi(Teacher_Form)
        QtCore.QMetaObject.connectSlotsByName(Teacher_Form)

    def retranslateUi(self, Teacher_Form):
        _translate = QtCore.QCoreApplication.translate
        Teacher_Form.setWindowTitle(_translate("Teacher_Form", "人脸识别系统教师端"))
        self.label.setText(_translate("Teacher_Form", "欢迎使用人脸签到系统"))
        self.pushButton.setText(_translate("Teacher_Form", "实时签到"))
        self.pushButton_2.setText(_translate("Teacher_Form", "照片签到"))
        self.pushButton_3.setText(_translate("Teacher_Form", "点名签到"))
        self.pushButton_4.setText(_translate("Teacher_Form", "签到查询"))
        self.pushButton_5.setText(_translate("Teacher_Form", "退出"))
