import cv2
import numpy as np
import math
import glob

# 閾値
threathold = 50

# 入力画像
file_path_list = glob.glob("./src/real_data/*")
query_img_list = []
for file_path in file_path_list:
    query_img = cv2.imread(file_path, 0)
    query_img = query_img[120:270, :]
    for i in range(5):
        query_img = cv2.GaussianBlur(query_img, (5,5), 0.5)
        query_ret, query_img = cv2.threshold(query_img, threathold, 255, cv2.THRESH_BINARY)
    query_img = cv2.Canny(query_img, 50, 100)
    query_img_list.append(query_img)

for query_img in query_img_list:
    # 輪郭を検出
    contours, _ = cv2.findContours(query_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for countour in contours:
        epsilon = 0.02*cv2.arcLength(countour, True)
        approx = cv2.approxPolyDP(countour, epsilon, True)
        print(len(approx))
        if len(approx) in [7,8,9]:
            (x,y), (MA, ma), angle = cv2.fitEllipse(countour)
            print(f"矢印の中心：({x},{y}), 向き：{angle}度")

            str_angle_degrees = ""
            if (0 <= angle and angle <= 10):
                str_angle_degrees = "Right"
            elif (350 <= angle):
                str_angle_degrees = "Right"
            elif (170 <= angle and angle <= 190):
                str_angle_degrees = "Left"
            else:
                str_angle_degrees = "Other"

            # 結果描画
            result_img = cv2.drawContours(query_img, countour, -1, (0,255,0), 3)
            font = cv2.FONT_HERSHEY_SIMPLEX
            #cv2.putText(result_img,f"{final_result}: {str_final_result}",(10,180),font,1,(0,0,0),2,cv2.LINE_AA)
            cv2.putText(result_img,f"{int(angle)}: {str_angle_degrees}",(10,100),font,1,(255,255,255),2,cv2.LINE_AA)
            cv2.imshow('result_img', result_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            break




   