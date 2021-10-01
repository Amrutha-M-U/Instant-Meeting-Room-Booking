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
pirA =GPIO.input(13)
pirB =GPIO.input(29)
motion_flag=pirA or pirB
        
if(motion_flag):
    print"motion"
    GPIO.output(18,True)
    GPIO.output(36,False)
else:
    print"No motion"
    GPIO.output(36,True)
    GPIO.output(18,False)
::endTime= datetime.datetime.now()
diff = endTime-startTime
print diff      
   
   
  
     
