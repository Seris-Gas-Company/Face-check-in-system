import dlib  # 人脸识别的库dlib

import cv2  # 图像处理的库OpenCV

"""
从电脑摄像头 视屏中识别人脸，并实时标出面部特征点
"""

# 使用特征提取器get_frontal_face_detector
detector = dlib.get_frontal_face_detector()
# 也可读入视频文件
# cap = cv2.VideoCapture("row.MP4")
# 建cv2摄像头对象，这里使用电脑自带摄像头，如果接了外部摄像头，则自动切换到外部摄像头
cap = cv2.VideoCapture(0)

# 设置视频参数，propId设置的视频参数，value设置的参数值
cap.set(3, 480)
# 截图screenshoot的计数器
cnt = 0
# cap.isOpened（） 返回true/false 检查初始化是否成功
while (cap.isOpened()):

    # cap.read()
    # 返回两个值：
    #  一个布尔值true/false，用来判断读取视频是否成功/是否到视频末尾
    #  图像对象，图像的三维矩阵
    flag, im_rd = cap.read()

    # 每帧数据延时1ms，延时为0读取的是静态帧
    k = cv2.waitKey(1)

    # 取灰度
    img_gray = cv2.cvtColor(im_rd, cv2.COLOR_RGB2GRAY)

    # 使用人脸检测器检测每一帧图像中的人脸。并返回人脸数rects
    faces = detector(img_gray, 0)

    # 待会要显示在屏幕上的字体
    font = cv2.FONT_HERSHEY_SIMPLEX

    # 如果检测到人脸
    if (len(faces) != 0):

        # 对每个人脸都画出框框
        for i in range(len(faces)):
            # enumerate方法同时返回数据对象的索引和数据，k为索引，d为faces中的对象
            for k, d in enumerate(faces):
                # 用红色矩形框出人脸
                cv2.rectangle(im_rd, (d.left(), d.top()), (d.right(), d.bottom()), (0, 255, 0), 2)
                # 计算人脸热别框边长
                face_width = d.right() - d.left()
                # 在上方显示文字
                cv2.putText(im_rd, str(face_width), (d.left(), d.top() - 20), font, 0.5, (255, 0, 0), 1)
        # 标出人脸数
        cv2.putText(im_rd, "Faces: " + str(len(faces)), (20, 50), font, 1, (0, 0, 255), 1, cv2.LINE_AA)
    else:
        # 没有检测到人脸
        cv2.putText(im_rd, "No Face", (20, 50), font, 1, (0, 0, 255), 1, cv2.LINE_AA)

    # 添加说明
    im_rd = cv2.putText(im_rd, "S: screenshot", (20, 400), font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
    im_rd = cv2.putText(im_rd, "Q: quit", (20, 450), font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)

    # 检测按键
    k = cv2.waitKey(1)
    # 按下s键截图保存
    if (k == ord('s')):
        cnt += 1
        cv2.imwrite("screenshoot" + str(cnt) + ".jpg", im_rd)
    # 按下q键退出
    if (k == ord('q')):
        break

    # 窗口显示
    cv2.imshow("camera", im_rd)

# 释放摄像头
cap.release()
# 删除建立的窗口
cv2.destroyAllWindows()