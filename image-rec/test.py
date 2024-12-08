# -*- coding: utf-8 -*-
import cv2
import image_rec

# 特徴点マッチングに使用する点数
point_num = 5

# テンプレート画像
map_img = cv2.imread("./src/map_arrow.png", 0)
map_kp, map_des = image_rec.create_vec(map_img)

# 入力画像
query_img_list = []
query_img_list.append(cv2.imread("./src/right_arrow.png", 0))
query_img_list.append(cv2.imread("./src/left_arrow.png", 0))

# 入力画像とテンプレート画像のマッチング
for query_img in query_img_list:
    # メインロジック
    query_kp, query_des = image_rec.create_vec(query_img)
    matches = image_rec.knn_match(map_des, query_des)
    #matches = image_rec.knn_match(query_des, map_des)
    good = image_rec.select_good_matches(matches, 0.85)
    # 精度が高かったもののうちスコアが高いものから指定個取り出す
    good = sorted(good, key=lambda x: x[0].distance)
    # goodに対応するmapとqueryを並べ替え
    map_idx_list, query_idx_list = image_rec.get_map_query_idx(good)
    good_map_kp = [map_kp[idx] for idx in map_idx_list]
    good_query_kp = [query_kp[idx] for idx in query_idx_list]

    #print(f"len(query_kp) = {len(query_kp)}")
    #print(f"len(map_kp) = {len(map_kp)}")
    #print(f"len(good) = {len(good)}")

    # 特徴点同士のスケール・回転角行列計算
    #scale_query, deg_query = image_rec.calc_scale_deg_mat(query_kp, map_kp, point_num)
    scale_query, deg_query = image_rec.calc_scale_deg_mat(good_query_kp, good_map_kp)
    # 相対関係が最大のものを取得
    deg_value, scale_value, max_idx = image_rec.select_related_points(scale_query, deg_query)
    print(f"scale_value = {scale_value}")
    print(f"deg_value = {deg_value}")
    print(f"max_idx = {max_idx}")

    # 目視確認
    result_img = cv2.drawMatchesKnn(map_img, map_kp, query_img, query_kp, good, None, flags=2)
    #result_img = cv2.drawMatchesKnn(query_img, query_kp, map_img, map_kp, good, None, flags=2)
    cv2.imshow('result_img', result_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

