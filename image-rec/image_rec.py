# -*- coding: utf-8 -*-
import cv2

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
