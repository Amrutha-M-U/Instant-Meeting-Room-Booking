
import smtplib
import RPi.GPIO as GPIO

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MY_ADDRESS = 'raspberrypipro5@gmail.com'
PASSWORD = 'amnpr12345'


def monitor_health():
	
	if GPIO.input(36) and GPIO.input(12):
		LED_FAIL_FLAG = True
	else:
		LED_FAIL_FLAG= False

	if LED_FAIL_FLAG:
		FAIL_INDICATION_FLAG = True
	else:
		FAIL_INDICATION_FLAG = False

	notify_pi_admin(FAIL_INDICATION_FLAG)


def notify_pi_admin(FAIL_INDICATION_FLAG):

	if FAIL_INDICATION_FLAG:
		mail()
		GPIO.output(36, False)
		GPIO.output(12, False)
			
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
    print'1'
    # set up the SMTP server
    s = smtplib.SMTP('smtp.gmail.com:587')
    print'2'
    s.starttls()
    print'login'
    s.login(MY_ADDRESS, PASSWORD)
    print'done'
    # For each contact, send the email:
    name = 'Raghu Srivatsa M P'
    email = 'raghu.srivatsa@rolls-royce.com'
    msg = MIMEMultipart()       # create a message

    # add in the actual person name to the message template
    message = message_template.substitute(PERSON_NAME=name.title())
    print'hi'
    # Prints out the message body for our sake
    print(message)

    # setup the parameters of the message
    msg['From']=MY_ADDRESS
    msg['To']=email
    msg['Subject']="Meeting Room Booking Alert"
    
    # add in the message body
    msg.attach(MIMEText(message, 'plain'))
    print'generated'
    # send the message via the server set up earlier.
    s.sendmail(MY_ADDRESS,[email],msg.as_string())
    print'sent'
    del msg
        
    # Terminate the SMTP session and close the connection
    s.quit()

def main():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(12,GPIO.OUT)
    GPIO.setup(36,GPIO.OUT)
    GPIO.output(12,True)
    GPIO.output(36,True)
    monitor_health()
    
if __name__ == '__main__':
    main()


















		
