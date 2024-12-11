import time
from Motor import *
from gpiozero import DistanceSensor
from PCA9685 import PCA9685
from Solver1 import Solver1
from Solver2 import Solver2
from Solver3 import Solver3
import smbus


solver1 = Solver1()
solver2 = Solver2()
solver3 = Solver3()

# Main program logic follows:
if __name__ == '__main__':
    print ('UpaRun Program is starting ... ')
    try:
        solver1.execute()
        solver2.execute()
        solver3.execute()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        PWM.setMotorModel(0,0,0,0)
