#!/usr/bin/env  python2
#Author Phinfinity <rndanish@gmail.com>
#The script only makes a copy of the email, doesn't delete any mails
#For README check http://github.com/phinfinity/movemail 

import getpass,imaplib,time

def default_hosts(s):
    if s=="1":
        return "imap.gmail.com"
    elif s=="2":
        return "students.iiit.ac.in"
    return s

def select_folder(con):
    v = map(lambda l: l.split()[2].decode() ,con.list()[1])
    s = ""
    while True:
        for i in xrange(len(v)):
            print "%d %s" %(i+1,v[i])
        s = raw_input()
        if len(s) != 0 and ((not s.isdigit()) or int(s) <= 0 or int(s) > len(v)):
            print "Error Invalid Selection"
        else:
            break
    folder="INBOX"
    if len(s) == 0 :
        con.select()        
    else:
        folder=v[int(s)-1].strip('"')
        con.select(mailbox=folder)
    return folder

def get_input():
    global src_host,dest_host
    global scon,dcon
    global dfolder
    print "Enter Source Host (1: imap.gmail.com 2:students.iiit.ac.in or enter your own host)"
    src_host=default_hosts(raw_input())
    print "Enter Destination Host (1: imap.gmail.com 2:students.iiit.ac.in or enter your own host)"
    dest_host=default_hosts(raw_input())
    print "Set Source Host: %s\nSet Destination Host: %s\n"%(src_host,dest_host)
    print "User name for %s"%src_host
    suser=raw_input()
    spass=getpass.getpass()
    print "User name for %s"%dest_host
    duser=raw_input()
    dpass=getpass.getpass()

    print "Connecting to %s"%src_host
    scon=imaplib.IMAP4_SSL(src_host)
    print "Connected!"
    scon.login(suser,spass)
    print "Authenticated!"
    print "Select Source Folder to copy from (default INBOX):"
    select_folder(scon)

    print "Connecting to %s"%dest_host
    dcon=imaplib.IMAP4_SSL(dest_host)
    print "Connected!"
    dcon.login(duser,dpass)
    print "Authenticated!"
    print "Select Destination Folder to copy to (default INBOX):"
    dfolder = select_folder(dcon)

def move_messages():
    print "Getting List of Messages in Folder"
    message_list=scon.search(None,'ALL')[1][0].split()
    print "Getting Details of Messages in Folder"
    dat=scon.fetch(','.join(message_list),"(BODY[HEADER.FIELDS (subject)])")[1]
    print "%d Messages in Folder to be moved"%len(message_list)
    subjects={}
    for i in dat:
        if type(i)==tuple:
            subjects[i[0].split()[0]]=i[1].strip()
    cnt=0;
    for i in message_list:
        cnt+=1
        print "Fetching - (%d/%d) %s" %(cnt,len(message_list),subjects[i])
        header_dat=scon.fetch(i,"(BODY[HEADER])")[1][0][1]
        body_dat=scon.fetch(i,"(BODY[TEXT])")[1][0][1]
        print "Appending to %s"%(dest_host)
        dcon.append(dfolder,None,None,header_dat+body_dat)
        #dcon.append('INBOX','',imaplib.Time2Internaldate(time.time()),header_dat+body_dat)
        


if __name__=="__main__":
    get_input()
    move_messages()
    dcon.close()
    scon.close()
