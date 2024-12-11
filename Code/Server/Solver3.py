import time
from Line_Tracking import Line_Tracking
from Motor import Motor

infrared=Line_Tracking()
PWM=Motor()

class Solver3:
    def __init__(self):
        pass

    def execute(self):
        print("solver3 execute!!")

        # いい感じに黒線に乗るまでの間はゆっくり前進しておく
        while infrared.check_Infrared() == -1:
            PWM.setMotorModel(800,800,800,800)
            time.sleep(0.1)

        # ライントレースのサンプルを呼び出す
        infrared.run()
        print("solver3 end!")
        return


