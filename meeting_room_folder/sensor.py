import RPi.GPIO as GPIO
import datetime
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(13,GPIO.IN)
GPIO.setup(29,GPIO.IN)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(36,GPIO.OUT)
GPIO.output(36,False)
GPIO.output(18,False)


startTime= datetime.datetime.now()
motion_flag = 0
while True:
    
    
    
    pirA =GPIO.input(13)
    pirB =GPIO.input(29)
    motion_flag=motion_flag or pirA or pirB
    endTime= datetime.datetime.now()
    diff = ((endTime-startTime).total_seconds())/60
    if(diff >=3):
      if(motion_flag):
        print"motion"
        GPIO.output(18,True)
        
        GPIO.output(36,False)
      else:
        print"No motion"
        GPIO.output(36,True)
        GPIO.output(18,False)
      startTime= datetime.datetime.now()
      motion_flag = 0
     
   
   
  
     
