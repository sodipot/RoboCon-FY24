import time
import os
import image_rec_lib
from picamera2 import Picamera2


class Solver1:
    img_file_path = os.path.abspath(f"./capture_image.jpg")
    picam2 = Picamera2()

    def __init__(self):
        pass

    def __del__(self):
        pass

    def execute(self):
        print("solver1 execute!")
        
        self.picam2.start()
        self.judge_arrow_direction()
        self.picam2.stop()

        print("solver1 end!")
        return

    def judge_arrow_direction(self):
        self.picam2.capture_file(self.img_file_path)
        direction = image_rec_lib.get_arrow_direction(self.img_file_path)
        print("direction is " + str(direction))
        return direction

