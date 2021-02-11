# Copyright (C) 2020 coneypo
# SPDX-License-Identifier: MIT

# Author:   coneypo
# Blog:     http://www.cnblogs.com/AdaminXie
# GitHub:   https://github.com/coneypo/Dlib_face_recognition_from_camera
# Mail:     coneypo@foxmail.com

# "features_all.csv" / Extract features from images and save into "features_all.csv"

import os
import dlib
from skimage import io
import csv
import numpy as np
import glob
import firebase_connect as fc

# Path of cropped faces
path_images_from_camera = "data/data_faces_from_camera/"

# Use frontal face detector of Dlib
detector = dlib.get_frontal_face_detector()

# Get face landmarks
predictor = dlib.shape_predictor('data/data_dlib/shape_predictor_68_face_landmarks.dat')

# Use Dlib resnet50 model to get 128D face descriptor
face_reco_model = dlib.face_recognition_model_v1("data/data_dlib/dlib_face_recognition_resnet_model_v1.dat")

user_num=fc.file_name


# Return 128D features for single image
# Input:    path_img           <class 'str'>
# Output:   face_descriptor    <class 'dlib.vector'>
def return_128d_features(path_img):
    img_rd = io.imread(path_img)
    faces = detector(img_rd, 1)

    print("%-40s %-20s" % ("Image with faces detected:", path_img), '\n')

    # For photos of faces saved, we need to make sure that we can detect faces from the cropped images
    if len(faces) != 0:
        shape = predictor(img_rd, faces[0])
        face_descriptor = face_reco_model.compute_face_descriptor(img_rd, shape)
    else:
        face_descriptor = 0
        print("no face")
    return face_descriptor


# Return the mean value of 128D face descriptor for person X
# Input:    path_faces_personX       <class 'str'>
# Output:   features_mean_personX    <class 'numpy.ndarray'>
def return_features_mean_personX(path_faces_personX):
    features_list_personX = []
    photos_list = os.listdir(path_faces_personX)
    if photos_list:
        for i in range(len(photos_list)):
            #  Get 128D features for single image of personX
            print("%-40s %-20s" % ("正在读的人脸图像 / Reading image:", path_faces_personX + "/" + photos_list[i]))
            features_128d = return_128d_features(path_faces_personX + "/" + photos_list[i])
            #  Jump if no face detected from image
            if features_128d == 0:
                i += 1
            else:
                features_list_personX.append(features_128d)
    else:
        print(" Warning: No images in " + path_faces_personX + '/', '\n')

    #  Compute the mean
    if features_list_personX:
        features_mean_personX = np.array(features_list_personX).mean(axis=0)
    else:
        features_mean_personX = np.zeros(128, dtype=int, order='C')
    print(type(features_mean_personX))
    return features_mean_personX


# Get the order of latest person
person_list = os.listdir("data/data_faces_from_camera/"+str(user_num)) #원래는 data/data_faces_from_camera/  한명만 읽을려면 data/data_faces_from_camera/사번
#person_list = os.listdir("data/data_faces_from_camera/person_3")
# person_num_list = []
# for person in person_list:
#     person_num_list.append(int(person.split('_')[-1]))
# person_cnt = max(person_num_list)

#여러명 read
# with open("data/csv/new.csv", "w", newline="") as csvfile:
#     writer = csv.writer(csvfile)
#     for person in range(person_cnt):
#         # Get the mean/average features of face/personX, it will be a list with a length of 128D
#         print(path_images_from_camera + "person_" + str(person + 1))
#         features_mean_personX = return_features_mean_personX(path_images_from_camera + "person_" + str(person + 1))
#         writer.writerow(features_mean_personX)
#         print("The mean of features:", list(features_mean_personX))
#         print('\n')
#     print(" Save all the features of faces registered into: data/features_all.csv")

#한명만 read
with open("data/csv/new.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)

    features_mean_personX = return_features_mean_personX(path_images_from_camera +str(user_num)) #"person_3"에 사번넣기
    #features_mean_personX = return_features_mean_personX(path_images_from_camera + "person_3")
    #여기에 모든 1열에 사번추가하는 코드 추가
    #list=[20172183] #사번
    list=[]
    list.append(int(user_num)) #user_num을 숫자로 넣기
    list.extend(features_mean_personX)
    writer.writerow(list)


path = 'data/csv/' #CSV 파일이 존재하는 경로
merge_path = 'data/csv/merge.csv' #최종Merge file
file_list = glob.glob(path + '*') #1. merge 대상 파일을 확인

with open(merge_path, 'w') as f: #2-1.merge할 파일을 열고
    writer = csv.writer(f)
    for file in file_list:
        with open(file ,'r') as f2:
            while True:
                line = f2.readline() #2.merge 대상 파일의 row 1줄을 읽어서

                if not line: #row가 없으면 해당 csv 파일 읽기 끝
                    break

                f.write(line) #3.읽은 row 1줄을 merge할 파일에 쓴다.
            file_name = file.split('\\')[-1]
            print(file.split('\\')[-1] + ' write complete...')

    print('>>> All file merge complete...')
