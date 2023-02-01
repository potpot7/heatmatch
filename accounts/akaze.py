import os
import cv2
import matplotlib.pyplot as plt
from django.utils import timezone

# １枚目の画像を読み込む
img1 = cv2.imread('c:/Users/kadom/Documents/wasi.jpg') 
# ２枚目の画像を読み込む
img2 = cv2.imread('c:/Users/kadom/Documents/mukai.jpg') 

# １枚目の画像をグレースケールで読み出し
gray1 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY) 
# ２枚目の画像をグレースケールで読み出し
gray2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY) 

# AKAZE検出器の生成
akaze = cv2.AKAZE_create() 
# gray1にAKAZEを適用、特徴点を検出
kp1, des1 = akaze.detectAndCompute(gray1,None) 
# gray2にAKAZEを適用、特徴点を検出
kp2, des2 = akaze.detectAndCompute(gray2,None) 

# BFMatcherオブジェクトの生成
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# Match descriptorsを生成
matches = bf.match(des1, des2)

# matchesをdescriptorsの似ている順にソートする 
matches = sorted(matches, key = lambda x:x.distance)

# 検出結果を描画する
img3 = cv2.drawMatches(img1, kp1, img2, kp2, matches[:10], None, flags = cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

# cv2.imshow('img',img3)
plt.figure(figsize=(10,10))
plt.imshow(cv2.cvtColor(img3, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.show()
#検出結果を描画した画像を出力する
# image_name = 'c:/Users/kadom/Documents/test2.png'
# cv2.imwrite(image_name,img3)


# TARGET_FILE = [image_name]
# IMG_DIR = os.path.abspath(os.path.dirname(__file__)) + 'images/'
# IMG_SIZE = (200, 200)

# target_img_path = IMG_DIR + TARGET_FILE
# #ターゲット画像をグレースケールで読み出し
# target_img = cv2.imread(target_img_path, cv2.IMREAD_GRAYSCALE)
# #ターゲット画像を200px×200pxに変換
# target_img = cv2.resize(target_img, IMG_SIZE)

# # BFMatcherオブジェクトの生成
# bf = cv2.BFMatcher(cv2.NORM_HAMMING)

# # AKAZEを適用、特徴点を検出
# detector = cv2.AKAZE_create()
# (target_kp, target_des) = detector.detectAndCompute(target_img, None)

# print('TARGET_FILE: %s' % (TARGET_FILE))

# files = os.listdir(IMG_DIR)
# for file in files:
#     if file == '.DS_Store' or file == TARGET_FILE:
#         continue
#     #比較対象の写真の特徴点を検出
#     comparing_img_path = IMG_DIR + file
#     try:
#         comparing_img = cv2.imread(comparing_img_path, cv2.IMREAD_GRAYSCALE)
#         comparing_img = cv2.resize(comparing_img, IMG_SIZE)
#         (comparing_kp, comparing_des) = detector.detectAndCompute(comparing_img, None)
#         # BFMatcherで総当たりマッチングを行う
#         matches = bf.match(target_des, comparing_des)
#         #特徴量の距離を出し、平均を取る
#         dist = [m.distance for m in matches]
#         ret = sum(dist) / len(dist)
#     except cv2.error:
#         # cv2がエラーを吐いた場合の処理
#         ret = 100000

#     print(file, ret)