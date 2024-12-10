# -*- coding: utf-8 -*-
import glob
import cv2
import image_rec

# 特徴点マッチングに使用する点数
point_num = 10

# 閾値
threathold = 100

# エッジ検出の閾値
min_val = 10
max_val = 50

# テンプレート画像
map_img = cv2.imread("./src/map_arrow.png", 0)
#map_kp, map_des = image_rec.create_vec(map_img)
map_ret, map_thresh_img = cv2.threshold(map_img, threathold, 255, cv2.THRESH_BINARY)
#map_kp, map_des = image_rec.create_vec(map_thresh_img)
map_edge = cv2.Canny(map_thresh_img, min_val, max_val)
map_kp, map_des = image_rec.create_vec(map_edge)

# 入力画像
file_path_list = glob.glob("./src/real_data/*")
query_img_list = []
for file_path in file_path_list:
    query_img = cv2.imread(file_path, 0)
    # query_img_list.append(query_img)
    ret, img_thresh = cv2.threshold(query_img, threathold, 255, cv2.THRESH_BINARY)
    #query_img_list.append(img_thresh)
    query_edge = cv2.Canny(img_thresh, min_val, max_val)
    query_img_list.append(query_edge)


# 入力画像とテンプレート画像のマッチング
for query_img in query_img_list:
    # 最終判定結果格納
    final_result = -1000
    # メインロジック
    query_kp, query_des = image_rec.create_vec(query_img)
    matches = image_rec.knn_match(map_des, query_des)
    good = image_rec.select_good_matches(matches, 0.89)
    is_good = True
    if (len(good) < 1):
        is_good = False
        final_result = -3
        print(f"-3: No Good Point")
    
    if (is_good):
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
        is_related = True
        if (deg_value == None):
            is_related = False
            final_result = -2
            print(f"-2: No Related Point")

        if (is_related):
            # 矢印の向きを判定
            arrow_direction = image_rec.get_arrow_direction(deg_value)
            final_result = arrow_direction
            if arrow_direction == 0:
                print(f"0: Right")
            elif arrow_direction == 1:
                print(f"1: Left")
            else:
                print(f"-1: Other")

    # 目視確認
    str_final_result = ""
    if (final_result == -3):
        str_final_result = "No Good Point"
    elif (final_result == -2):
        str_final_result = "No Related Point"
    elif (final_result == -1):
        str_final_result = "Other"
    elif (final_result == 0):
        str_final_result = "Right"
    elif (final_result == 1):
        str_final_result = "Left"
    else:
        str_final_result = "Error"

    #result_img = cv2.drawMatchesKnn(map_thresh_img, map_kp, query_img, query_kp, good, None, flags=2)
    result_img = cv2.drawMatchesKnn(map_edge, map_kp, query_img, query_kp, good, None, flags=2)
    font = cv2.FONT_HERSHEY_SIMPLEX
    #cv2.putText(result_img,f"{final_result}: {str_final_result}",(10,180),font,1,(0,0,0),2,cv2.LINE_AA)
    cv2.putText(result_img,f"{final_result}: {str_final_result}",(10,180),font,1,(255,255,255),2,cv2.LINE_AA)
    cv2.imshow('result_img', result_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    