from picamera import PiCamera
from time import sleep
camera = PiCamera()
camera.start_preview()
for i in range(3):
    sleep(3)
    camera.capture('/home/pi/Desktop/images/imageB%s.jpg' % i)
camera.stop_preview()

