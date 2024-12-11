from picamera2 import Picamera2
picam2 = Picamera2()

# こいつはデフォだがバグる
# picam2.start_and_capture_file("image.jpg")

picam2.start()

picam2.capture_file("capture_image.jpg")

picam2.stop()