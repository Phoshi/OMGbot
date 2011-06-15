# -*- coding: utf-8 -*-
from plugins import plugin
from userlevelHandler import getLevel
from securityHandler import isAllowed
import settingsHandler
import globalv
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def __level__(self):
        return 150
    def action(self, complete):
        msg=complete.message()
        if msg.split()[0]=="-list":
           users=settingsHandler.readSetting("autoidentifyd","nickname, level")
           out=[]
           for name,level in users:
               if len(msg.split())==1:
                   out.append(name+":"+str(level))
               elif msg.split()[1].lower()==name.lower():
                   out.append(name+":"+str(level))
           msg=', '.join(out)
        elif len(msg.split())==1:
           users=settingsHandler.readSetting("autoidentifyd","nickname, level")
           for name,level in users:
               if name==msg:
                   return ["PRIVMSG $C$ :%s"%(level)]
           return ["PRIVMSG $C$ :0"]


        elif isAllowed(complete.userMask())>getLevel(complete.cmd()[0]):
            if msg.split()[0] in [x[0] for x in settingsHandler.readSetting("autoidentifyd","nickname")]:
                settingsHandler.updateSetting("autoidentifyd","level",str(msg.split()[1]), where="nickname='%s'"%msg.split()[0])
                msg="Level updated"
                globalv.miscVars[2].append((msg.split()[0], msg.split()[1]))
            else:
                settingsHandler.writeSetting("autoidentifyd",["nickname","level"], [msg.split()[0], msg.split()[1]])
                msg="User Elevated"
                globalv.miscVars[2].append((msg.split()[0], msg.split()[1]))
        else:
            msg="Only elevated users can do this!"
        return ["PRIVMSG $C$ :"+msg]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
