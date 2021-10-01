import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(13,GPIO.IN)
GPIO.setup(29,GPIO.IN)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(36,GPIO.OUT)
GPIO.output(36,False)
GPIO.output(18,False)

while True:
    motion_flag = 0;
    for i in range (0,180):
        pirA =GPIO.input(13)
        pirB =GPIO.input(29)
        motion_flag=motion_flag or pirA or pirB
        time.sleep(1)
    if(motion_flag):
        print"motion"
        GPIO.output(18,True)
        GPIO.output(36,False)
    else:
        print"No motion"
        GPIO.output(36,True)
        GPIO.output(18,False)
     
   
   
  
     
