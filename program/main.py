import datetime

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QAbstractItemView, QTableWidgetItem
import sys
from myUI import Login_Form, Register_Form, Student_Form, Teacher_Form, Stu_Inquiry_Form, Stu_Info_Form
from myUI import Tch_Info_Form, Checkin_Form ,Checkin_text, Tch_stu_form
import pymysql

# 登录账号
static_login_user = 0
now_ctid=0

# 登录界面
class My_Login_Form(QMainWindow, Login_Form.Ui_Login_Form):
    def __init__(self, parent=None):
        super(My_Login_Form, self).__init__(parent)
        self.setupUi(self)

    def login(self):
        global static_login_user
        conn = pymysql.connect(
            host='localhost',  # 主机名（或IP地址）
            port=3306,  # 端口号，默认为3306
            user='root',  # 用户名
            password='123852',  # 密码
            charset='utf8mb4'  # 设置字符编码
        )
        conn.select_db("checkin")
        user=self.lineEdit.text()
        userpass=self.lineEdit_2.text()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE uname=%s", user)
        results = cursor.fetchall()
        if len(results)!=0:
            if results[0][1]==user and results[0][2]==userpass:
                static_login_user = user
                if results[0][4]==1:
                    self.close()
                    self.new_window = My_Teacher_Form()
                    self.new_window.show()
                else :
                    self.close()
                    self.new_window = My_Student_Form()
                    self.new_window.show()
            else:
                QMessageBox.information(self, "error!", "用户名或密码错误", QMessageBox.Ok)
        else:
            QMessageBox.information(self, "error!", "用户名或密码错误", QMessageBox.Ok)
        cursor.close()
        conn.close()

    def register(self):
        self.new_window = My_Register_Form()
        self.new_window.show()
        self.close()

    def refindPassword(self):
        QMessageBox.information(self, "error!", "请联系管理员18903200556", QMessageBox.Ok)


# 学生界面
class My_Student_Form(QMainWindow, Student_Form.Ui_Student_Form):
    def __init__(self, parent=None):
        super(My_Student_Form, self).__init__(parent)
        self.setupUi(self)

    def stu1(self):
        self.close()
        self.new_window = My_Stu_Inquiry_Form()
        self.new_window.show()

    def stu2(self):
        self.close()
        self.new_window = My_Stu_Info_Form()
        self.new_window.show()

    def back(self):
        self.close()
        self.new_window = My_Login_Form()
        self.new_window.show()


# 学生查询界面
class My_Stu_Inquiry_Form(QMainWindow, Stu_Inquiry_Form.Ui_Stu_Inquiry_Form):
    def __init__(self, parent=None):
        super(My_Stu_Inquiry_Form, self).__init__(parent)
        self.setupUi(self)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        conn = pymysql.connect(
            host='localhost',  # 主机名（或IP地址）
            port=3306,  # 端口号，默认为3306
            user='root',  # 用户名
            password='123852',  # 密码
            charset='utf8mb4'  # 设置字符编码
        )
        conn.select_db("checkin")
        cursor = conn.cursor()
        cursor.execute("SELECT sid FROM student WHERE uname=%s", static_login_user)
        sid = cursor.fetchall()
        cursor.execute("SELECT * FROM student WHERE uname=%s", static_login_user)
        stu = cursor.fetchall()
        cursor.execute("SELECT * FROM stucheckin WHERE sid=%s", sid[0][0])
        results=cursor.fetchall()
        row_count=0
        print(stu)
        print(results)
        for result in results:
            self.tableWidget.insertRow(row_count)
            self.tableWidget.setItem(0, 0, QTableWidgetItem(result[1]))
            if result[3]==1:
                self.tableWidget.setItem(0, 1, QTableWidgetItem("签到"))
            elif result[3]==2:
                self.tableWidget.setItem(0, 1, QTableWidgetItem("请假"))
            elif result[3]==3:
                self.tableWidget.setItem(0, 1, QTableWidgetItem("迟到"))
            elif result[3]==4:
                self.tableWidget.setItem(0, 1, QTableWidgetItem("早退"))
            elif result[3]==5:
                self.tableWidget.setItem(0, 1, QTableWidgetItem("旷课"))
            else :
                self.tableWidget.setItem(0, 1, QTableWidgetItem("没点名"))
            self.tableWidget.setItem(0, 2, QTableWidgetItem(stu[0][1]))
            self.tableWidget.setItem(0, 3, QTableWidgetItem(stu[0][2]))
            self.tableWidget.setItem(0, 4, QTableWidgetItem(result[5]))
            row_count+=1

    def select(self):
        print("select")

    def back(self):
        self.close()
        self.new_window = My_Student_Form()
        self.new_window.show()


