import smtplib
import imaplib
import datetime
import time
import RPi.GPIO as GPIO

from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(13,GPIO.IN)
GPIO.setup(29,GPIO.IN)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(36,GPIO.OUT)
GPIO.output(36,False)
GPIO.output(18,False)

MY_ADDRESS = 'raspberrypipro5@gmail.com'
PASSWORD = 'amnpr12345'
admin = 'neenu.thankachan@rolls-royce.com' 
hour_hand = 9
i = 3
booking_data=[[0,5,20,25,40],[5,20,25,40,55],['B','U','U','B','B'],['Maria','Neenu','Maria','Maria','Maria'],['maria.mathews@rolls-royce.com','neenu.thankachan@rolls-royce.com','maria.mathews@rolls-royce.com','maria.mathews@rolls-royce.com','maria.mathews@rolls-royce.com']]
case_size = 4 #--------------------------------------len(booking_data[0])
red_led = 0
green_led = 0
motion_count = 0
OK = 0
counter = 0
no_rply_count = 0
reply = -1
warm_up = 1
block_mail_sent = "FALSE"
alert_mail_sent = "FALSE"
admin_flag = "FALSE"
reply_waiting = "TRUE"
min_hand=booking_data[0][i]
startTime= datetime.datetime.now()
start_cnfm= datetime.datetime.now()
start_reply= datetime.datetime.now()
start_ok= datetime.datetime.now()
print "new case : ",booking_data[2][i]

def get_contacts(filename):
    """
    Return two lists names, emails containing names and email addresses
    read from a file specified by filename.
    """
    
    names = []
    emails = []
    with open(filename, mode='r') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails

def read_template(filename):
    """
    Returns a Template object comprising the contents of the 
    file specified by filename.
    """
    
    with open(filename, 'r') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def send_alert(name,email) :
    # set up the SMTP server
    s = smtplib.SMTP('smtp.gmail.com:587')
    #print 'not send yet'
    #print'tmplt'
    message_template = read_template('alert_mail.txt')
    s.starttls()
    print'login'
    s.login(MY_ADDRESS, PASSWORD)
    #print'done'
    msg = MIMEMultipart()       # create a message
    # add in the actual person name to the message template
    message = message_template.substitute(PERSON_NAME=name)
    #print'tmplt done'
    # Prints out the message body for our sake
    #print(message)
    # setup the parameters of the message
    msg['From']=MY_ADDRESS
    msg['To']=email
    msg['Subject']="Booking Alert"
    #print 'msg structure done'
    # add in the message body
    msg.attach(MIMEText(message, 'plain'))
    #print'generated'
    # send the message via the server set up earlier.
    s.sendmail(MY_ADDRESS,[email],msg.as_string())
    print'sent'
    del msg
    # Terminate the SMTP session and close the connection
    s.quit()

def read_reply(name,email) :
    global start_reply
    global no_rply_count
    #print'in  read'
    msrvr=imaplib.IMAP4_SSL \
           ('imap.gmail.com',993)
    #print'gmail '
    print 'logging in'
    msrvr.login(MY_ADDRESS,PASSWORD)
    #print'done'
    stat,cnt=msrvr.select('inbox')
    #print'in inbox'
    rv,dta=msrvr.search(None,'(UNSEEN)','(FROM %s)'%(email))
    end = datetime.datetime.now()
    #print dta
    diff = ((end-start_reply).total_seconds())/60
    if(dta[0]=='' and no_rply_count<3) : 
      print'no'
      #print no_rply_count
      if(diff>=1) :  
          no_rply_count=no_rply_count+1
          start_reply = datetime.datetime.now()
      return -1
    elif(dta[0]=='') :
      print "No reply"
      return 0
    else:
        print'selected'
        ##print no_rply_count
        ids=dta[0]
        id_list=ids.split()
        latest_email_id=id_list[-1]
        rv,dta=msrvr.fetch(latest_email_id,'(UID BODY[TEXT])')
        #stat,dta=msrvr.fetch \
         #         (cnt[0], \
          #         '(UID BODY[TEXT])')
        #print'read'
       # print 'reply : '
        reply=dta[0][1][0]
        print reply[0]
        if (reply[0]=='Y' or reply[0]=='y') :
            return 1
        else:
            return 0
    msrvr.close()
    msrvr.logout()

