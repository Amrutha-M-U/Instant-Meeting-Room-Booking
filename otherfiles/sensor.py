import RPi.GPIO as GPIO
import datetime
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(13,GPIO.IN)
GPIO.setup(29,GPIO.IN)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(36,GPIO.OUT)
GPIO.output(36,False)
GPIO.output(18,False)

#time.sleep(30)
startTime= datetime.datetime.now()
#motion_flag = 0
motion_count = 0


pirA =GPIO.input(13)
pirB =GPIO.input(29)
if(pirA or pirB) :
    motion_count = motion_count+1
#motion_flag=motion_flag or pirA or pirB
endTime= datetime.datetime.now()
diff = ((endTime-startTime).total_seconds())/60
if(diff >=1):
  if(motion_count>=300000):
  #  print"motion"
  #  print motion_count
#      print motion_flag
    GPIO.output(18,True)
    GPIO.output(36,False)
  else:
  #  print"No motion"
   # print motion_count
#       print motion_flag
    GPIO.output(36,True)
    GPIO.output(18,False)
  motion_count = 0
endTime2= datetime.datetime.now()
print ((endTime2-startTime).total_seconds())
#   motion_flag = 0
 
   
   
  
     