# 学生个人信息界面
class My_Stu_Info_Form(QMainWindow, Stu_Info_Form.Ui_Stu_Info_Form):
    def __init__(self, parent=None):
        super(My_Stu_Info_Form, self).__init__(parent)
        self.setupUi(self)
        conn = pymysql.connect(
            host='localhost',  # 主机名（或IP地址）
            port=3306,  # 端口号，默认为3306
            user='root',  # 用户名
            password='123852',  # 密码
            charset='utf8mb4'  # 设置字符编码
        )
        conn.select_db("checkin")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM student WHERE uname=%s", static_login_user)
        results = cursor.fetchall()
        print(results)
        self.lineEdit.setText(results[0][2])
        self.lineEdit_2.setText(results[0][1])
        if results[0][5]==1:
            self.lineEdit_4.setText("男")
        else :
            self.lineEdit_4.setText("女")
        cursor.execute("SELECT * FROM user WHERE uname=%s", static_login_user)
        results = cursor.fetchall()
        print(results)
        self.lineEdit_3.setText(results[0][3])
        cursor.close()
        conn.close()
    def back(self):
        self.close()
        self.new_window = My_Student_Form()
        self.new_window.show()
    def save(self):
        flag=1
        conn = pymysql.connect(
            host='localhost',  # 主机名（或IP地址）
            port=3306,  # 端口号，默认为3306
            user='root',  # 用户名
            password='123852',  # 密码
            charset='utf8mb4'  # 设置字符编码
        )
        conn.select_db("checkin")
        cursor = conn.cursor()
        print(static_login_user)
        sex=self.lineEdit_4.text()
        pass1=self.lineEdit_5.text()
        pass2=self.lineEdit_6.text()
        if sex=="女":
            cursor.execute("UPDATE student SET ssex=0 WHERE uname=%s", static_login_user)
            conn.commit()
        elif sex=="男":
            cursor.execute("UPDATE student SET ssex=1 WHERE uname=%s", static_login_user)
            conn.commit()
        else :
            QMessageBox.information(self, "error!", "性别请输入男或女", QMessageBox.Ok)
            flag=0
        if len(pass1)>0 or len(pass2)>0 :
            if len(pass1)<6 or len(pass1)>16:
                QMessageBox.information(self, "error!", "密码为6-16位", QMessageBox.Ok)
                flag = 0
            elif pass1 != pass2:
                QMessageBox.information(self, "error!", "两次密码不一致", QMessageBox.Ok)
                flag = 0
            else:
                value=(pass1,static_login_user)
                cursor.execute("UPDATE user SET upass=%s WHERE uname=%s",value)
                conn.commit()
        if flag==1:
            QMessageBox.information(self, "修改成功", "修改成功", QMessageBox.Ok)
        cursor.close()
        conn.close()
        print("save")


