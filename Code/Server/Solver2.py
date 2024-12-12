import time
from gpiozero import DistanceSensor
from Move import Move
from SensorInstance import sensor
car = Move()

class Solver2:
    def __init__(self):
        pass
    
    def execute(self):
        print("solver2 execute!!")
        
        self.sensor = sensor

        # 進み順をここで定義する
        self.avoid_to_left()
        self.avoid_to_right()
        self.avoid_to_left()
        self.avoid_to_right()
        self.avoid_to_left()
        self.avoid_to_right()
        self.avoid_to_left()
        
        car.stop()

        print("solver2 end!")
        return
    
    def get_distance(self):
        distance_cm = self.sensor.distance * 100
        print(str(distance_cm) + "cm")
        return int(distance_cm)
    
    #右によける
    def avoid_to_right(self):
        # ぶつかるまで前進
        car.run_foword()
        while self.get_distance() >= 20:
            time.sleep(0.1)

        car.stop()
        time.sleep(1)

        # 壁がなくなるまで右へ
        car.run_right()
        while self.get_distance() < 30:
            time.sleep(0.1)
        time.sleep(0.5)

        return
    
    # 左によける
    def avoid_to_left(self):
        # ぶつかるまで前進
        car.run_foword()
        while self.get_distance() >= 20:
            time.sleep(0.1)

        car.stop()
        time.sleep(1)
        
        # 壁がなくなるまで左へ
        car.run_left()
        while self.get_distance() < 30:
            time.sleep(0.1)
        time.sleep(0.5)
        return

