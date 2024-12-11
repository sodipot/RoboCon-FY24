# -*- coding: utf-8 -*-
import glob
import cv2
import image_rec

# 特徴点マッチングに使用する点数
point_num = 10

# テンプレート画像
map_img = cv2.imread("./src/map_arrow.png", 0)
#map_kp, map_des = image_rec.create_vec(map_img)
map_ret, map_thresh_img = cv2.threshold(map_img, 50, 255, cv2.THRESH_BINARY)
map_kp, map_des = image_rec.create_vec(map_thresh_img)

def get_arrow_direction(query_img_path):
    # クエリ画像の下処理
    query_img = cv2.imread(query_img_path, 0)
    ret, img_thresh = cv2.threshold(query_img, 50, 255, cv2.THRESH_BINARY)

    # 入力画像とテンプレート画像のマッチング
    query_kp, query_des = image_rec.create_vec(img_thresh)
    matches = image_rec.knn_match(map_des, query_des)
    good = image_rec.select_good_matches(matches, 0.85)
    if (len(good) < 1):
        return -1
    # 精度が高かったもののうちスコアが高いものから指定個取り出す
    good = sorted(good, key=lambda x: x[0].distance)
    # goodに対応するmapとqueryを並べ替え
    map_idx_list, query_idx_list = image_rec.get_map_query_idx(good)
    good_map_kp = [map_kp[idx] for idx in map_idx_list]
    good_query_kp = [query_kp[idx] for idx in query_idx_list]

    # 特徴点同士のスケール・回転角行列計算
    scale_query, deg_query = image_rec.calc_scale_deg_mat(good_query_kp, good_map_kp)
    # 相対関係が最大のものを取得
    deg_value, scale_value, max_idx = image_rec.select_related_points(scale_query, deg_query)
    if (deg_value == None):
        return -1
    
    # 矢印の向きを判定
    arrow_direction = image_rec.get_arrow_direction(deg_value)
    return arrow_direction

