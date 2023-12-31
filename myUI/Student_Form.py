# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Student_Form.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Student_Form(object):
    def setupUi(self, Student_Form):
        Student_Form.setObjectName("Student_Form")
        Student_Form.resize(381, 329)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Student_Form.sizePolicy().hasHeightForWidth())
        Student_Form.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../icon/APP_icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Student_Form.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(Student_Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)
        Student_Form.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Student_Form)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 381, 22))
        self.menubar.setObjectName("menubar")
        Student_Form.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Student_Form)
        self.statusbar.setObjectName("statusbar")
        Student_Form.setStatusBar(self.statusbar)

        self.retranslateUi(Student_Form)
        self.pushButton.clicked.connect(Student_Form.stu1) # type: ignore
        self.pushButton_2.clicked.connect(Student_Form.stu2) # type: ignore
        self.pushButton_3.clicked.connect(Student_Form.back) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Student_Form)

    def retranslateUi(self, Student_Form):
        _translate = QtCore.QCoreApplication.translate
        Student_Form.setWindowTitle(_translate("Student_Form", "人脸签到系统学生端"))
        self.label.setText(_translate("Student_Form", "欢迎使用人脸识别系统"))
        self.pushButton.setText(_translate("Student_Form", "签到查询"))
        self.pushButton_2.setText(_translate("Student_Form", "个人信息"))
        self.pushButton_3.setText(_translate("Student_Form", "退出"))