# 教师界面
class My_Teacher_Form(QMainWindow, Teacher_Form.Ui_Teacher_Form):
    def __init__(self, parent=None):
        super(My_Teacher_Form, self).__init__(parent)
        self.setupUi(self)

    def teacher1(self):
        pass

    def teacher2(self):
        pass

    def teacher3(self):
        self.new_window = My_Tch_stu_form()
        self.new_window.show()
        self.close()

    def teacher4(self):
        self.new_window = My_Tch_Checkin_Form()
        self.new_window.show()
        self.close()

    def teacher5(self):
        self.new_window = My_Tch_Info_Form()
        self.new_window.show()
        self.close()

    def back(self):
        self.new_window = My_Login_Form()
        self.new_window.show()
        self.close()


# 教师信息
class My_Tch_Info_Form(QMainWindow, Tch_Info_Form.Ui_Tch_Info_Form):
    def __init__(self, parent=None):
        super(My_Tch_Info_Form, self).__init__(parent)
        self.setupUi(self)
        conn = pymysql.connect(
            host='localhost',  # 主机名（或IP地址）
            port=3306,  # 端口号，默认为3306
            user='root',  # 用户名
            password='123852',  # 密码
            charset='utf8mb4'  # 设置字符编码
        )
        conn.select_db("checkin")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM teacher WHERE uname=%s", static_login_user)
        results = cursor.fetchall()
        print(results)
        self.lineEdit.setText(results[0][2])
        self.lineEdit_2.setText(results[0][1])
        if results[0][3] == 1:
            self.lineEdit_4.setText("男")
        else:
            self.lineEdit_4.setText("女")
        cursor.execute("SELECT * FROM user WHERE uname=%s", static_login_user)
        results = cursor.fetchall()
        print(results)
        self.lineEdit_3.setText(results[0][3])
        cursor.close()
        conn.close()

    def save(self):
        flag = 1
        conn = pymysql.connect(
            host='localhost',  # 主机名（或IP地址）
            port=3306,  # 端口号，默认为3306
            user='root',  # 用户名
            password='123852',  # 密码
            charset='utf8mb4'  # 设置字符编码
        )
        conn.select_db("checkin")
        cursor = conn.cursor()
        print(static_login_user)
        sex = self.lineEdit_4.text()
        pass1 = self.lineEdit_5.text()
        pass2 = self.lineEdit_6.text()
        if sex == "女":
            cursor.execute("UPDATE teacher SET tsex=0 WHERE uname=%s", static_login_user)
            conn.commit()
        elif sex == "男":
            cursor.execute("UPDATE teacher SET tsex=1 WHERE uname=%s", static_login_user)
            conn.commit()
        else:
            QMessageBox.information(self, "error!", "性别请输入男或女", QMessageBox.Ok)
            flag = 0
        if len(pass1) > 0 or len(pass2) > 0:
            if len(pass1) < 6 or len(pass1) > 16:
                QMessageBox.information(self, "error!", "密码为6-16位", QMessageBox.Ok)
                flag = 0
            elif pass1 != pass2:
                QMessageBox.information(self, "error!", "两次密码不一致", QMessageBox.Ok)
                flag = 0
            else:
                value = (pass1, static_login_user)
                cursor.execute("UPDATE user SET upass=%s WHERE uname=%s", value)
                conn.commit()
        if flag == 1:
            QMessageBox.information(self, "修改成功", "修改成功", QMessageBox.Ok)
        cursor.close()
        conn.close()
        print("save")

    def back(self):
        self.new_window = My_Teacher_Form()
        self.new_window.show()
        self.close()

