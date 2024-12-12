import time
from Motor import Motor
from PCA9685 import PCA9685
from Gyro import Gyro
import signal

PWM = Motor()

class Move_ex:
    gyro = Gyro()
    theta = 0.0

    # コンストラクタ
    def __init__(self):
        self.gyro.set_up()

    # ハンドラ
    def signal_handler(self, arg1, arg2):
        print(f"theta = {self.theta}")
        dtheta = self.gyro.get_true_wz() * 0.001
        self.theta += dtheta
        #if (self.theta > 90.0):
        #    exit(0)
        
    # 右回転
    def turn_right(self):
        self.theta = 0.0 
        # センサスタート
        self.gyro.start()

        signal.signal(signal.SIGALRM, self.signal_handler)
        # インターバルタイマ
        signal.setitimer(signal.ITIMER_REAL, 0.0, 0.0005)

        
        PWM.setMotorModel(-1450, -1450, 1450, 1450)
        while self.theta < 90.0:
            time.sleep(0.0005)
        
        # ここに来たら、積算角度が90度以上
        PWM.setMotorModel(0,0,0,0)

        # センサ停止
        self.gyro.stop()

        return


    # 右回転
    def turn_left(self):
        self.theta = 0.0 
        # センサスタート
        self.gyro.start()

        signal.signal(signal.SIGALRM, self.signal_handler)
        PWM.setMotorModel(1450, 1450, -1450, -1450)
        while self.theta > -90.0:
            time.sleep(0.0005)
        
        # ここに来たら、積算角度が90度以上
        PWM.setMotorModel(0,0,0,0)

        # インターバルタイマ停止
        signal.setitmer(signal.ITIMER_REAL, 0.0, 0.0005)

        # センサ停止
        self.gyro.stop()

        return



    

move = Move_ex()
move.turn_right()


"""
# Main program logic follows:
if __name__ == '__main__':
    print ('EasyRun Program is starting ... ')
    try:
        move.run()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        PWM.setMotorModel(0,0,0,0)
        print ("\nEnd of program")
"""