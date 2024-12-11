import time
from Motor import *
from PCA9685 import PCA9685

class Move:
    # コンストラクタ
    def __init__(self):
        pass

    # 走行プログラム
    def run(self):
        self.run_foword()
        time.sleep(2)

        self.run_back()
        time.sleep(2)

        self.turn_right()
        time.sleep(2)

        self.turn_left()
        time.sleep(2)

        self.run_right()
        time.sleep(2)

        self.run_left()
        time.sleep(2)

        self.stop()
        time.sleep(2)
        return


    # 前進
    def run_foword(self):
        self.PWM.setMotorModel(2000, 2000, 2000, 2000)
    
    # 右回転
    def turn_right(self):
        self.PWM.setMotorModel(-1450, -1450, 1450, 1450)
                                                                                                                                                                                                                                                                                                                                                                                                                                             
    # 左回転
    def turn_left(self):
        self.PWM.setMotorModel(1450, 1450, -1450, -1450)

    # 後退
    def run_back(self):
        self.PWM.setMotorModel(-800, -800, -800, -800)

    # 停止
    def stop(self):
        self.PWM.setMotorModel(0,0,0,0)
    
    # 右移動
    def run_right(self):
        self.PWM.setMotorModel(-1450, 1450, 1450, -1450)
    
    # 左移動
    def run_left(self):
        self.PWM.setMotorModel(1450, -1450, -1450, 1450)

move = Move()

# Main program logic follows:
if __name__ == '__main__':
    print ('EasyRun Program is starting ... ')
    try:
        move.run()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        move.PWM.setMotorModel(0,0,0,0)
        print ("\nEnd of program")
                
        
            
        

