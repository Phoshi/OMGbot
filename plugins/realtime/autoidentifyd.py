# -*- coding: utf-8 -*-
#[11 May 10 11:12] * James * Hi everyone
from plugins import plugin
import globalv
import time
import calendar
import os
import settingsHandler
class pluginClass(plugin):
    def __init_db_tables__(self, name):
        settingsHandler.newTable(name, "nickname")
        settingsHandler.writeSetting(name, "nickname","PY")
        settingsHandler.writeSetting(name, "nickname","Silver_Skree")
    def __init__(self):
        self.users=settingsHandler.readSetting("autoidentifyd","nickname")
        self.users=[x[0] for x in self.users]
        self.giveup={}
    def gettype(self):
        return "realtime"
    def action(self, complete):
        idMessages=["identified for this nick","a registered nick","a registered nick"]
        if complete.user() in self.users and ".*!"+complete.userMask().split('!')[1] not in [x[0] for x in globalv.miscVars[2]]:
            if complete.user() not in self.giveup.keys():
                    self.giveup[complete.user()]=0
            if self.giveup[complete.user()]<=0:
                self.giveup[complete.user()]=10
                return ["WHOIS "+complete.user()]
            else:
                self.giveup[complete.user()]-=1
        if complete.complete().split()[1]=="JOIN":
            return ["WHOIS %s"%complete.user()]
        if complete.complete().split()[1] in ["330","307"]:
            level=settingsHandler.readSetting("autoidentifyd","level",where="nickname='%s'"%complete.complete()[1:].split(':')[0].split()[-1])
            level="1" if level==[] else level
            if (".*!"+globalv.miscVars[0][complete.complete()[1:].split(':')[0].split()[-1]],level) not in globalv.miscVars[2]:
                globalv.miscVars[2].append((".*!"+globalv.miscVars[0][complete.complete()[1:].split(':')[0].split()[-1]],level))
        elif complete.complete().split()[1]=="353":
            returns=[]
            for name in complete.message().split():
                try:
                    if name[0] in ["@","+",'&']:
                        name=name[1:]
                    if name in self.users:
                        returns.append("WHOIS %s"%name)
                except:
                    print "Autoidentifyd;whois-on-join;%s;"%name
            return returns
        return [""]
    def describe(self, complete):
        msg=complete.message()
        sender=complete[0].split(' ')
        sender=sender[2]
        return ["PRIVMSG $C$ :I am the logging module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :I log your text so I can use it for nefarious means."]
