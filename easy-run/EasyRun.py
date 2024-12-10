import time
from Motor import *
from gpiozero import DistanceSensor

trigger_pin = 27
echo_pin    = 22
sensor = DistanceSensor(echo=echo_pin, trigger=trigger_pin ,max_distance=3)


class EasyRun:
    # コンストラクタ
    def __init__(self):
        self.PWM = Motor()

    # 走行プログラム
    def run(self):
        self.run_foword()
        time.sleep(2)

    # 距離取得関数
    def get_distance(self):
        distance_cm = sensor.distance * 100
        print ("Obstacle distance is "+str(distance_cm)+"CM")
        return int(distance_cm)

    # 前進
    def run_foword(self):
        self.PWM.setMotorModel(2000, 2000, 2000, 2000)
    
    # 停止
    def stop(self):
        self.PWM.setMotorModel(0,0,0,0)                                                                                                                                                                                             
    
    # 左回転
    def turn_left(self):
        self.PWM.setMotorModel(-1450, -1450, 1450, 1450)
                                                                                                                                                                                                                                                                                                                                                                                                                                             
    # 右回転
    def turn_right(self):
        self.PWM.setMotorModel(1450, 1450, -1450, -1450)

    # 180度回転
    def turn_right(self):
        self.PWM.setMotorModel(1450, 1450, -1450, -1450)
easyrun=EasyRun()              



# Main program logic follows:
if __name__ == '__main__':
    print ('EasyRun Program is starting ... ')
    try:
        easyrun.run()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        #PWM.setMotorModel(0,0,0,0)
        easyrun.PWM.setMotorModel(0,0,0,0)
        print ("\nEnd of program")
                
        
            
        


