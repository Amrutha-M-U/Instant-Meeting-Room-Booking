import imaplib
import time
print'1'
msrvr=imaplib.IMAP4_SSL \
       ('imap.gmail.com',993)
print'2'
unm='raspberrypipro5@gmail.com'
pswd='amnpr12345'
email='"neenu.thankachan@rolls-royce.com"'
no_rply_count=0
print 'logging in'
msrvr.login(unm,pswd)
print'done'
stat,cnt=msrvr.select('inbox')
print'in inbox'
rv,dta=msrvr.search(None,'(UNSEEN)','(FROM %s)'%(email))
print dta
while dta[0]=='' and no_rply_count<3 : 
  print'no'
  print no_rply_count
  no_rply_count=no_rply_count+1
  time.sleep(60) #-------------------------------------------------------------------rum timer
  stat,cnt=msrvr.select('inbox')
  rv,dta=msrvr.search(None,'(UNSEEN)','(FROM %s)'%(email))
  print dta
if dta[0]=='' :
  print "No reply"  
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
msrvr.close()
msrvr.logout()
