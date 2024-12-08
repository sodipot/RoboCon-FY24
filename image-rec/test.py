# -*- coding: utf-8 -*-
import cv2
import image_rec

# 特徴点マッチングに使用する点数
point_num = 5

# テンプレート画像
query_img = cv2.imread("./src/query_arrow.png", 0)
query_kp, query_des = image_rec.create_vec(query_img)

# 入力画像
input_img_list = []
input_img_list.append(cv2.imread("./src/right_arrow.png", 0))
input_img_list.append(cv2.imread("./src/left_arrow.png", 0))

# 入力画像とテンプレート画像のマッチング
for input_img in input_img_list:
    # メインロジック
    input_kp, input_des = image_rec.create_vec(input_img)
    matches = image_rec.knn_match(query_des, input_des)
    good = image_rec.select_good_matches(matches, 1.0)
    # 精度が高かったもののうちスコアが高いものから指定個取り出す
    good = sorted(good, key=lambda x: x[0].distance)

    # 特徴点同士のスケール・回転角行列計算
    if (len(good) < point_num):
        point_num = len(good)
    scale_map, deg_map = image_rec.calc_scale_deg_mat(query_kp, input_kp, point_num)
    # 相対関係が最大のものを取得
    deg_value, scale_value, max_idx = image_rec.select_related_points(scale_map, deg_map, point_num)
    print(f"scale_value = {scale_value}")
    print(f"deg_value = {deg_value}")
    print(f"max_idx = {max_idx}")

    # 目視確認
    result_img = cv2.drawMatchesKnn(query_img, query_kp, input_img, input_kp, good, None, flags=2)
    cv2.imshow('result_img', result_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

