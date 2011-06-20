# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import settingsHandler
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        msg=complete.message()
        list=settingsHandler.readSettingRaw("coreIgnorance","ignorance,nickname")
        print [x[0] for x in settingsHandler.readSettingRaw("coreIgnorance","ignorance")]
        laters=[]
        print list
        for line in list:
            laters.append(line[0]+((" ("+line[1]+")") if line[1]!="*Unknown*" else ""))
        if len(list)==0:
            laters=["PRIVMSG $C$ :No users ignored, cap'n!"]
        else:
            laters="PRIVMSG $C$ :"+', '.join(laters)
        return laters

    def describe(self, complete):
        msg=complete.message()
        return ["PRIVMSG $C$ :I am the !laterlist module. I list all current laters.","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!laterlist"]
