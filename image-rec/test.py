# -*- coding: utf-8 -*-
import cv2
import image_rec

# テンプレート画像
query_img = cv2.imread("./src/templete_arrow.png", 0)
query_kp, query_des = image_rec.create_vec(query_img)

# 入力画像
input_img_list = []
input_img_list.append(cv2.imread("./src/right_img.png", 0))
input_img_list.append(cv2.imread("./src/left_img.png", 0))
input_img_list.append(cv2.imread("./src/up_img.png", 0))
input_img_list.append(cv2.imread("./src/down_img.png", 0))
input_img_list.append(cv2.imread("./src/drow_img.png", 0))

# 入力画像とテンプレート画像のマッチング
for input_img in input_img_list:
    # メインロジック
    input_kp, input_des = image_rec.create_vec(input_img)
    matches = image_rec.knn_match(query_des, input_des)
    good = image_rec.select_good_matches(matches, 0.2)

    # 特徴点同士のスケール・回転角行列計算
    scale_map, deg_map = image_rec.calc_scale_deg_mat(query_kp, input_kp)
    print(scale_map)
    print(deg_map)

    # 目視確認
    result_img = cv2.drawMatchesKnn(query_img, query_kp, input_img, input_kp, good, None, flags=2)
    cv2.imshow('result_img', result_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

