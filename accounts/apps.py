from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

# import cv2
# import os
# import matplotlib.pyplot as plt
# from datetime import datetime

# # １枚目の画像を読み込む
# img1 = cv2.imread('C:/Users/1101_python/Pictures/Saved Pictures/illust.png') 
# # ２枚目の画像を読み込む
# img2 = cv2.imread('C:/Users/1101_python/Pictures/Saved Pictures/male2.jpg') 
# IMG_SIZE = (200, 200)


# # １枚目の画像をグレースケールで読み出し
# gray1 = cv2.resize(img1,IMG_SIZE)
# gray1 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY) 
# # ２枚目の画像をグレースケールで読み出し
# gray2 = cv2.resize(img2,IMG_SIZE)
# gray2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY) 

# # AKAZE検出器の生成
# akaze = cv2.AKAZE_create() 
# # gray1にAKAZEを適用、特徴点を検出
# kp1, des1 = akaze.detectAndCompute(gray1,None) 
# # gray2にAKAZEを適用、特徴点を検出
# kp2, des2 = akaze.detectAndCompute(gray2,None) 

# # BFMatcherオブジェクトの生成
# bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# # Match descriptorsを生成
# matches = bf.match(des1, des2)

# # matchesをdescriptorsの似ている順にソートする 
# matches = sorted(matches, key = lambda x:x.distance)

# # 検出結果を描画する
# img3 = cv2.drawMatches(img1, kp1, img2, kp2, matches[:30], None, flags = cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
# print(img3)
# #検出結果を描画した画像を出力する
# now = datetime.now().strftime('%Y%m%d_%H%M%S')
# cv2.imwrite(f'C:/Users/1101_python/Pictures/Saved Pictures/akaze{now}.jpg',img3)

# TARGET_FILE = 'female1.jpg'
# IMG_DIR = 'C:/Users/1101_python/Pictures/Saved Pictures/'
# IMG_SIZE = (200, 200)

# target_img_path = f"{IMG_DIR}/{TARGET_FILE}"
# #ターゲット画像をグレースケールで読み出し
# target_img = cv2.imread(target_img_path, cv2.IMREAD_GRAYSCALE)
# #ターゲット画像を200px×200pxに変換
# target_img = cv2.resize(target_img, IMG_SIZE)

# # BFMatcherオブジェクトの生成
# bf = cv2.BFMatcher(cv2.NORM_HAMMING,crossCheck=True)

# # AKAZEを適用、特徴点を検出
# detector = cv2.AKAZE_create()
# (target_kp, target_des) = detector.detectAndCompute(target_img, None)

# print('TARGET_FILE: %s' % (TARGET_FILE))

# # ディレクトリ内の全ファイルを取得
# # DB操作ではファイル名から検索が必要
# good=[]
# files = os.listdir(IMG_DIR)
# for file in files:
#     if file == TARGET_FILE:
#         continue
#     #比較対象の写真の特徴点を検出
#     # 相手ファイルのフルパス
#     comparing_img_path = IMG_DIR + file
#     try:
#         # ファイルをcv2で読み込み
#         comparing_img = cv2.imread(comparing_img_path, cv2.IMREAD_GRAYSCALE)
#         # サイズ変更
#         comparing_img = cv2.resize(comparing_img, IMG_SIZE)
#         # タプル
#         (comparing_kp, comparing_des) = detector.detectAndCompute(comparing_img, None)
#         # BFMatcherで総当たりマッチングを行う
#         matches = bf.match(target_des, comparing_des)
#         #特徴量の距離を出し、平均を取る
#         # # 検出結果を描画する
#         # img3 = cv2.drawMatches(target_img_path, target_kp, comparing_img_path, comparing_kp, matches[:30], None, flags = cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
#         # print(img3)
#         # #検出結果を描画した画像を出力する
#         # now = datetime.now().strftime('%Y%m%d_%H%M%S')
#         # cv2.imwrite(f'C:/Users/1101_python/Pictures/Saved Pictures/akaze{now}.jpg',img3)
#         dist = [m.distance for m in matches]
#         ret = sum(dist) / len(dist)
#     except cv2.error:
#         # cv2がエラーを吐いた場合の処理
#         ret = 100000

#     print('file:',file, 'ret:',ret)

    # plt.imshow(img3)
    # plt.show()

# plt.imshow(img3)
# # 軸の線を消す
# plt.axis("off")
# plt.show()
# print(img3)

# dir_path = 'C:/Users/1101_python/Pictures/Saved Pictures/'
# img_size = (200,200)
# target_img_path = 'C:/Users/1101_python/Pictures/Saved Pictures/female1.jpg'
# # グレースケールにしたほうが濃淡が出てわかりやすいためグレースケールに色を変更
# target_img = cv2.imread(target_img_path, cv2.IMREAD_GRAYSCALE)
# # サイズの変更
# target_img = cv2.resize(target_img, img_size)
# bf = cv2.BFMatcher(cv2.NORM_HAMMING)
# detector = cv2.AKAZE_create()
# (target_kp, target_des) = detector.detectAndCompute(target_img, None)
 
# files = os.listdir(dir_path)
# result = {}
# for file in files:
#     if file == target_img_path:
#         continue
#     img_path = dir_path + file
#     try:
#         img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
#         img = cv2.resize(img, img_size)
#         (kp, des) = detector.detectAndCompute(img, None)
#         matches = bf.match(target_des, des)
#         dist = [m.distance for m in matches]
#         ret = sum(dist) / len(dist)
#         result[file.replace('.png','')] = ret
#     except cv2.error:
#         ret = 999999
 
# for k,v in sorted(result.items(),reverse=True,key=lambda x:x[1]):
#     img = cv2.imread('img/{0}.png'.format(k)) 
#     plt.figure(figsize=(8,8))
#     plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
#     plt.title('{0} : {1:.06}'.format(k , v),fontsize=20)
#     plt.axis("off")
#     plt.show()