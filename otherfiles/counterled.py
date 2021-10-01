import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(7,GPIO.OUT)
while True:
    x = int(input('Enter number'))
    x = x % 4
    if x==1:
            GPIO.output(13,True)
            GPIO.output(11,False)
            GPIO.output(7,False)
            time.sleep(1)
    elif x==2:
            GPIO.output(13,True)
            GPIO.output(11,True)
            GPIO.output(7,False)
            time.sleep(1)

    elif x==3:
            GPIO.output(13,True)
            GPIO.output(11,True)
            GPIO.output(7,True)
            time.sleep(1)

    else:
            GPIO.output(13,False)
            GPIO.output(11,False)
            GPIO.output(7,False)
            time.sleep(1)
