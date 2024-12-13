import cv2
import numpy as np
import math

# 閾値
threathold = 40

def get_arrow_direction(file_path):
    # 入力画像の前処理
    query_img = cv2.imread(file_path, 0)
    query_img = query_img[120:, :]
    query_ret, query_img = cv2.threshold(query_img, threathold, 255, cv2.THRESH_BINARY)
    query_img = 255 - query_img

    # 輪郭を検出
    contours, _ = cv2.findContours(query_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if (len(contours) < 1):
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


# BLUE
#BLUE_LOWER = np.array([90,64,0])
BLUE_LOWER = np.array([120,64,0])
BLUE_UPPER = np.array([150,255,255])
# GREEN
GREEN_LOWER = np.array([60,64,0])
GREEN_UPPER = np.array([90,255,255])
# RED
ORENGE_LOWER = np.array([0,64,0])
ORENGE_UPPER = np.array([30,255,255])

# 最大値
MAX_THRETH_PER = 0.05

def get_color(file_path):
    # 入力画像の前処理
    query_img = cv2.imread(file_path)
    #BGR色空間からHSV色空間への変換
    hsv = cv2.cvtColor(query_img, cv2.COLOR_BGR2HSV)
    #色検出しきい値範囲内の色を抽出するマスクを作成
    blue_frame_mask = cv2.inRange(hsv, BLUE_LOWER, BLUE_UPPER)
    green_frame_mask = cv2.inRange(hsv, GREEN_LOWER, GREEN_UPPER)
    orenge_frame_mask = cv2.inRange(hsv, ORENGE_LOWER, ORENGE_UPPER)
    #論理演算で色検出
    blue_count = len(blue_frame_mask[blue_frame_mask > 0])
    green_count = len(green_frame_mask[green_frame_mask > 0])
    orenge_count = len(orenge_frame_mask[orenge_frame_mask > 0])

    color_count = np.array([orenge_count, green_count, blue_count])
    print(f"color_count = {color_count}")
    max_color_count = np.max(color_count)
    if (max_color_count > query_img.shape[0]*query_img.shape[1]*MAX_THRETH_PER):
        max_color_index = np.argmax(color_count)
        return max_color_index
    
    return -1

"""
result_none = get_color(f"./capture_image.jpg")
result_red = get_color(f"./red.jpg")
result_green = get_color(f"./green.jpg")
result_blue = get_color(f"./blue.jpg")
print(f"result_none = {result_none}")
print(f"result_red = {result_red}")
print(f"result_green = {result_green}")
print(f"result_blue = {result_blue}")
"""