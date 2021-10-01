import RPi.GPIO as GPIO
import time
ls = [True, False, False]
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.OUT)
GPIO.setup(36,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
while True:
    
        
    GPIO.output(7,True)
    GPIO.output(36,False)
    GPIO.output(11,False)

    time.sleep(.25)
    GPIO.output(7,False)
    GPIO.output(36,True)
    GPIO.output(11,False)

    time.sleep(0.25)
    GPIO.output(7,False)
    GPIO.output(36,False)
    GPIO.output(11,True)

    time.sleep(0.25)

 
