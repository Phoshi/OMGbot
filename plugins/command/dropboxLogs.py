# -*- coding: utf-8 -*-
from plugins import plugin
import globalv, urllib2,urllib
import time
import os
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        arguments=complete.message().split()
        channel=complete.channel()
        msg=0 
        for argument in arguments:
            if argument.isdigit()==True:
                msg=argument
            if argument[0]=='#':
                channel=argument
        now=time.gmtime()
        year=now[0]
        day=now[7]-int(msg)
        if day<0:
            year-=1
            day+=365
        file="/"+os.path.join("home","py","omg","logs","LogFile - "+channel+"-"+str(year)+"-"+str(day))
        print "Linking",file
        print os.path.exists(file)
        newFile="/home/py/Dropbox/Public/"+file+".txt"
        print newFile
        print os.getcwd()
        if os.path.exists(newFile)==False:
            #os.symlink(file,newFile)
            os.system('ln -s "%s" "%s"' % (file, newFile))
        msg="http://dl.dropbox.com/u/10241580/"+file.replace(' ','%20').replace('#','%23')+".txt"
        return ["PRIVMSG $C$ :"+msg]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !pastebinLogs module. I return a pastebin URL with the logs of today - [msg].","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!pastebinLogs [offset]"]