def unblock_mail():
    # set up the SMTP server
    s = smtplib.SMTP('smtp.gmail.com:587')
    #print 'not send yet'
    #print'tmplt'
    name='Admin'
    message_template = read_template('unblock_mail.txt')
    s.starttls()
    print'login'
    s.login(MY_ADDRESS, PASSWORD)
    #print'done'
    msg = MIMEMultipart()       # create a message
    # add in the actual person name to the message template
    message = message_template.substitute(Admin=name)
    #print'tmplt done'
    # Prints out the message body for our sake
    #print(message)
    # setup the parameters of the message
    msg['From']=MY_ADDRESS
    msg['To']=admin
    msg['Subject']="Unblock Request"
    #print 'msg structure done'
    # add in the message body
    msg.attach(MIMEText(message, 'plain'))
    #print'generated'
    # send the message via the server set up earlier.
    s.sendmail(MY_ADDRESS,[admin],msg.as_string())
    print'sent'
    del msg
    # Terminate the SMTP session and close the connection
    s.quit()

def block_mail():
    # set up the SMTP server
    s = smtplib.SMTP('smtp.gmail.com:587')
    #print 'not send yet'
    #print'tmplt'
    name='Admin'
    message_template = read_template('block_mail.txt')
    s.starttls()
    print'login'
    s.login(MY_ADDRESS, PASSWORD)
    #print'done'
    msg = MIMEMultipart()       # create a message
    # add in the actual person name to the message template
    message = message_template.substitute(Admin=name)
    #print'tmplt done'
    # Prints out the message body for our sake
    #print(message)
    # setup the parameters of the message
    msg['From']=MY_ADDRESS
    msg['To']=admin
    msg['Subject']="Block Request"
    #print 'msg structure done'
    # add in the message body
    msg.attach(MIMEText(message, 'plain'))
    #print'generated'
    # send the message via the server set up earlier.
    s.sendmail(MY_ADDRESS,[admin],msg.as_string())
    print'sent'
    del msg
    # Terminate the SMTP session and close the connection
    s.quit()
    
def confirm_timer(led):
    global min_hand
    global counter
    global start_cnfm
    end = datetime.datetime.now()
    diff = ((end-start_cnfm).total_seconds())/60
    if(diff>=1) :
        if(led and counter<4) :
            counter=counter+1
            print 'counter-',counter
        min_hand=min_hand+1
        start_cnfm= datetime.datetime.now()
    if(counter==4) :
       # print'confmd'
        return 1
    return 0

def send_mail(i):
    global min_hand
    global counter
    global block_mail_sent
    global alert_mail_sent
    global admin_flag
    global unblocked
    global OK
    global reply
    global reply_waiting
    global start_ok
    global name
    global email
    #print '1'
    #print 'min -',min_hand
    status=booking_data[2][i]
    run_flag = 0
   # print'2'
    if(status=='U') :
        if(status=='U' and not OK  and min_hand<=booking_data[1][i]) :
            #print'3-wanted'
           # print 'red- ',red_led
           # print 'green-',green_led
            if((block_mail_sent=="FALSE") and confirm_timer(red_led)) :
                    #print "admin to blk"
                    block_mail()                    
                    block_mail_sent = "TRUE"
                    admin_flag = "TRUE"
                    unblocked = "FALSE"
                    counter = 0
            elif(admin_flag=="TRUE" and unblocked=="FALSE" and confirm_timer(green_led)) : 
                    #print'sent mail to admin to unblk'
                    unblock_mail()
                    unblocked = "TRUE"
                    status = 'B'
            elif(admin_flag=="FALSE" and green_led) :
                    print 'OK'
                    OK = 1
        elif(OK) :
             end = datetime.datetime.now()
             diff = ((end-start_ok).total_seconds())/60
             if(diff>=1) :
                 min_hand = min_hand+1
                 start_ok = datetime.datetime.now()
                 
    elif(status=='B') : 
        if(status=='B' and not OK and reply_waiting=="TRUE" and min_hand<=booking_data[1][i]) :
            #print'4-unwanted'
            #print'red-',red_led
            #print'green-',green_led
            if(confirm_timer(green_led)) :
                #print'no one'
                if(alert_mail_sent=='FALSE') :
                    #print 'in alert'
                    name=booking_data[3][i]
                    email=booking_data[4][i]
                    send_alert(name,email)
                    alert_mail_sent = "TRUE"
                if(reply==-1) :   
                    reply=read_reply(name,email)
                    #print 'reply return- '
                    #print reply
                if(reply==0) :
                    #print 'send to admin unblk'
                    unblock_mail()
                    reply_waiting = 'FALSE'
                    status = 'U'
                elif(reply==1):
                    reply_waiting = 'FALSE'
            elif(alert_mail_sent=="FALSE" and red_led) :
                  print 'OK'
                  OK = 1
        elif(OK) :
             end = datetime.datetime.now()
             diff = ((end-start_ok).total_seconds())/60
             if(diff>=1) :
                 min_hand = min_hand+1
                 start_ok = datetime.datetime.now()         
        