# 教师查询
class My_Tch_Checkin_Form(QMainWindow, Checkin_Form.Ui_Checkin_Form):
    def __init__(self, parent=None):
        super(My_Tch_Checkin_Form, self).__init__(parent)
        self.setupUi(self)
        self.dateEdit.setDate(datetime.date(1752,9,14))
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        conn = pymysql.connect(
            host='localhost',  # 主机名（或IP地址）
            port=3306,  # 端口号，默认为3306
            user='root',  # 用户名
            password='123852',  # 密码
            charset='utf8mb4'  # 设置字符编码
        )
        conn.select_db("checkin")
        cursor = conn.cursor()
        cursor.execute("SELECT tid FROM teacher WHERE uname=%s", static_login_user)
        tid = cursor.fetchall()
        cursor.execute("SELECT * FROM stucheckin WHERE tid=%s", tid[0][0])
        results = cursor.fetchall()
        row_count = 0
        print(results)
        for result in results:
            self.tableWidget.insertRow(row_count)
            cursor.execute("SELECT uname,sname FROM student WHERE sid=%s", result[2])
            stu=cursor.fetchall()
            self.tableWidget.setItem(row_count, 0, QTableWidgetItem(result[1]))
            self.tableWidget.setItem(row_count, 1, QTableWidgetItem(result[5]))
            self.tableWidget.setItem(row_count, 2, QTableWidgetItem(stu[0][1]))
            self.tableWidget.setItem(row_count, 3, QTableWidgetItem(stu[0][0]))
            if result[3] == 1:
                self.tableWidget.setItem(row_count, 4, QTableWidgetItem("签到"))
            elif result[3] == 2:
                self.tableWidget.setItem(row_count, 4, QTableWidgetItem("请假"))
            elif result[3] == 3:
                self.tableWidget.setItem(row_count, 4, QTableWidgetItem("迟到"))
            elif result[3] == 4:
                self.tableWidget.setItem(row_count, 4, QTableWidgetItem("早退"))
            elif result[3] == 5:
                self.tableWidget.setItem(row_count, 4, QTableWidgetItem("旷课"))
            else:
                self.tableWidget.setItem(row_count, 4, QTableWidgetItem("没点名"))
            self.tableWidget.setItem(row_count, 5, QTableWidgetItem(str(result[0])))
            row_count += 1
        cursor.close()
        conn.close()

    def refresh(self):
        self.tableWidget.setRowCount(0)
        conn = pymysql.connect(
            host='localhost',  # 主机名（或IP地址）
            port=3306,  # 端口号，默认为3306
            user='root',  # 用户名
            password='123852',  # 密码
            charset='utf8mb4'  # 设置字符编码
        )
        conn.select_db("checkin")
        cursor = conn.cursor()
        cursor.execute("SELECT tid FROM teacher WHERE uname=%s", static_login_user)
        tid = cursor.fetchall()
        cursor.execute("SELECT * FROM stucheckin WHERE tid=%s", tid[0][0])
        results = cursor.fetchall()
        row_count = 0
        print(results)
        for result in results:
            self.tableWidget.insertRow(row_count)
            cursor.execute("SELECT uname,sname FROM student WHERE sid=%s", result[2])
            stu = cursor.fetchall()
            self.tableWidget.setItem(row_count, 0, QTableWidgetItem(result[1]))
            self.tableWidget.setItem(row_count, 1, QTableWidgetItem(result[5]))
            self.tableWidget.setItem(row_count, 2, QTableWidgetItem(stu[0][1]))
            self.tableWidget.setItem(row_count, 3, QTableWidgetItem(stu[0][0]))
            if result[3] == 1:
                self.tableWidget.setItem(row_count, 4, QTableWidgetItem("签到"))
            elif result[3] == 2:
                self.tableWidget.setItem(row_count, 4, QTableWidgetItem("请假"))
            elif result[3] == 3:
                self.tableWidget.setItem(row_count, 4, QTableWidgetItem("迟到"))
            elif result[3] == 4:
                self.tableWidget.setItem(row_count, 4, QTableWidgetItem("早退"))
            elif result[3] == 5:
                self.tableWidget.setItem(row_count, 4, QTableWidgetItem("旷课"))
            else:
                self.tableWidget.setItem(row_count, 4, QTableWidgetItem("没点名"))
            self.tableWidget.setItem(row_count, 5, QTableWidgetItem(str(result[0])))
            row_count += 1
        cursor.close()
        conn.close()

    def search(self):
        self.tableWidget.setRowCount(0)
        conn = pymysql.connect(
            host='localhost',  # 主机名（或IP地址）
            port=3306,  # 端口号，默认为3306
            user='root',  # 用户名
            password='123852',  # 密码
            charset='utf8mb4'  # 设置字符编码
        )
        conn.select_db("checkin")
        cursor = conn.cursor()
        cursor.execute("SELECT tid FROM teacher WHERE uname=%s", static_login_user)
        tid=cursor.fetchall()[0][0]
        state = self.lineEdit_3.text()
        flag1 = -1
        stu_id = self.lineEdit_2.text()
        flag2 = 0
        class_name = self.lineEdit_4.text()
        flag3 = 0
        time = self.dateEdit.text()
        flag4 = 0
        if state=="签到":
            flag1=1
        elif state=="请假":
            flag1=2
        elif state=="迟到":
            flag1=3
        elif state=="早退":
            flag1=4
        elif state=="旷课":
            flag1=5
        elif state=="没点名":
            flag1=5
        elif len(state)==0:
            flag1=-1
        else:
            QMessageBox.information(self, "查找失败", "签到状态输入错误，应为签到、请假、迟到、旷课", QMessageBox.Ok)
        cursor.execute("SELECT * FROM student WHERE uname=%s", stu_id)
        stu = cursor.fetchall()
        if len(stu)!=0:
            flag2=1
        if len(class_name)!=0:
            flag3=1
        if time!="1752/9/14":
            flag4=1
        sql="SELECT * FROM stucheckin WHERE "
        count=0
        if flag1 > -1:
            count+=1
            sql=sql+"ctstate="+str(flag1)
        if flag2!=0:
            if count>0:
                sql=sql+" AND "
            count+=1
            sql=sql+"sid="+str(stu[0][0])
        if flag3!=0 :
            if count>0:
                sql=sql+" AND "
            count+=1
            sql=sql+"ctname like \'%"+class_name+"%\'"
        if flag4!=0:
            if count>0:
                sql=sql+" AND "
            count+=1
            sql=sql+"cttime like \'%"+time+"%\'"
        if count>0:
            sql = sql + " AND "
            sql=sql+"tid="+str(tid)
            print(sql)
            cursor.execute(sql)
            results = cursor.fetchall()
            row_count = 0
            print(results)
            for result in results:
                self.tableWidget.insertRow(row_count)
                cursor.execute("SELECT uname,sname FROM student WHERE sid=%s", result[2])
                stu = cursor.fetchall()
                self.tableWidget.setItem(row_count, 0, QTableWidgetItem(result[1]))
                self.tableWidget.setItem(row_count, 1, QTableWidgetItem(result[5]))
                self.tableWidget.setItem(row_count, 2, QTableWidgetItem(stu[0][1]))
                self.tableWidget.setItem(row_count, 3, QTableWidgetItem(stu[0][0]))
                if result[3] == 1:
                    self.tableWidget.setItem(row_count, 4, QTableWidgetItem("签到"))
                elif result[3] == 2:
                    self.tableWidget.setItem(row_count, 4, QTableWidgetItem("请假"))
                elif result[3] == 3:
                    self.tableWidget.setItem(row_count, 4, QTableWidgetItem("迟到"))
                elif result[3] == 4:
                    self.tableWidget.setItem(row_count, 4, QTableWidgetItem("早退"))
                elif result[3] == 5:
                    self.tableWidget.setItem(row_count, 4, QTableWidgetItem("旷课"))
                else:
                    self.tableWidget.setItem(row_count, 4, QTableWidgetItem("没点名"))
                self.tableWidget.setItem(row_count, 5, QTableWidgetItem(str(result[0])))
                row_count += 1
        cursor.close()
        conn.close()
        print("search")

    def back(self):
        self.new_window = My_Teacher_Form()
        self.new_window.show()
        self.close()

    def xiugai(self):
        print("xiugai")
        global now_ctid
        for i in self.tableWidget.selectedItems():
            now_ctid=self.tableWidget.item(i.row(),5).text()
            break
        print(now_ctid)
        self.new_window = My_Checkin_text()
        self.new_window.show()
        self.close()

