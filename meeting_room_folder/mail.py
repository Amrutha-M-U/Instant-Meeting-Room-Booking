import smtplib
import imaplib
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(16,GPIO.IN)
GPIO.setup(18,GPIO.IN)

from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MY_ADDRESS = 'raspberrypipro5@gmail.com'
PASSWORD = 'amnpr12345'
hour_hand=9
min_hand=0 
i=4 #-----------------------------------------------------------------------------------------------------------0
booking_data=[[0,10,20,30,40],[10,20,30,40,50],['B','U','U','B','B'],['Maria','Neenu','Maria','Neenu','Neenu'],['maria.mathews@rolls-royce.com','neenu.thankachan@rolls-royce.com','maria.mathews@rolls-royce.com','neenu.thankachan@rolls-royce.com','neenu.thankachan@rolls-royce.com']]
admin = 'archana.tripathi@rolls-royce.com' #------------------change
case_size =5 #--------------------------------------------------------------------------------------------len(booking_data[0])
#sample=[[1,0,0,0,0],[0,1,0,0,0],[1,1,0,1,1],[0,0,1,0,0]]
#pirA = 1 #-----------------------------------------------change to sensor data
#pirB = 0 #-----------------------------------------------   "
#red_led = 1 #--------------------------------------------change to led data
#green_led = 0 #-----------------------------------------  "

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
    print 'not send yet'
    print'tmplt'
    message_template = read_template('alert_mail.txt')
    s.starttls()
    print'login'
    s.login(MY_ADDRESS, PASSWORD)
    print'done'
    msg = MIMEMultipart()       # create a message
    # add in the actual person name to the message template
    message = message_template.substitute(PERSON_NAME=name)
    print'tmplt done'
    # Prints out the message body for our sake
    print(message)
    # setup the parameters of the message
    msg['From']=MY_ADDRESS
    msg['To']=email
    msg['Subject']="Booking Alert"
    print 'msg structure done'
    # add in the message body
    msg.attach(MIMEText(message, 'plain'))
    print'generated'
    # send the message via the server set up earlier.
    s.sendmail(MY_ADDRESS,[email],msg.as_string())
    print'sent'
    del msg
    # Terminate the SMTP session and close the connection
    s.quit()

def read_reply(name,email) :
    print'in  read'
    msrvr=imaplib.IMAP4_SSL \
           ('imap.gmail.com',993)
    print'gmail '
    no_rply_count=0
    print 'logging in'
    msrvr.login(MY_ADDRESS,PASSWORD)
    print'done'
    stat,cnt=msrvr.select('inbox')
    print'in inbox'
    rv,dta=msrvr.search(None,'(UNSEEN)','(FROM %s)'%(email))
    print dta
    while dta[0]=='' and no_rply_count<3 : 
      print'no'
      print no_rply_count
      no_rply_count=no_rply_count+1
      run_timer(min_hand)
      stat,cnt=msrvr.select('inbox')
      rv,dta=msrvr.search(None,'(UNSEEN)','(FROM %s)'%(email))
      print dta
    if dta[0]=='' :
      print "No reply"
      return 0
    else:
        print'selected'
        print no_rply_count
        ids=dta[0]
        id_list=ids.split()
        latest_email_id=id_list[-1]
        rv,dta=msrvr.fetch(latest_email_id,'(UID BODY[TEXT])')
        #stat,dta=msrvr.fetch \
         #         (cnt[0], \
          #         '(UID BODY[TEXT])')
        print'read'
        print 'reply : '
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
    print 'not send yet'
    print'tmplt'
    name='Admin'
    message_template = read_template('unblock_mail.txt')
    s.starttls()
    print'login'
    s.login(MY_ADDRESS, PASSWORD)
    print'done'
    msg = MIMEMultipart()       # create a message
    # add in the actual person name to the message template
    message = message_template.substitute(Admin=name)
    print'tmplt done'
    # Prints out the message body for our sake
    #print(message)
    # setup the parameters of the message
    msg['From']=MY_ADDRESS
    msg['To']=admin
    msg['Subject']="Unblock Request"
    print 'msg structure done'
    # add in the message body
    msg.attach(MIMEText(message, 'plain'))
    print'generated'
    # send the message via the server set up earlier.
    s.sendmail(MY_ADDRESS,[admin],msg.as_string())
    print'sent'
    del msg
    # Terminate the SMTP session and close the connection
    s.quit()

