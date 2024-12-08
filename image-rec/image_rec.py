# -*- coding: utf-8 -*-
import cv2
import math

# ORB特徴点検出器を作る
extractor = cv2.ORB_create()

# Brute-Force Matcher生成
bf = cv2.BFMatcher()

# 特徴ベクトル抽出
def create_vec(img):
    kp, des = extractor.detectAndCompute(img, None)
    return kp, des

# KNNマッチング
def knn_match(des1, des2):
    matches = bf.knnMatch(des1, des2, k=2)
    return matches

# 閾値でマッチング選別
def select_good_matches(matches, ratio=0.5):
    good = []
    for m, n in matches:
        if m.distance < ratio * n.distance:
            good.append([m])
    return good

# 距離と角度を計算
def calcurate_len_deg(kp, i, j):
    x1, y1 = kp[i].pt
    x2, y2 = kp[j].pt
    deg = math.atan2(y2 - y1, x2 - x1) * 180 / math.pi
    len = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return len, deg