# 签到修改界面
class My_Checkin_text(QMainWindow, Checkin_text.Ui_Checkin_text):
    def __init__(self, parent=None):
        super(My_Checkin_text, self).__init__(parent)
        self.setupUi(self)
        conn = pymysql.connect(
            host='localhost',  # 主机名（或IP地址）
            port=3306,  # 端口号，默认为3306
            user='root',  # 用户名
            password='123852',  # 密码
            charset='utf8mb4'  # 设置字符编码
        )
        conn.select_db("checkin")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM stucheckin WHERE ctid=%s", now_ctid)
        results = cursor.fetchall()
        cursor.execute("SELECT uname FROM student WHERE sid=%s", results[0][2])
        stu = cursor.fetchall()
        print(results)
        for result in results:
            self.lineEdit.setText(result[1])
            self.lineEdit_2.setText(stu[0][0])
            self.dateTimeEdit.setDateTime(datetime.datetime.strptime(result[5],"%Y/%m/%d %H:%M"))
            if result[3] == 1:
                self.radioButton.click()
            elif result[3] == 2:
                self.radioButton_2.click()
            elif result[3] == 3:
                self.radioButton_3.click()
            elif result[3] == 4:
                self.radioButton_4.click()
            elif result[3] == 5:
                self.radioButton_5.click()
            else:
                pass
        cursor.close()
        conn.close()

    def save(self):
        print("save")
        conn = pymysql.connect(
            host='localhost',  # 主机名（或IP地址）
            port=3306,  # 端口号，默认为3306
            user='root',  # 用户名
            password='123852',  # 密码
            charset='utf8mb4'  # 设置字符编码
        )
        conn.select_db("checkin")
        cursor = conn.cursor()
        class_name = self.lineEdit.text()
        stu_id = self.lineEdit_2.text()
        time = self.dateTimeEdit.text()
        flag = 0
        if self.radioButton.isChecked():
            flag=1
        elif self.radioButton_2.isChecked():
            flag=2
        elif self.radioButton_3.isChecked():
            flag=3
        elif self.radioButton_4.isChecked():
            flag=4
        elif self.radioButton_5.isChecked():
            flag=5
        cursor.execute("SELECT * FROM student WHERE uname=%s",stu_id)
        stu=cursor.fetchall()
        if len(stu_id)==0:
            QMessageBox.information(self, "修改失败", "学生学号不能为空", QMessageBox.Ok)
        elif len(stu)==0:
            QMessageBox.information(self, "修改失败", "找不到该学生", QMessageBox.Ok)
        elif len(class_name)==0:
            QMessageBox.information(self, "修改失败", "课程名不能为空", QMessageBox.Ok)
        else:
            value =(class_name,stu[0][0],flag,time,now_ctid)
            cursor.execute("UPDATE stucheckin SET ctname=%s,sid=%s,ctstate=%s,cttime=%s WHERE ctid=%s",value)
            print(value)
            conn.commit()
        cursor.close()
        conn.close()
        QMessageBox.information(self, "修改成功", "修改成功", QMessageBox.Ok)
    def back(self):
        print("back")
        global now_ctid
        now_ctid = 0
        self.new_window = My_Tch_Checkin_Form()
        self.new_window.show()
        self.close()

    def delete(self):
        print("delete")
        global now_ctid
        conn = pymysql.connect(
            host='localhost',  # 主机名（或IP地址）
            port=3306,  # 端口号，默认为3306
            user='root',  # 用户名
            password='123852',  # 密码
            charset='utf8mb4'  # 设置字符编码
        )
        conn.select_db("checkin")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM stucheckin WHERE ctid=%s", now_ctid)
        conn.commit()
        cursor.close()
        conn.close()
        now_ctid = 0
        self.new_window = My_Tch_Checkin_Form()
        self.new_window.show()
        self.close()
        QMessageBox.information(self, "删除成功", "删除成功", QMessageBox.Ok)


