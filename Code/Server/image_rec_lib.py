import cv2
import numpy as np
import math

# 閾値
threathold = 40

def get_arrow_direction(file_path):
    # 入力画像の前処理
    query_img = cv2.imread(file_path, 0)
    query_img = query_img[120:270, :]
    query_ret, query_img = cv2.threshold(query_img, threathold, 255, cv2.THRESH_BINARY)
    query_img = 255 - query_img

    # 輪郭を検出
    contours, _ = cv2.findContours(query_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if (contours < 1):
        return -1
    # 最大輪郭を選択
    largest_contour = max(contours, key=cv2.contourArea)
    # 輪郭を近似
    epsilon_ratio=0.01
    epsilon = epsilon_ratio * cv2.arcLength(largest_contour, True)
    approx_contour = cv2.approxPolyDP(largest_contour, epsilon, True)
    # 重心を計算
    moments = cv2.moments(approx_contour)
    if (moments['m00'] == 0):
        return -1
    centroid_x = int(moments['m10'] / moments['m00'])
    centroid_y = int(moments['m01'] / moments['m00'])
    centroid = np.array([centroid_x, centroid_y])
    # 凸包の輪郭を取得
    hull = cv2.convexHull(approx_contour)
    hull_points = hull[:, 0, :]
    # 凸包の重心を計算
    hull_centroid = np.mean(hull_points, axis=0).astype(int)

    # ベクトル計算（矢印の重心 - 凸包の重心）
    vector = centroid - hull_centroid

    # 画像データはY座標が下に行くと正になるので、Y座標を反転して角度を計算
    angle = math.atan2(-vector[1], vector[0])  # Y座標を反転
    angle_degrees = math.degrees(angle)

    # 角度を 0°～360° に変換
    if angle_degrees < 0:
        angle_degrees += 360

    print(f"angle_degrees={angle_degrees}")

    if (0 <= angle_degrees and angle_degrees <= 10):
        return 0
    elif (350 <= angle_degrees):
        return 0
    elif (170 <= angle_degrees and angle_degrees <= 190):
        return 1
    else:
        return -1