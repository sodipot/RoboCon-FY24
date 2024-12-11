import time
import os
import image_rec_lib
from picamera2 import Picamera2
from SensorInstance import sensor
from Move import Move

class Solver1:
    img_file_path = os.path.abspath(f"./capture_image.jpg")
    picam2 = Picamera2()
    car = Move()

    def __init__(self):
        pass

    def __del__(self):
        pass

    def execute(self):
        print("solver1 execute!")
        
        self.sensor = sensor
        isSolved = False

        while not isSolved:
            # ぶつかるまで前進
            self.car.run_foword()

            while self.get_distance() >= 25:
                time.sleep(0.05)
            
            self.car.stop()
            time.sleep(1)

            # 向きをたずねて回転
            direction = self.judge_arrow_direction()
            if direction == 0:
                self.car.turn_right()
                time.sleep(0.8)

            elif direction == 1:
                self.car.turn_left()
                time.sleep(0.8)

            else :
                self.car.turn_right()
                time.sleep(1.5)
        
        print("solver1 end!")
        return

    def get_distance(self):
        distance_cm = self.sensor.distance * 100
        print(str(distance_cm) + "cm")
        return int(distance_cm)

    def judge_arrow_direction(self):
        self.picam2.start()
        self.picam2.capture_file(self.img_file_path)

        direction = image_rec_lib.get_arrow_direction(self.img_file_path)
        self.picam2.stop()

        print("direction is " + str(direction))
        return direction

