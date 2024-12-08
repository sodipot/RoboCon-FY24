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
    good = image_rec.select_good_matches(matches, 8.5)
    if (len(good) < 1):
        print("[error] no good point")
        continue
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
    
    # 矢印の向きを判定
    arrow_direction = image_rec.get_arrow_direction(deg_value)
    if arrow_direction == 0:
        print(f"0: Right")
    elif arrow_direction == 1:
        print(f"1: Left")
    else:
        print(f"-1: Other")

    # 目視確認
    """
    result_img = cv2.drawMatchesKnn(map_img, map_kp, query_img, query_kp, good, None, flags=2)
    cv2.imshow('result_img', result_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    """
