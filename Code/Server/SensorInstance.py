# sensor_instance.py
from gpiozero import DistanceSensor

# センサーのインスタンスを作成
trigger_pin = 27
echo_pin    = 22
sensor = DistanceSensor(echo=echo_pin, trigger=trigger_pin, max_distance=3)
