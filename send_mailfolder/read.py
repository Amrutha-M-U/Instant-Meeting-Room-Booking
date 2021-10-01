import imaplib
print'1'
msrvr=imaplib.IMAP4_SSL \
       ('imap.gmail.com',993)
print'2'
unm='raspberrypipro5@gmail.com'
pswd='amnpr12345'
email='"neenu.thhan@rolls-royce.com"'
dta=None
print'data : '
print dta
print 'logging in'
msrvr.login(unm,pswd)
print'done'
stat,cnt=msrvr.select('inbox')
print cnt
print cnt[0]
print cnt[1]
print cnt[2]
print stat
print'in inbox'
#rv,dta=msrvr.search(None,'(FROM "maria.mathews@rolls-royce.com")')
if msrvr.search(None,'(FROM %s)'%(email)):
 rv,dta=msrvr.search(None,'(FROM %s)'%(email))

print rv
print'data : '
print dta
if dta==None:
  print "No reply"
  exit()
else:
    print'selected'
    ids=dta[0]
    id_list=ids.split()
    latest_email_id=id_list[-1]
    rv,dta=msrvr.fetch(latest_email_id,'(UID BODY[TEXT])')
    num-int(dta[0])
    print'no: ',num
    #stat,dta=msrvr.fetch \
     #         (cnt[0], \
      #         '(UID BODY[TEXT])')
    print'read'
    print 'reply : '
    reply=dta[0][1][0]
    print reply[0]
msrvr.close()
msrvr.logout()
