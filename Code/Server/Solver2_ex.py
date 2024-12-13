import time
import os
import image_rec_lib
from picamera2 import Picamera2
from gpiozero import DistanceSensor
from Move import Move
from SensorInstance import sensor
car = Move()

class Solver2:
    img_file_path = os.path.abspath(f"./capture_image_color.jpg")
    picam2 = Picamera2()

    def __init__(self):
        pass
    
    def execute(self):
        print("solver2 execute!!")
        
        self.sensor = sensor
        isSolved = False
        toRight = False

        while not isSolved:

            # 距離を測る
            d = self.get_distance()

            # 近い
            if d <= self.NEAR:
                # 一度止まる
                self.car.stop()
                
                # カメラ判定
                color = self.judge_color()
                time.sleep(2)

                if color == 0:
                    # 左へ避けて終了
                    self.avoid_to_left()
                    isSolved = True

                # 右へ
                if toRight:
                    # 壁がなくなるまでみぎへ
                    self.avoid_to_right()

                # 左
                else :
                    # 壁がなくなるまで左へ
                    self.avoid_to_left()

                # よける方向反転
                toRight = not toRight

            # 遠い
            elif (self.NEAR < d) and (d < self.FAR):
                # ちょっと進む
                self.car.run_foword()
                time.sleep(0.1)

            # 外れ値は無視する
            else:
                pass

        car.stop()

        print("solver2 end!")
        return
    
    def get_distance(self):
        distance_cm = self.sensor.distance * 100
        print(str(distance_cm) + "cm")
        return int(distance_cm)
    
    def judge_color(self):
        self.picam2.capture_file(self.img_file_path)
        color = image_rec_lib.get_color(self.img_file_path)
        return color



    #右によける
    def avoid_to_right(self):
        # # ぶつかるまで前進
        # car.run_foword()
        # while self.get_distance() >= 20:
        #     time.sleep(0.1)

        # car.stop()
        # time.sleep(1)

        # 壁がなくなるまで右へ
        car.run_right()
        while self.get_distance() < 30:
            time.sleep(0.1)
        time.sleep(0.5)

        return
    
    # 左によける
    def avoid_to_left(self):
        # # ぶつかるまで前進
        # car.run_foword()
        # while self.get_distance() >= 20:
        #     time.sleep(0.1)

        # car.stop()
        # time.sleep(1)
        
        # 壁がなくなるまで左へ
        car.run_left()
        while self.get_distance() < 30:
            time.sleep(0.1)
        time.sleep(0.5)
        return

