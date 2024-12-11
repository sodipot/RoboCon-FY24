import time
from gpiozero import DistanceSensor
from Move import Move

trigger_pin = 27
echo_pin    = 22
sensor = DistanceSensor(echo=echo_pin, trigger=trigger_pin ,max_distance=3)
car = Move()

class Solver2:
    def __init__(self):
        pass
    
    def execute(self):
        print("solver2 execute!!")
        
        # 進み順をここで定義する
        self.avoid_to_left()
        self.avoid_to_right()


        print("solver2 end!")
        return
    
    def get_distance(self):
        distance_cm = sensor.distance * 100
        print(str(distance_cm) + "cm")
        return int(distance_cm)
    
    #右によける
    def avoid_to_right(self):
        # ぶつかるまで前進
        car.run_foword()
        while self.get_distance >= 10:
            time.sleep(0.1)
        
        # 壁がなくなるまで右へ
        car.run_right()
        while self.get_distance < 20:
            time.sleep(0.1)

        return
    
    # 左によける
    def avoid_to_left(self):
        # ぶつかるまで前進
        car.run_foword()
        while self.get_distance >= 10:
            time.sleep(0.1)
        
        # 壁がなくなるまで左へ
        car.run_left()
        while self.get_distance * 100 < 20:
            time.sleep(0.1)
        return

