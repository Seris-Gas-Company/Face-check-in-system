import datetime
from imageio import imread
import dlib
from PIL import Image
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QAbstractItemView, QTableWidgetItem
import sys
from myUI import Login_Form, Register_Form, Student_Form, Teacher_Form, Stu_Inquiry_Form, Stu_Info_Form
from myUI import Tch_Info_Form, Checkin_Form ,Checkin_text, Tch_stu_form, Stu_text,Check1_Form
import pymysql
import numpy as np

def get_feature(path):
    img = imread(path)
    dets = detector(img)
    shape = predictor(img, dets[0])
    face_vector = facerec.compute_face_descriptor(img, shape)
    return (face_vector)
def distance(a, b):
    a, b = np.array(a), np.array(b)
    sub = np.sum((a - b) ** 2)
    add = (np.sum(a ** 2) + np.sum(b ** 2)) / 2.
    return sub / add

def classifier(a, b, t=0.09):
    if (distance(a, b) <= t):
        ret = True
    else:
        ret = False
    return (ret)

# 导入模型
detector = dlib.get_frontal_face_detector()
predictor_path = 'shape_predictor_68_face_landmarks.dat'
predictor = dlib.shape_predictor(predictor_path)
face_rec_model_path = 'dlib_face_recognition_resnet_model_v1.dat'
facerec = dlib.face_recognition_model_v1(face_rec_model_path)
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
            self.tableWidget.setItem(row_count, 0, QTableWidgetItem(result[1]))
            if result[3]==1:
                self.tableWidget.setItem(row_count, 1, QTableWidgetItem("签到"))
            elif result[3]==2:
                self.tableWidget.setItem(row_count, 1, QTableWidgetItem("请假"))
            elif result[3]==3:
                self.tableWidget.setItem(row_count, 1, QTableWidgetItem("迟到"))
            elif result[3]==4:
                self.tableWidget.setItem(row_count, 1, QTableWidgetItem("早退"))
            elif result[3]==5:
                self.tableWidget.setItem(row_count, 1, QTableWidgetItem("旷课"))
            else :
                self.tableWidget.setItem(row_count, 1, QTableWidgetItem("没点名"))
            self.tableWidget.setItem(row_count, 2, QTableWidgetItem(stu[0][1]))
            self.tableWidget.setItem(row_count, 3, QTableWidgetItem(stu[0][2]))
            self.tableWidget.setItem(row_count, 4, QTableWidgetItem(result[5]))
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
        self.new_window = My_Check1_Form()
        self.new_window.show()
        self.close()

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

# 学生管理
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
        self.newf = My_Tch_stu_text()
        self.newf.show()
        self.close()

# 学生修改
class My_Tch_stu_text(QMainWindow,Stu_text.Ui_Stu_text):
    def __init__(self, parent=None):
        super(My_Tch_stu_text, self).__init__(parent)
        self.setupUi(self)
        self.setAcceptDrops(True)
        conn = pymysql.connect(
            host='localhost',  # 主机名（或IP地址）
            port=3306,  # 端口号，默认为3306
            user='root',  # 用户名
            password='123852',  # 密码
            charset='utf8mb4'  # 设置字符编码
        )
        conn.select_db("checkin")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM student WHERE sid=%s",now_ctid)
        stu = cursor.fetchall()
        self.lineEdit.setText(stu[0][1])
        self.lineEdit_2.setText(stu[0][2])
        self.lineEdit_3.setText(stu[0][3])
        self.lineEdit_4.setText(stu[0][4])

    def save(self):
        uname=self.lineEdit.text()
        sname=self.lineEdit_2.text()
        sclass=self.lineEdit_3.text()
        if len(self.lineEdit_4.text())>0:
            if self.lineEdit_4.text().endswith(('.gif', '.jpg', '.png')):
                detector = dlib.get_frontal_face_detector()
                try:
                    img = imread(self.lineEdit_4.text())
                    dets = detector(img)
                    if len(dets)==0:
                        spic=""
                        QMessageBox.information(self, "error!", "未检测到人脸", QMessageBox.Ok)
                    elif len(dets)>1:
                        spic=""
                        QMessageBox.information(self, "error!", "检测到过多人脸", QMessageBox.Ok)
                    else:
                        spic = self.lineEdit_4.text()
                except:
                    spic=""
                    QMessageBox.information(self, "error!", "请检查文件路径", QMessageBox.Ok)
            else:
                spic = ""
                QMessageBox.information(self, "error!", "不支持改文件格式", QMessageBox.Ok)
        else:
            spic = ""
        value=(uname,sname,sclass,spic,now_ctid)
        conn = pymysql.connect(
            host='localhost',  # 主机名（或IP地址）
            port=3306,  # 端口号，默认为3306
            user='root',  # 用户名
            password='123852',  # 密码
            charset='utf8mb4'  # 设置字符编码
        )
        conn.select_db("checkin")
        cursor = conn.cursor()
        cursor.execute("UPDATE student SET uname=%s,sname=%s,sclass=%s,spic=%s WHERE sid=%s", value)
        conn.commit()
        cursor.close()
        conn.close()
        print("save")

    def back(self):
        print("back")
        global now_ctid
        now_ctid = 0
        self.newf = My_Tch_stu_form()
        self.newf.show()
        self.close()

    def open(self):
        if len(self.lineEdit_4.text())==0:
            QMessageBox.information(self, "error!", "照片路径不能为空", QMessageBox.Ok)
        elif self.lineEdit_4.text().endswith(('.gif', '.jpg', '.png')):
            img = Image.open(self.lineEdit_4.text())
            img.show()
        else:
            QMessageBox.information(self, "error!", "不支持该文件类型", QMessageBox.Ok)

    def dragEnterEvent(self, evn):
        self.setWindowTitle('鼠标拖入窗口了')
        self.lineEdit_4.setText(evn.mimeData().text().strip('file:///'))
        evn.accept()

    def dropEvent(self, evn):
        self.setWindowTitle('鼠标放开了')

    def dragMoveEvent(self, evn):
        print('鼠标移入')

