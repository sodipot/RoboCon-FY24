# -*- coding: utf-8 -*-
import cv2

# 画像１
img1 = cv2.imread("../src/templete_arrow.png", 0)
# 画像２
img2 = cv2.imread("../src/right_img.png", 0)
#img2 = cv2.imread("../src/left_img.png", 0)
#img2 = cv2.imread("../src/up_img.png", 0)
#img2 = cv2.imread("../src/down_img.png", 0)

# A-KAZE検出器の生成
akaze = cv2.AKAZE_create()                                

# 特徴量の検出と特徴量ベクトルの計算
kp1, des1 = akaze.detectAndCompute(img1, None)
kp2, des2 = akaze.detectAndCompute(img2, None)


# Brute-Force Matcher生成
bf = cv2.BFMatcher()
# 特徴量ベクトル同士をBrute-Force＆KNNでマッチング
matches = bf.knnMatch(des1, des2, k=2)


print(len(matches))

# データを間引きする
ratio = 0.8
good = []
for m, n in matches:
    if m.distance < ratio * n.distance:
        good.append([m])

# 対応する特徴点同士を描画
img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, None, flags=2)

# 画像表示
cv2.imshow('img', img3)

# キー押下で終了
cv2.waitKey(0)
cv2.destroyAllWindows()
