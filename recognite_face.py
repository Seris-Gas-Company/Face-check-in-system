import dlib
from imageio import imread
import glob
import numpy as np

detector = dlib.get_frontal_face_detector()
predictor_path = 'shape_predictor_68_face_landmarks.dat'
predictor = dlib.shape_predictor(predictor_path)
face_rec_model_path = 'dlib_face_recognition_resnet_model_v1.dat'
facerec = dlib.face_recognition_model_v1(face_rec_model_path)


def get_feature(path):
    img = imread(path)
    dets = detector(img)
    print('检测到了 %d 个人脸' % len(dets))
    # 这里假设每张图只有一个人脸
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

path_lists1 = ["chenping.png", "vv1.jpg"]
path_lists2 = ["vv2.png", "vvtest.png"]

feature_lists1 = [get_feature(path) for path in path_lists1]
feature_lists2 = [get_feature(path) for path in path_lists2]

print("feature 1 shape", feature_lists1[0].shape)

out1 = distance(feature_lists1[0], feature_lists1[1])
out2 = distance(feature_lists2[0], feature_lists2[1])

print("diff distance is", out1)
print("same distance is", out2)

out1 = distance(feature_lists1[0], feature_lists1[1])
out2 = distance(feature_lists2[0], feature_lists2[1])




print("vvtest is 张维为", classifier(feature_lists2[1], feature_lists2[1]))
print("chenping is 张维为", classifier(feature_lists1[0], feature_lists2[1]))
print("vv1 is 张维为", classifier(feature_lists1[1], feature_lists2[1]))
print("vv2 is 张维为", classifier(feature_lists2[0], feature_lists2[1]))