def block_mail():
    # set up the SMTP server
    s = smtplib.SMTP('smtp.gmail.com:587')
    print 'not send yet'
    print'tmplt'
    name='Admin'
    message_template = read_template('block_mail.txt')
    s.starttls()
    print'login'
    s.login(MY_ADDRESS, PASSWORD)
    print'done'
    msg = MIMEMultipart()       # create a message
    # add in the actual person name to the message template
    message = message_template.substitute(Admin=name)
    print'tmplt done'
    # Prints out the message body for our sake
    #print(message)
    # setup the parameters of the message
    msg['From']=MY_ADDRESS
    msg['To']=admin
    msg['Subject']="Block Request"
    print 'msg structure done'
    # add in the message body
    msg.attach(MIMEText(message, 'plain'))
    print'generated'
    # send the message via the server set up earlier.
    s.sendmail(MY_ADDRESS,[admin],msg.as_string())
    print'sent'
    del msg
    # Terminate the SMTP session and close the connection
    s.quit()
    
def confirm_timer(led):
    global min_hand
    global counter
    if(led and counter<2) : #--------------------------------------------------------5
        counter=counter+1
        print 'counter-',counter
        min_hand=min_hand+1
    time.sleep(60)
    if(counter==2) : #-------------------------------------------------------------5
        print'confmd'
        return 1
    global run_flag
    run_flag=1
    return 0

def run_timer(min_hand):
    time.sleep(60)
    min_hand=min_hand+1

def get_green_led() :
    print GPIO.input(16)
    return GPIO.input(16)

def get_red_led() :
    print GPIO.input(18)
    return GPIO.input(18)


def main():
    global i
    global min_hand
    global counter
    while(i<case_size) :
        print '1'
        min_hand=booking_data[0][i]
        print 'min -%d',min_hand
        #pirA = sample[0][i]
        #pirB = sample[1][i]
        #red_led = sample[2][i]
        #green_led=sample[3][i]
        status=booking_data[2][i]
        block_mail_sent = "FALSE"
        alert_mail_sent = "FALSE"
        admin_flag = "FALSE"
        OK = 0
        counter=0
        global run_flag
        run_flag = 0
        print'2'
        if(status=='U') :
            while (status=='U' and not OK  and min_hand<=booking_data[1][i]) :
                print'3-wanted'
                run_flag = 0
                red_led = get_red_led()
                print 'red- ',red_led
                green_led = get_green_led()
                print 'green-',green_led
                if(red_led and (block_mail_sent=="FALSE") and confirm_timer(red_led)) :
                        print "admin to blk"
                        block_mail()                    
                        block_mail_sent = "TRUE"
                        admin_flag = "TRUE"
                        unblocked = "FALSE"
                        counter = 0
                elif(admin_flag=="TRUE" and unblocked=="FALSE" and confirm_timer(green_led)) : #---------------------
                        print'sent mail to admin to unblk'
                        unblock_mail()
                        unblocked = "TRUE"
                        status = 'B'
                elif(not run_flag) :
                    print'ok'
                    run_timer(min_hand)
                    OK=1
        else :
            while(status=='B' and not OK and alert_mail_sent=="FALSE" and min_hand<=booking_data[1][i]) :
                print'4-unwanted'
                red_led = get_red_led()
                print'red-',red_led
                green_led = get_green_led()
                print'green-',green_led       
                run_flag = 0
                if(green_led and confirm_timer(green_led)) :
                    print'no one'
                    if(alert_mail_sent=='FALSE') :
                        print 'in alert'
                        name=booking_data[3][i]
                        email=booking_data[4][i]
                        send_alert(name,email)                    
                        reply=read_reply(name,email)
                        print 'reply return- '
                        print reply
                        alert_mail_sent = "TRUE"
                    if(not reply) :
                        print 'send to admin unblk'
                        unblock_mail()
                        status = 'U'
                elif(not run_flag) :
                    run_timer(min_hand)
                    OK = 1
                    
        i=i+1
        print 'i++'
        print i    
if __name__ == '__main__':
    main()
