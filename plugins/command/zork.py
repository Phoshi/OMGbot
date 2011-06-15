# -*- coding: utf-8 -*-
from plugins import plugin
from settingsHandler import readSetting
import globalv
import subprocess
import shlex
import urllib, urllib2
import os
import pexpect
from time import sleep
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def __init__(self):
        init="/home/py/frotz/bin/dfrotz /home/py/frotz/bin/ZORK1.DAT"
        args=shlex.split(init)
        #self.zork=subprocesses.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        self.zork=pexpect.spawn(init)
        self.scrollback=""

    def action(self, complete):
        msg=complete.message()
        if msg=="scrollback":
            data={"paste_code":self.scrollback,"paste_private":1,"paste_expire_date":"1H"}
            data=urllib.urlencode(data)
            req = urllib2.Request("http://pastebin.com/api_public.php", data)
            response = urllib2.urlopen(req)
            msg=response.read()
            return ["PRIVMSG $C$ :%s"%msg]

        else:
            over=False
            self.zork.sendline(msg)
            output=""
            while not over:
                try:
                    self.zork.expect('\r\n',timeout=2)
                    output+="\n"+self.zork.before
                    print output
                except Exception as detail:
                    print detail
                    over=True
            ret=[]
            self.scrollback+=output
            for line in output.split('\n'): # 0 is stdout
                if line!="":
                    ret.append("PRIVMSG $C$ :"+line)
            return ret
    def describe(self, complete):
        msg=complete.message()
        sender=complete[0].split(' ')
        sender=sender[2]
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