# 非实时签到
class My_Check1_Form(QMainWindow,Check1_Form.Ui_Check1_Form):
    def __init__(self, parent=None):
        super(My_Check1_Form, self).__init__(parent)
        self.setupUi(self)
        self.setAcceptDrops(True)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget_2.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setRowCount(0)
        self.tableWidget_2.setRowCount(0)
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
            self.tableWidget.setItem(row_count, 0, QTableWidgetItem(s[3]))
            self.tableWidget.setItem(row_count, 1, QTableWidgetItem(s[1]))
            self.tableWidget.setItem(row_count, 2, QTableWidgetItem(s[2]))
            self.tableWidget.setItem(row_count, 3, QTableWidgetItem(str(s[0])))
            row_count += 1
        now = datetime.datetime.now()
        now_time = str(now.year) + "/" + str(now.month) + "/" + str(now.day)
        cursor.execute("SELECT tid FROM teacher WHERE uname=%s", static_login_user)
        tid = cursor.fetchall()
        sql="SELECT * FROM stucheckin WHERE cttime like \'%" +now_time+ "%\' AND tid =" +str(tid[0][0])
        print(sql)
        cursor.execute(sql)
        results = cursor.fetchall()
        print(results)
        row_count = 0
        for result in results:
            self.tableWidget_2.insertRow(row_count)
            cursor.execute("SELECT uname,sname FROM student WHERE sid=%s", result[2])
            stu = cursor.fetchall()
            self.tableWidget_2.setItem(row_count, 0, QTableWidgetItem(result[5])) # 时间
            self.tableWidget_2.setItem(row_count, 1, QTableWidgetItem(result[1])) # 课程名
            self.tableWidget_2.setItem(row_count, 2, QTableWidgetItem(stu[0][1])) # 姓名
            self.tableWidget_2.setItem(row_count, 3, QTableWidgetItem(stu[0][0])) # 学号
            # 情况
            if result[3] == 1:
                self.tableWidget_2.setItem(row_count, 4, QTableWidgetItem("签到"))
            elif result[3] == 2:
                self.tableWidget_2.setItem(row_count, 4, QTableWidgetItem("请假"))
            elif result[3] == 3:
                self.tableWidget_2.setItem(row_count, 4, QTableWidgetItem("迟到"))
            elif result[3] == 4:
                self.tableWidget_2.setItem(row_count, 4, QTableWidgetItem("早退"))
            elif result[3] == 5:
                self.tableWidget_2.setItem(row_count, 4, QTableWidgetItem("旷课"))
            else:
                self.tableWidget_2.setItem(row_count, 4, QTableWidgetItem("没点名"))
            # 编号
            self.tableWidget_2.setItem(row_count, 5, QTableWidgetItem(str(result[0])))
            row_count += 1
        cursor.close()
        conn.close()

    def refresh(self):
        print("refresh")
        self.label_5.setText("学生")
        global now_ctid
        now_ctid=0
        self.tableWidget.setRowCount(0)
        self.tableWidget_2.setRowCount(0)
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
            self.tableWidget.setItem(row_count, 0, QTableWidgetItem(s[3]))
            self.tableWidget.setItem(row_count, 1, QTableWidgetItem(s[1]))
            self.tableWidget.setItem(row_count, 2, QTableWidgetItem(s[2]))
            self.tableWidget.setItem(row_count, 3, QTableWidgetItem(str(s[0])))
            row_count += 1
        now = datetime.datetime.now()
        now_time = str(now.year) + "/" + str(now.month) + "/" + str(now.day)
        cursor.execute("SELECT tid FROM teacher WHERE uname=%s", static_login_user)
        tid = cursor.fetchall()
        sql = "SELECT * FROM stucheckin WHERE cttime like \'%" + now_time + "%\' AND tid =" + str(tid[0][0])
        print(sql)
        cursor.execute(sql)
        results = cursor.fetchall()
        print(results)
        row_count = 0
        for result in results:
            self.tableWidget_2.insertRow(row_count)
            cursor.execute("SELECT uname,sname FROM student WHERE sid=%s", result[2])
            stu = cursor.fetchall()
            self.tableWidget_2.setItem(row_count, 0, QTableWidgetItem(result[5]))  # 时间
            self.tableWidget_2.setItem(row_count, 1, QTableWidgetItem(result[1]))  # 课程名
            self.tableWidget_2.setItem(row_count, 2, QTableWidgetItem(stu[0][1]))  # 姓名
            self.tableWidget_2.setItem(row_count, 3, QTableWidgetItem(stu[0][0]))  # 学号
            # 情况
            if result[3] == 1:
                self.tableWidget_2.setItem(row_count, 4, QTableWidgetItem("签到"))
            elif result[3] == 2:
                self.tableWidget_2.setItem(row_count, 4, QTableWidgetItem("请假"))
            elif result[3] == 3:
                self.tableWidget_2.setItem(row_count, 4, QTableWidgetItem("迟到"))
            elif result[3] == 4:
                self.tableWidget_2.setItem(row_count, 4, QTableWidgetItem("早退"))
            elif result[3] == 5:
                self.tableWidget_2.setItem(row_count, 4, QTableWidgetItem("旷课"))
            else:
                self.tableWidget_2.setItem(row_count, 4, QTableWidgetItem("没点名"))
            # 编号
            self.tableWidget_2.setItem(row_count, 5, QTableWidgetItem(str(result[0])))
            row_count += 1
        cursor.close()
        conn.close()

    def search(self):
        self.tableWidget.setRowCount(0)
        global now_ctid
        now_ctid=0
        self.label_5.setText("学生")
        conn = pymysql.connect(
            host='localhost',  # 主机名（或IP地址）
            port=3306,  # 端口号，默认为3306
            user='root',  # 用户名
            password='123852',  # 密码
            charset='utf8mb4'  # 设置字符编码
        )
        conn.select_db("checkin")
        cursor=conn.cursor()
        sid=self.lineEdit_2.text()
        flag1 = 0
        class_name=self.lineEdit_3.text()
        flag2 = 0
        if len(sid) != 0:
            flag1 = 1
        if len(class_name) != 0:
            flag2 = 1
        sql = "SELECT * FROM student WHERE "
        count = 0
        if flag1 != 0:
            count += 1
            sql = sql + "uname like \'%" + sid + "%\'"
        if flag2 != 0:
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
                # 班级
                self.tableWidget.setItem(row_count, 0, QTableWidgetItem(s[3]))
                # 学号
                self.tableWidget.setItem(row_count, 1, QTableWidgetItem(s[1]))
                # 姓名
                self.tableWidget.setItem(row_count, 2, QTableWidgetItem(s[2]))
                # 编号
                self.tableWidget.setItem(row_count, 3, QTableWidgetItem(str(s[0])))
                row_count+=1
        cursor.close()
        conn.close()
        print("search")

    def select_student(self):
        global now_ctid
        name=""
        for i in self.tableWidget.selectedItems():
            now_ctid = self.tableWidget.item(i.row(), 3).text()
            name=self.tableWidget.item(i.row(),2).text()+self.tableWidget.item(i.row(),1).text()
            break
        self.label_5.setText("当前学生:"+name)
        print("select_student")

    def select_checkin(self):
        global now_ctid
        for i in self.tableWidget_2.selectedItems():
            now_ctid = self.tableWidget_2.item(i.row(), 5).text()
            break
        self.label_5.setText("学生")
        print("select_checkin")
        self.new_window = My_Checkin_text()
        self.new_window.show()
        self.close()

    def pic(self):
        print("pic")
        if len(self.lineEdit.text())>0:
            pic1_path=self.lineEdit.text()
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
            cursor.execute("SELECT tid FROM teacher WHERE uname=%s", static_login_user)
            tid = cursor.fetchall()[0][0]
            cursor = conn.cursor()
            if now_ctid == 0:
                QMessageBox.information(self, "error!", "未选中学生", QMessageBox.Ok)
            elif len(self.lineEdit_4.text()) == 0:
                QMessageBox.information(self, "error!", "课程名称不能为空", QMessageBox.Ok)
            else:
                cursor.execute("SELECT * FROM student WHERE sid=%s", now_ctid)
                s = cursor.fetchall()
                pic2_path = s[0][4]
                if len(pic2_path) == 0:
                    QMessageBox.information(self, "error!", "该生未录入照片", QMessageBox.Ok)
                else:
                    feature_lists1=get_feature(pic1_path)
                    feature_lists2=get_feature(pic2_path)
                    if classifier(feature_lists1, feature_lists2):
                        now = datetime.datetime.now()
                        now_time = str(now.year) + "/" + str(now.month) + "/" + str(now.day) + " " + str(now.hour) + ":" + str(
                            now.minute)
                        value = (self.lineEdit_4.text(), now_ctid, 1, tid, now_time)
                        print(value)
                        sql = "INSERT INTO stucheckin (ctname,sid,ctstate,tid,cttime) VALUES (%s,%s,%s,%s,%s);"
                        cursor.execute(sql, value)
                        conn.commit()
                        now_ctid = 0
                        self.label_5.setText("学生")
                        QMessageBox.information(self, "签到成功", "已签到！", QMessageBox.Ok)
                    else:
                        QMessageBox.information(self, "error!", "照片与数据库当中的人不一致", QMessageBox.Ok)
                cursor.close()
                conn.close()
        else:
            QMessageBox.information(self, "error!", "照片路径不能为空", QMessageBox.Ok)

    def back(self):
        global now_ctid
        now_ctid=0
        print("back")
        self.new_window = My_Teacher_Form()
        self.new_window.show()
        self.close()

    def qiandao(self):
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
        cursor.execute("SELECT tid FROM teacher WHERE uname=%s",static_login_user)
        if now_ctid==0:
            QMessageBox.information(self, "error!", "未选中学生", QMessageBox.Ok)
        elif len(self.lineEdit_4.text())==0:
            QMessageBox.information(self, "error!", "课程名称不能为空", QMessageBox.Ok)
        else:
            tid=cursor.fetchall()[0][0]
            now=datetime.datetime.now()
            now_time=str(now.year)+"/"+str(now.month)+"/"+str(now.day)+" "+str(now.hour)+":"+str(now.minute)
            value=(self.lineEdit_4.text(),now_ctid,1,tid,now_time)
            print(value)
            sql="INSERT INTO stucheckin (ctname,sid,ctstate,tid,cttime) VALUES (%s,%s,%s,%s,%s);"
            cursor.execute(sql,value)
            conn.commit()
            now_ctid = 0
            self.label_5.setText("学生")
            QMessageBox.information(self, "签到成功", "已签到！", QMessageBox.Ok)
        cursor.close()
        conn.close()

    def qingjia(self):
        print("qingjia")
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
        cursor.execute("SELECT tid FROM teacher WHERE uname=%s", static_login_user)
        if now_ctid == 0:
            QMessageBox.information(self, "error!", "未选中学生", QMessageBox.Ok)
        elif len(self.lineEdit_4.text()) == 0:
            QMessageBox.information(self, "error!", "课程名称不能为空", QMessageBox.Ok)
        else:
            tid = cursor.fetchall()[0][0]
            now = datetime.datetime.now()
            now_time = str(now.year) + "/" + str(now.month) + "/" + str(now.day) + " " + str(now.hour) + ":" + str(
                now.minute)
            value = (self.lineEdit_4.text(), now_ctid, 2, tid, now_time)
            print(value)
            sql = "INSERT INTO stucheckin (ctname,sid,ctstate,tid,cttime) VALUES (%s,%s,%s,%s,%s);"
            cursor.execute(sql, value)
            conn.commit()
            now_ctid = 0
            self.label_5.setText("学生")
            QMessageBox.information(self, "请假", "已记录该学生请假！", QMessageBox.Ok)
        cursor.close()
        conn.close()

    def chidao(self):
        print("chidao")
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
        cursor.execute("SELECT tid FROM teacher WHERE uname=%s", static_login_user)
        if now_ctid == 0:
            QMessageBox.information(self, "error!", "未选中学生", QMessageBox.Ok)
        elif len(self.lineEdit_4.text()) == 0:
            QMessageBox.information(self, "error!", "课程名称不能为空", QMessageBox.Ok)
        else:
            tid = cursor.fetchall()[0][0]
            now = datetime.datetime.now()
            now_time = str(now.year) + "/" + str(now.month) + "/" + str(now.day) + " " + str(now.hour) + ":" + str(
                now.minute)
            value = (self.lineEdit_4.text(), now_ctid, 3, tid, now_time)
            print(value)
            sql = "INSERT INTO stucheckin (ctname,sid,ctstate,tid,cttime) VALUES (%s,%s,%s,%s,%s);"
            cursor.execute(sql, value)
            conn.commit()
            now_ctid = 0
            self.label_5.setText("学生")
            QMessageBox.information(self, "迟到", "已记录该学生迟到！", QMessageBox.Ok)
        cursor.close()
        conn.close()

    def zaotui(self):
        print("zaotui")
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
        cursor.execute("SELECT tid FROM teacher WHERE uname=%s", static_login_user)
        if now_ctid == 0:
            QMessageBox.information(self, "error!", "未选中学生", QMessageBox.Ok)
        elif len(self.lineEdit_4.text()) == 0:
            QMessageBox.information(self, "error!", "课程名称不能为空", QMessageBox.Ok)
        else:
            tid = cursor.fetchall()[0][0]
            now = datetime.datetime.now()
            now_time = str(now.year) + "/" + str(now.month) + "/" + str(now.day) + " " + str(now.hour) + ":" + str(
                now.minute)
            value = (self.lineEdit_4.text(), now_ctid, 4, tid, now_time)
            print(value)
            sql = "INSERT INTO stucheckin (ctname,sid,ctstate,tid,cttime) VALUES (%s,%s,%s,%s,%s);"
            cursor.execute(sql, value)
            conn.commit()
            now_ctid = 0
            self.label_5.setText("学生")
            QMessageBox.information(self, "早退", "已记录该学生早退！", QMessageBox.Ok)
        cursor.close()
        conn.close()

    def kuangke(self):
        print("kuangke")
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
        cursor.execute("SELECT tid FROM teacher WHERE uname=%s", static_login_user)
        if now_ctid == 0:
            QMessageBox.information(self, "error!", "未选中学生", QMessageBox.Ok)
        elif len(self.lineEdit_4.text()) == 0:
            QMessageBox.information(self, "error!", "课程名称不能为空", QMessageBox.Ok)
        else:
            tid = cursor.fetchall()[0][0]
            now = datetime.datetime.now()
            now_time = str(now.year) + "/" + str(now.month) + "/" + str(now.day) + " " + str(now.hour) + ":" + str(
                now.minute)
            value = (self.lineEdit_4.text(), now_ctid, 5, tid, now_time)
            print(value)
            sql = "INSERT INTO stucheckin (ctname,sid,ctstate,tid,cttime) VALUES (%s,%s,%s,%s,%s);"
            cursor.execute(sql, value)
            conn.commit()
            now_ctid = 0
            self.label_5.setText("学生")
            QMessageBox.information(self, "旷课", "已记录该学生旷课！", QMessageBox.Ok)
        cursor.close()
        conn.close()

    def dragEnterEvent(self, evn):
        self.setWindowTitle('鼠标拖入窗口了')
        self.lineEdit.setText(evn.mimeData().text().strip('file:///'))
        evn.accept()

    def dropEvent(self, evn):
        self.setWindowTitle('鼠标放开了')

    def dragMoveEvent(self, evn):
        print('鼠标移入')
# 实时签到


if __name__ == '__main__':
    app = QApplication(sys.argv)  # 在 QApplication 方法中使用，创建应用程序对象
    main_form=My_Login_Form()
    main_form.show()
    sys.exit(app.exec_())  # 结束进程，退出程序
