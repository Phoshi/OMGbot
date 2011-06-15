# -*- coding: utf-8 -*-
#[11 May 10 11:12] * James * Hi everyone
from plugins import plugin
import globalv
import time
import calendar
import os
import settingsHandler
class pluginClass(plugin):
    def gettype(self):
        return "realtime"
    def __init_db_tables__(self, name):
        settingsHandler.newTable("logd","ignore")
    def action(self, arguments):

        ignores=[x[0].lower() for x in settingsHandler.readSettingRaw("logd","ignore")]
        if arguments.channel().lower() in ignores or arguments.user().lower() in ignores:
            print "Channel or User Ignored"
            return [""]
        complete=arguments.complete()[1:].split(':',1)
        if len(complete)>1:
            msg=complete[1]
        else:
            msg=""
            if len(complete[0].split())<2:
                print "Message Not Long Enough, exiting"
                return [""]
        try:
            sender=complete[0].split(' ')
            channel=arguments.channel()
            userMask=arguments.userMask()
            user=arguments.user()
            msgType=sender[1]
            ttime=time.gmtime()
            if msgType=="JOIN":
                channel=msg
            message=""
            if os.path.exists(os.path.join("logs","LogFile - "+channel+"-"+str(ttime[0]) + "-" + str(ttime[7]))):
                file=open(os.path.join("logs","LogFile - "+channel.lower()+"-"+str(ttime[0]) + "-" + str(ttime[7])),"a")
            else:
                file=open(os.path.join("logs","LogFile - "+channel.lower()+"-"+str(ttime[0]) + "-" + str(ttime[7])),"w")
            if msgType=="PRIVMSG":
                if msg.split()[0]=="ACTION":
                    msg=' '.join(msg.split()[1:])[:-1]
                else:
                    msg="* "+msg
                message="[%(time)s] * %(user)s %(umessage)s" % {"time":time.strftime("%d %b %y %H:%M"), "user":user,"umessage":msg}
            if msgType=="JOIN":
                message="[%(time)s] > %(user)s has joined" % {"time":time.strftime("%d %b %y %H:%M"), "user":userMask}
            if msgType=="PART":
                message="[%(time)s] < %(user)s has left" % {"time":time.strftime("%d %b %y %H:%M"), "user":userMask}
            if message!="":
                file.write(message+"\n")
            file.close()
            """if msgType=="QUIT":
                for channel in globalv.channels:
                    if os.path.exists(os.path.join("logs","LogFile - "+channel+"-"+str(ttime[0]) + "-" + str(ttime[7]))):
                        file=open(os.path.join("logs","LogFile - "+channel+"-"+str(ttime[0]) + "-" + str(ttime[7])),"a")
                    else:
                        file=open(os.path.join("logs","LogFile - "+channel+"-"+str(ttime[0]) + "-" + str(ttime[7])),"w")
                    message="[%(time)s] < %(user)s has quit: %(reason)s" % {"time":time.strftime("%d %b %y %H:%M"), "user":userMask,"reason":msg}
                    file.write(message+"\n")
                    file.close()"""
        except Exception as detail:
            print "Log failure: %s"%detail
        return [""]
    def describe(self, complete):
        msg=complete.message()
        sender=complete[0].split(' ')
        sender=sender[2]
        return ["PRIVMSG $C$ :I am the logging module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :I log your text so I can use it for nefarious means."]
