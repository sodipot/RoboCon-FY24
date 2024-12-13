import time
import os
import image_rec_lib
from picamera2 import Picamera2
from SensorInstance import sensor
from Move import Move
from Move_ex import Move_ex
from ADC import *

class Solver1:
    img_file_path = os.path.abspath(f"./capture_image.jpg")
    picam2 = Picamera2()
    car = Move()
    car_ex = Move_ex()
    adc = Adc()

    # for left lane
    # L_LIGHT_THRESHOLD = 2.86
    # R_LIGHT_THRESHOLD = 2.74

    # for right lane
    L_LIGHT_THRESHOLD = 2.86
    R_LIGHT_THRESHOLD = 2.72

    # 判定に用いる距離
    NEAR = 40.0
    FAR = 300.0

    def __init__(self):
        self.picam2.start()
        #pass

    def __del__(self):
        self.picam2.stop()
        #pass

    def execute(self):
        print("solver1 execute!")
        
        self.sensor = sensor
        isSolved = False
        prev_d_d1 = 1000000
        prev_d_d2 = 1000000
        prev_d_d3 = 1000000
        prev_d_d4 = 1000000

        # 最初にちょっと走る
        self.car.run_foword()
        time.sleep(1)

        while not isSolved:
            
            # 明かるければ迷路クリア済み
            L = self.adc.recvADC(0)
            R = self.adc.recvADC(1)
            print(f'Light: L={L}, R={R}')
            if L >= self.L_LIGHT_THRESHOLD and R >= self.R_LIGHT_THRESHOLD:
                isSolved = True



            # 距離を測る
            d = self.get_distance()

            # 近い
            if d <= self.NEAR:
                # 一度止まって画像処理
                self.car.stop()
                dir = self.judge_arrow_direction()
                time.sleep(2)

                # 右
                if dir == 0: 
                    # ターン
                    self.car_ex.turn_right()
                    time.sleep(1)
                # 左
                elif dir == 1:
                    # ターン
                    self.car_ex.turn_left()
                    time.sleep(1)
                # それ以外
                else:
                    # 少し下がりもう一度画像処理
                    self.car.run_back()
                    time.sleep(0.3)
                    self.car.stop()
                    dir = self.judge_arrow_direction()
                    time.sleep(2)

                    # 下がってもわからないならちょっと曲がっておく
                    if dir == -1:
                        self.car.turn_left()
                        time.sleep(0.25)
            
            # 遠い
            elif (self.NEAR < d) and (d < self.FAR):
                # ちょっと進む
                self.car.run_foword()
                time.sleep(0.1)

            # 外れ値は無視する
            else:
                pass

            # スタック
            if (abs(d - prev_d_d4) <= 0.1):
                print(f'd_diff0:{abs(d-prev_d_d4)}')
                print(f'd_diff1:{d}')
                print(f'd_diff2:{prev_d_d1}')
                print(f'd_diff3:{prev_d_d2}')
                print(f'd_diff4:{prev_d_d3}')
                print(f'd_diff5:{prev_d_d4}')
                # ちょっと曲がる
                self.car.turn_left()
                time.sleep(0.1)



            prev_d_d4 = prev_d_d3
            prev_d_d3 = prev_d_d2
            prev_d_d2 = prev_d_d1
            prev_d_d1 = d
        
        print("solver1 end!")
        return

    def get_distance(self):
        distance_cm = self.sensor.distance * 100
        print(str(distance_cm) + "cm")
        # return int(distance_cm)
        return (distance_cm)

    def judge_arrow_direction(self):
        # self.picam2.start()
        # time.sleep(1)

        self.picam2.capture_file(self.img_file_path)
        direction = image_rec_lib.get_arrow_direction(self.img_file_path)

        # リソースの開放
        # self.picam2.stop()
        # try:
        #     self.picam2.close()  # カメラリソースを解放
        # except RuntimeError as e:
        #     print(f"RuntimeError in __del__: {e}")

        print("direction is " + str(direction))
        return direction

