import json
import numpy as np
import cv2
import glob
import os

def get_target_value(key, dic):
    if not isinstance(dic, dict) or not isinstance(tmp_list, list):
        return 'argv[1] not an dict or argv[-1] not an list '

    if key in dic.keys():
        tmp_list.append(dic[key])
    else:
        for value in dic.values():
            if isinstance(value, dict):
                get_target_value(key, value)
            elif isinstance(value, (list, tuple)):
                _get_value(key, value)
    return tmp_list
def _get_value(key, val):
    for val_ in val:
        if isinstance(val_, dict):
            get_target_value(key, val_)
        elif isinstance(val_, (list, tuple)):
            _get_value(key, val_)
def UID_Point_List(path_list):
    key1 = path_list[0].keys()
    key2 = path_list[1].keys()
    Key_List1 = list(key1)
    Key_List2 = list(key2)

    value_list1 = path_list[0].values()
    value_list2 = path_list[1].values()
    Tmp1 = list(value_list1)
    Tmp2 = list(value_list2)
    Value_list1 = Tmp1
    Value_list2 = Tmp2
    return Key_List1, Key_List2, Value_list1, Value_list2
def file_name(file_dir):
    tmp = []
    UID = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.jpg':
                #L.append(os.path.join(root, file))
                tmp.append(file)
    for i in range(len(tmp)):
        Ntmp = tmp[i]
        MNtmp = Ntmp[:-4]
        UID.append(MNtmp)
    #print(UID)
    return UID
def main_program(path_list, images, f_name):
    key1 = list(path_list[0].keys())
    key2 = list(path_list[1].keys())
    value1 = list(path_list[0].values())
    value2 = list(path_list[1].values())

    for i in range(len(key1)):
        for j in range(len(f_name)): # Group 1(Left)
            if key1[i] == f_name[j]:
                P_Grp1 = []
                for k in range(len(value1[i][0])):
                    Xtmp1 = value1[i][0][k]['x']
                    Ytmp1 = value1[i][0][k]['y']
                    P_Grp1.append([Xtmp1, Ytmp1])
                    cut_image1(P_Grp1, images[j], f_name[j])#Crop out the ROI region of each image，P_Grp1 is the array of edge points: [[x1, y1]...[xn,yn]]
    for i in range(len(key2)):
        for j in range(len(f_name)): # Group 2(Right)
            if key2[i] == f_name[j]:
                P_Grp2 = []
                for k in range(len(value2[i][0])):
                    Xtmp2 = value2[i][0][k]['x']
                    Ytmp2 = value2[i][0][k]['y']
                    P_Grp2.append(([Xtmp2, Ytmp2]))
                    cut_image2(P_Grp2, images[j], f_name[j])
def cut_image1(P_Grp, image, filename): #Crop out the ROI of each image (left side)
    img = image
    pts = np.array([P_Grp]).reshape((-1, 1, 2)).astype(np.int32)

    # (1) Crop the bounding rect
    rect = cv2.boundingRect(pts)
    x, y, w, h = rect
    croped = img[y:y + h, x:x + w].copy()

    # (2) make mask
    pts = pts - pts.min(axis=0)

    mask = np.zeros(croped.shape[:2], np.uint8)
    cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)

    # (3) do bit-op
    dst = cv2.bitwise_and(croped, croped, mask=mask)

    cv2.imwrite("D:/Images/cut/7324_15130_1/%s" % filename + ".jpg", dst)
def cut_image2(P_Grp, image, filename): # (Right side)
    img = image
    pts = np.array([P_Grp]).reshape((-1, 1, 2)).astype(np.int32)

    # (1) Crop the bounding rect
    rect = cv2.boundingRect(pts)
    x, y, w, h = rect
    croped = img[y:y + h, x:x + w].copy()

    # (2) make mask
    pts = pts - pts.min(axis=0)

    mask = np.zeros(croped.shape[:2], np.uint8)
    cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)

    # (3) do bit-op
    dst = cv2.bitwise_and(croped, croped, mask=mask)

    cv2.imwrite("D:/Images/cut/7324_15130_2/%s" % filename + ".jpg", dst)

tmp_list = []
paths_list = []
images=[]

file = open('D:/Images/jsons/1.2.840.113704.7.32.0619.2.340.3.2831178315.480.1513207304.457.3.json', encoding='utf-8')  #Target json file
images_dir = 'D:/Images/output/7324_15130' #Target jpg images rebuilt from dicom files
images = [cv2.imread(file) for file in glob.glob("D:/Images/output/7324_15130/*.jpg")]
user_dic = json.load(file)  #Read json files

filename = file_name(images_dir)
paths_list = get_target_value('paths', user_dic) #Read all SOPInstanceUIDs which include contour points in corresponding json file
key_list1, key_list2, value_list1, value_list2 = UID_Point_List(paths_list)
main_program(paths_list, images, filename)
