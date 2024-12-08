# -*- coding: utf-8 -*-
import cv2
import math
import numpy as np

# ORB特徴点検出器を作る
#extractor = cv2.ORB_create()
extractor = cv2.AKAZE_create()

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
    vec = np.array(kp[i].pt) - np.array(kp[j].pt)
    deg = np.arctan2(vec[1], vec[0])
    len = np.linalg.norm(vec)
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
            deg_value = np.rad2deg(m_deg - q_deg)
            
            print(f"m_deg = {m_deg}, q_deg = {q_deg}")
            print(f"deg_value = {deg_value}")
            if deg_value < 0:
                deg_value += 360
            if m_len <= 0:
                continue
            scale = m_len/q_len
            # 結果を行列に格納
            deg_cand[i][j] = deg_value
            deg_cand[j][i] = deg_value
            len_cand[i][j] = scale
            len_cand[j][i] = scale
    
    return len_cand, deg_cand

# 最も多く相対関係が一致する2点を選択
# それはないだろ的な2点を経験則で排除する
# ある点iについて，j, kとの相対関係が一致するかを各jについて調べる
def select_related_points(len_cand, deg_cand, point_num = 2):
    cand_count = np.zeros((point_num, point_num))
    size_range_min = 0.5  # 明らかに違う比率の結果を弾く重要パラメータ
    size_range_max = 2.0  # 明らかに違う比率の結果を弾く重要パラメータ
    dif_range = 1.0  # 重要パラメータ

    print(f"len_cand = {len_cand}")
    print(f"deg_cand = {deg_cand}")

    for i in range(len(deg_cand)):
        for j in range(len(deg_cand)):
            # 明らかに違う比率の結果を弾く
            if len_cand[i][j] < size_range_min or len_cand[i][j] > size_range_max:
                #print(f"len_cand[i][j] = {len_cand[i][j]}")
                continue

            for k in range(len(deg_cand)):
                # 明らかに違う比率の結果を弾く
                if len_cand[i][k] < size_range_min or len_cand[i][k] > size_range_max:
                    #print(f"len_cand[i][k] = {len_cand[i][k]}")
                    continue

                # 誤差がある範囲以下の値なら同じ値とみなす
                deg_dif = np.abs(deg_cand[i][k] - deg_cand[i][j])
                size_dif = np.abs(len_cand[i][k] - len_cand[i][j])
                print(f"size_dif = {size_dif}, deg_fif = {deg_dif}")
                print(f"len_cand[i][j]*dif_range={len_cand[i][j]*dif_range}, deg_cand[i][j]*dif_range={deg_cand[i][j]*dif_range}")
                if deg_dif <= deg_cand[i][j]*dif_range and size_dif <= len_cand[i][j]*dif_range:
                    cand_count[i][j] += 1
                    print("cand_count")

    # どの2点も同じ相対関係になかった場合
    if np.max(cand_count) < 1:
        print("[error] no matching point pair")
        return None, None, None

    # もっとも多く相対関係が一致する2点を取ってくる
    maxidx = np.unravel_index(np.argmax(cand_count), cand_count.shape)
    deg_value = deg_cand[maxidx]
    size_rate = len_cand[maxidx]

    return deg_value, size_rate, maxidx