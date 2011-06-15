# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
from userlevelHandler import getLevel
import os
from securityHandler import isAllowed
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def __level__(self):
        return 150
    def action(self, complete):
        msg=complete.message()
        sender=complete.userMask()
        if len(msg.split())>1:
            mode=msg.split()[1].lower()
        else:
            mode="on"
        msg=msg.split()[0]
        print sender
        if isAllowed(sender)>=getLevel(complete.cmd()[0]):
            if mode=="on":
                with open(os.path.join("config","autoloading.txt"),"a") as file:
                    file.write("\n"+msg)
                    return ["PRIVMSG $C$ :Plugin set to autoload, cap'n"]
            else:
                with open(os.path.join("config","autoloading.txt"),"r") as file:
                    lines=file.read().split('\n')
                    print lines
                    lines.remove(msg)
                    with open(os.path.join("config","autoloading.txt"),"w") as file:
                        file.write('\n'.join(lines))
                        return ["PRIVMSG $C$ :Plugin removed from autoloading, cap'n"]
            if msg=="list":
                pluginList=[]
                for line in open(os.path.join("config","autoloading.txt")):
                    pluginList.append(line.strip())
                    msg="Autoloading plugins: "+', '.join(pluginList)
                    return ["PRIVMSG $C$ :"+msg]
            return ["PRIVMSG $C$ :You do not have the required access rights!"]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !autoload module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!autoload [plugin] [on/off]"]
