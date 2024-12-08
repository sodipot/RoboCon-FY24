# -*- coding: utf-8 -*-
import cv2
import math
import numpy as np

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

# スケールと回転角の行列を計算
def calc_scale_deg_mat(query_kp, map_kp, point_num=2):
    # 点i, jの相対角度と相対長さを格納する配列
    deg_cand = np.zeros((point_num, point_num))  
    len_cand = np.zeros((point_num, point_num))
    # 全ての点のサイズ比，相対角度を求める
    for i in range(point_num):
        for j in range(i+1, point_num):
            # クエリ画像から特徴点間の角度と距離を計算
            q_len, q_deg = calcurate_len_deg(query_kp, i, j)
            # マップ画像から特徴点間の角度と距離を計算
            m_len, m_deg = calcurate_len_deg(map_kp, i, j)
            # 2つの画像の相対角度と距離
            deg_value = q_deg - m_deg
            if deg_value < 0:
                deg_value += 360
            if m_len <= 0:
                continue
            scale = q_len/m_len
            # 結果を行列に格納
            deg_cand[i][j] = deg_value
            deg_cand[j][i] = deg_value
            len_cand[i][j] = scale
            len_cand[j][i] = scale
    
    return len_cand, deg_cand