import time
import os
import image_rec
from picamera2 import Picamera2


class Solver1:
    img_file_path = os.path.abspath(f"./capture_image.jpg")
    picam2 = Picamera2()

    def __init__(self):
        self.picam2.start()

    def __del__(self):
        self.picam2.stop()

    def execute(self):
        print("solver1 execute!")
        time.sleep(2)
        print("solver1 end!")
        return
    
    def judge_arroow_direction(self):
        self.picam2.capture_file(self.img_file_path)
        direction = image_rec.get_arrow_direction(self.img_file_path)
        return direction