def glow_led():
    global red_led
    global green_led
    global motion_count
    global startTime
    global warm_up
    pirA =GPIO.input(13)
    pirB =GPIO.input(29)
    #motion_flag=motion_flag or pirA or pirB
    if(pirA or pirB) :
      motion_count = motion_count+1
    endTime= datetime.datetime.now()
    diff = ((endTime-startTime).total_seconds())/60
    if(diff >= 1):
      
          warm_up = 0  
          if(motion_count>=300000):
            print"motion"
            print motion_count
            GPIO.output(18,True)
            GPIO.output(36,False)
            red_led = 1
            green_led = 0
          else:
            print"No motion"
            print motion_count
            GPIO.output(36,True)
            GPIO.output(18,False)
            red_led = 0
            green_led = 1        
          startTime= datetime.datetime.now()
          motion_count = 0

def monitor_health():
	
	if GPIO.input(36) and GPIO.input(18):
		LED_FAIL_FLAG = True
	else:
		LED_FAIL_FLAG= False

	

	notify_pi_admin(LED_FAIL_FLAG)


def notify_pi_admin(FAIL_INDICATION_FLAG):

	if FAIL_INDICATION_FLAG:
		mail()
		GPIO.output(36, False)
		GPIO.output(18, False)
			
	else:
		pass

def read_template(filename):
    """
    Returns a Template object comprising the contents of the 
    file specified by filename.
    """
    
    with open(filename, 'r') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def mail():
    
    message_template = read_template('failure_mail.txt')
    #print'1'
    # set up the SMTP server
    s = smtplib.SMTP('smtp.gmail.com:587')
    #print'2'
    s.starttls()
    #print'login'
    s.login(MY_ADDRESS, PASSWORD)
    #print'done'
    # For each contact, send the email:
    name = 'Raghu Srivatsa M P'
    email = 'raghu.srivatsa@rolls-royce.com'
    msg = MIMEMultipart()       # create a message

    # add in the actual person name to the message template
    message = message_template.substitute(PERSON_NAME=name.title())
    #print'hi'
    # Prints out the message body for our sake
    #print(message)

    # setup the parameters of the message
    msg['From']=MY_ADDRESS
    msg['To']=email
    msg['Subject']="Meeting Room Booking Alert"
    
    # add in the message body
    msg.attach(MIMEText(message, 'plain'))
    #print'generated'
    # send the message via the server set up earlier.
    s.sendmail(MY_ADDRESS,[email],msg.as_string())
    #print'sent'
    del msg
        
    # Terminate the SMTP session and close the connection
    s.quit()
      
def main():
    global i
    global min_hand
    global counter 
    global block_mail_sent
    global alert_mail_sent
    global admin_flag
    global OK
    time.sleep(30)
    while(warm_up) :
        glow_led()
        monitor_health()
    while(i<case_size) :
       # print 'case-',i
        #print 'glw'
        glow_led()
        #print 'mntr'
        monitor_health()
       # print 'snd'
        send_mail(i)
        if(min_hand==booking_data[1][i]):
            block_mail_sent = "FALSE"
            alert_mail_sent = "FALSE"
            admin_flag = "FALSE"
            reply_waiting = "TRUE"
            OK = 0
            counter = 0
            no_rply_count = 0
            print 'case ',i," completed"
            i = i+1
            #print "new case : ",booking_data[2][i]
            min_hand=booking_data[0][i]
if __name__ == '__main__':
    main()
  
     