# 注册界面
class My_Register_Form(QMainWindow, Register_Form.Ui_Register_Form):
    def __init__(self, parent=None):
        super(My_Register_Form, self).__init__(parent)
        self.setupUi(self)

    def register(self):
        conn = pymysql.connect(
            host='localhost',  # 主机名（或IP地址）
            port=3306,  # 端口号，默认为3306
            user='root',  # 用户名
            password='123852',  # 密码
            charset='utf8mb4'  # 设置字符编码
        )
        conn.select_db("checkin")
        cursor = conn.cursor()
        user=self.lineEdit.text()
        username=self.lineEdit_2.text()
        userpass1=self.lineEdit_3.text()
        userpass2=self.lineEdit_4.text()
        useridnum=self.lineEdit_5.text()
        if len(user)!=6 and len(user)!=5:
            QMessageBox.information(self, "error!", "用户名为学号或职工号", QMessageBox.Ok)
        elif len(username)<1 or len(username)>4:
            QMessageBox.information(self, "error!", "用户姓名错误", QMessageBox.Ok)
        elif len(userpass1)<6 or len(userpass1)>16:
            QMessageBox.information(self, "error!", "密码为6-16位", QMessageBox.Ok)
        elif userpass2!=userpass1:
            QMessageBox.information(self, "error!", "两次密码不一致", QMessageBox.Ok)
        elif len(useridnum) != 18:
            QMessageBox.information(self, "error!", "身份证号错误", QMessageBox.Ok)
        else:
            print(user,username,userpass1,userpass2,useridnum)
            cursor.execute("SELECT * FROM user WHERE uname=%s",user)
            results = cursor.fetchall()
            QMessageBox.information(self, "注册成功", "注册成功！！！", QMessageBox.Ok)
            if len(results)==0:
                sql1 = "INSERT INTO user (uname, upass, unum, urole) VALUES (%s, %s, %s, %s)"
                if len(user) == 5:
                    values1 = (user, userpass1, useridnum, 1)
                    cursor.execute(sql1, values1)
                    conn.commit()
                    sql2 = "INSERT INTO teacher (uname, tname) VALUES (%s, %s)"
                    values2 = (user, username)
                    cursor.execute(sql2, values2)
                    conn.commit()
                if len(user) == 6:
                    values1 = (user, userpass1, useridnum, 2)
                    cursor.execute(sql1, values1)
                    conn.commit()
                    sql2 = "INSERT INTO student (uname, sname) VALUES (%s, %s)"
                    values2 = (user, username)
                    cursor.execute(sql2, values2)
                    conn.commit()
            else :
                QMessageBox.information(self, "error!", "该职工号或学号已被注册", QMessageBox.Ok)
        cursor.close()
        conn.close()
        print("zhuce")

    def back(self):
        print("back")
        self.new_window=My_Login_Form()
        self.new_window.show()
        self.close()

