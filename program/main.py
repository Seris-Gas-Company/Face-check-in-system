from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys
from myUI import Login_Form, Register_Form, Student_Form, Teacher_Form ,Stu_Inquiry_Form


# 登录界面
class My_Login_Form(QMainWindow, Login_Form.Ui_Login_Form):
    def __init__(self, parent=None):
        super(My_Login_Form, self).__init__(parent)
        self.setupUi(self)

    def login(self):
        if len(self.lineEdit.text()) == 5 and self.lineEdit.text() == self.lineEdit_2.text():
            print("jiaoshi")
            controller.show_teacher()
        elif len(self.lineEdit.text()) == 6 and self.lineEdit.text() == self.lineEdit_2.text():
            print("xuesheng")
            controller.show_student()
        elif self.lineEdit.text() == 'admin' and self.lineEdit_2.text() == '000000':
            print("admin")
        else:
            QMessageBox.information(self, "error!", "密码输入错误", QMessageBox.Ok)

    def register(self):
        controller.show_register()

    def refindPassword(self):
        QMessageBox.information(self, "error!", "请联系管理员18903200556", QMessageBox.Ok)


# 学生界面
class My_Student_Form(QMainWindow, Student_Form.Ui_Student_Form):
    def __init__(self, parent=None):
        super(My_Student_Form, self).__init__(parent)
        self.setupUi(self)

    def stu1(self):
        controller.show_stu_stu1()

    def stu2(self):
        pass

    def back(self):
        controller.show_student_login()

class My_Stu_Inquiry_Form(QMainWindow,Stu_Inquiry_Form.Ui_Stu_Inquiry_Form):
    def __init__(self,parent=None):
        super(My_Stu_Inquiry_Form,self).__init__(parent)
        self.setupUi(self)

    def back(self):
        controller.show_stu1_stu()

# 教师界面
class My_Teacher_Form(QMainWindow, Teacher_Form.Ui_Teacher_Form):
    def __init__(self, parent=None):
        super(My_Teacher_Form, self).__init__(parent)
        self.setupUi(self)


class My_Register_Form(QMainWindow, Register_Form.Ui_Register_Form):
    def __init__(self, parent=None):
        super(My_Register_Form, self).__init__(parent)
        self.setupUi(self)

    def register(self):
        print("zhuce")

    def back(self):
        print("back")
        controller.show_register_login()


# 界面跳转
class Controller:
    def __init__(self):
        self.login = My_Login_Form()
        self.student = My_Student_Form()
        self.teacher = My_Teacher_Form()
        self.register = My_Register_Form()
        self.stu_inquiry=My_Stu_Inquiry_Form()
        self.login.hide()
        self.student.hide()
        self.teacher.hide()
        self.stu_inquiry.hide()
        self.login.hide()
        self.register.hide()

    def show_main(self):
        self.login.show()

    def show_student(self):
        self.login.close()
        self.student.show()

    def show_teacher(self):
        self.login.close()
        self.teacher.show()

    def show_register(self):
        self.login.close()
        self.register.show()

    def show_register_login(self):
        self.login.show()
        self.register.close()

    def show_teacher_login(self):
        self.login.show()
        self.teacher.close()

    def show_student_login(self):
        self.login.show()
        self.student.close()

    def show_stu1_stu(self):
        self.student.show()
        self.stu_inquiry.close()

    def show_stu_stu1(self):
        self.stu_inquiry.show()
        self.student.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)  # 在 QApplication 方法中使用，创建应用程序对象
    controller = Controller()
    controller.show_main()
    sys.exit(app.exec_())  # 结束进程，退出程序
