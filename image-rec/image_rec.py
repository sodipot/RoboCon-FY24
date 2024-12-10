# -*- coding: utf-8 -*-
import cv2
import numpy as np

# 各種経験則パラメータ
# テストデータ用
"""
size_range_min = 0.9  # 明らかに違う比率の結果を弾く重要パラメータ
size_range_max = 1.1  # 明らかに違う比率の結果を弾く重要パラメータ
dif_range = 0.05  # 重要パラメータ
"""

# 実データ用
size_range_min = 0.5  # 明らかに違う比率の結果を弾く重要パラメータ
size_range_max = 2.0  # 明らかに違う比率の結果を弾く重要パラメータ
dif_range = 0.05  # 重要パラメータ

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
def select_good_matches(matches, ratio=0.1):
    good = []
    for m, n in matches:
        if m.distance < ratio * n.distance:
            good.append([m])
    return good

# 対応するマップとクエリの特徴点インデックスを取得
def get_map_query_idx(matches):
    map_idx_list = []
    query_idx_list = []
    for match in matches:
        query_idx_list.append(match[0].trainIdx)
        map_idx_list.append(match[0].queryIdx)
    return map_idx_list, query_idx_list

# 距離と角度を計算
def calcurate_len_deg(kp, i, j):
    vec = np.array(kp[i].pt) - np.array(kp[j].pt)
    deg = np.arctan2(vec[1], vec[0])
    len = np.linalg.norm(vec)
    return len, deg

# スケールと回転角の行列を計算
def calc_scale_deg_mat(query_kp, map_kp):
    point_num = len(map_kp)
    # 点i, jの相対角度と相対長さを格納する配列
    deg_cand = np.zeros((point_num, point_num))  
    len_cand = np.zeros((point_num, point_num))
    # 全ての点のサイズ比，相対角度を求める
    for i in range(point_num):
        for j in range(i+1, point_num):
            # マップ画像から特徴点間の角度と距離を計算
            m_len, m_deg = calcurate_len_deg(map_kp, i, j)
            # クエリ画像から特徴点間の角度と距離を計算
            q_len, q_deg = calcurate_len_deg(query_kp, i, j)
            # 2つの画像の相対角度と距離
            deg_value = np.rad2deg(q_deg - m_deg)
            
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

# 最も多く相対関係が一致する2点を選択
# それはないだろ的な2点を経験則で排除する
# ある点iについて，j, kとの相対関係が一致するかを各jについて調べる
def select_related_points(len_cand, deg_cand):
    point_num = len(len_cand[0])
    cand_count = np.zeros((point_num, point_num))

    # スケール・回転角行列
    # print(f"len_cand = {len_cand}")
    # print(f"deg_cand = {deg_cand}")

    for i in range(len(deg_cand)):
        for j in range(len(deg_cand)):
            # 明らかに違う比率の結果を弾く
            if len_cand[i][j] < size_range_min or len_cand[i][j] > size_range_max:
                continue

            for k in range(len(deg_cand)):
                # 明らかに違う比率の結果を弾く
                if len_cand[i][k] < size_range_min or len_cand[i][k] > size_range_max:
                    continue

                # 誤差がある範囲以下の値なら同じ値とみなす
                deg_dif = np.abs(deg_cand[i][k] - deg_cand[i][j])
                size_dif = np.abs(len_cand[i][k] - len_cand[i][j])
                if deg_dif <= deg_cand[i][j]*dif_range and size_dif <= len_cand[i][j]*dif_range:
                    cand_count[i][j] += 1

    # どの2点も同じ相対関係になかった場合
    if np.max(cand_count) < 1:
        print("[error] no matching point pair")
        return None, None, None

    #print(f"cand_count = {cand_count}")
    # もっとも多く相対関係が一致する2点を取ってくる
    maxidx = np.unravel_index(np.argmax(cand_count), cand_count.shape)
    deg_value = deg_cand[maxidx]
    size_rate = len_cand[maxidx]

    return deg_value, size_rate, maxidx

# 角度から左右を判別
# 0:right, 1: left, -1: others
def get_arrow_direction(deg):
    print(deg)
    """
    # 右向きとして判定
    if (0 <= deg and deg <= 10):
        return 0
    if (350 <= deg and deg <= 360):
        return 0
    # 左向きとして判定
    if (170 <= deg and deg <= 190):
        return 1
    # その他として判定
    return -1
    """
    # 右向きとして判定
    if (0 <= deg and deg <= 10):
        return 0
    if (350 <= deg and deg <= 360):
        return 0
    # 左向きとして判定
    if (170 <= deg and deg <= 190):
        return 1
    # その他として判定
    return -1