class My_Tch_stu_form(QMainWindow,Tch_stu_form.Ui_Tch_stu_form):
    def __init__(self, parent=None):
        super(My_Tch_stu_form, self).__init__(parent)
        self.setupUi(self)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setRowCount(0)
        conn = pymysql.connect(
            host='localhost',  # 主机名（或IP地址）
            port=3306,  # 端口号，默认为3306
            user='root',  # 用户名
            password='123852',  # 密码
            charset='utf8mb4'  # 设置字符编码
        )
        conn.select_db("checkin")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM student")
        stu = cursor.fetchall()
        row_count=0
        print(stu)
        for s in stu:
            self.tableWidget.insertRow(row_count)
            self.tableWidget.setItem(row_count, 0, QTableWidgetItem(str(s[0])))
            self.tableWidget.setItem(row_count, 1, QTableWidgetItem(s[1]))
            self.tableWidget.setItem(row_count, 2, QTableWidgetItem(s[2]))
            self.tableWidget.setItem(row_count, 3, QTableWidgetItem(s[3]))
            self.tableWidget.setItem(row_count, 4, QTableWidgetItem(s[4]))
            row_count += 1
        cursor.close()
        conn.close()

    def back(self):
        print("back")
        self.new_window = My_Teacher_Form()
        self.new_window.show()
        self.close()

    def refresh(self):
        print("refresh")
        self.tableWidget.setRowCount(0)
        conn = pymysql.connect(
            host='localhost',  # 主机名（或IP地址）
            port=3306,  # 端口号，默认为3306
            user='root',  # 用户名
            password='123852',  # 密码
            charset='utf8mb4'  # 设置字符编码
        )
        conn.select_db("checkin")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM student")
        stu = cursor.fetchall()
        row_count = 0
        print(stu)
        for s in stu:
            self.tableWidget.insertRow(row_count)
            self.tableWidget.setItem(row_count, 0, QTableWidgetItem(str(s[0])))
            self.tableWidget.setItem(row_count, 1, QTableWidgetItem(s[1]))
            self.tableWidget.setItem(row_count, 2, QTableWidgetItem(s[2]))
            self.tableWidget.setItem(row_count, 3, QTableWidgetItem(s[3]))
            self.tableWidget.setItem(row_count, 4, QTableWidgetItem(s[4]))
            row_count += 1

    def search(self):
        self.tableWidget.setRowCount(0)
        conn = pymysql.connect(
            host='localhost',  # 主机名（或IP地址）
            port=3306,  # 端口号，默认为3306
            user='root',  # 用户名
            password='123852',  # 密码
            charset='utf8mb4'  # 设置字符编码
        )
        conn.select_db("checkin")
        cursor=conn.cursor()
        sid=self.lineEdit.text()
        flag1 = 0
        name=self.lineEdit_2.text()
        flag2 = 0
        class_name=self.lineEdit_3.text()
        flag3 = 0
        if len(sid) != 0:
            flag1 = 1
        if len(name) != 0:
            flag2 = 1
        if len(class_name) != 0:
            flag3 = 1
        sql = "SELECT * FROM student WHERE "
        count = 0
        if flag1 != 0:
            count += 1
            sql = sql + "uname like \'%" + sid + "%\'"
        if flag2 != 0:
            if count > 0:
                sql = sql + " AND "
            count += 1
            sql = sql + "sname like \'%" + name + "%\'"
        if flag3 != 0:
            if count > 0:
                sql = sql + " AND "
            count += 1
            sql = sql + "sclass like \'%" + class_name + "%\'"
        print(sql)
        if count > 0:
            row_count = 0
            cursor.execute(sql)
            stu=cursor.fetchall()
            for s in stu:
                self.tableWidget.insertRow(row_count)
                self.tableWidget.setItem(row_count, 0, QTableWidgetItem(str(s[0])))
                self.tableWidget.setItem(row_count, 1, QTableWidgetItem(s[1]))
                self.tableWidget.setItem(row_count, 2, QTableWidgetItem(s[2]))
                self.tableWidget.setItem(row_count, 3, QTableWidgetItem(s[3]))
                self.tableWidget.setItem(row_count, 4, QTableWidgetItem(s[4]))
                row_count+=1
        cursor.close()
        conn.close()
        print("search")

    def xiugai(self):
        print("xiugai")
        global now_ctid
        for i in self.tableWidget.selectedItems():
            now_ctid = self.tableWidget.item(i.row(), 0).text()
            break
        print(now_ctid)

if __name__ == '__main__':
    app = QApplication(sys.argv)  # 在 QApplication 方法中使用，创建应用程序对象
    main_form=My_Login_Form()
    main_form.show()
    sys.exit(app.exec_())  # 结束进程，退出程序
