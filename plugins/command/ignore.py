# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import re
import securityHandler
import settingsHandler
from userlevelHandler import getLevel
import os
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def __level__(self):
        return 50
    def action(self, complete):
        msg=complete.message()
        nick=complete.userMask()
        amsg=msg
        nickname="*Unknown*"
        if securityHandler.isAllowed(nick)>=getLevel(complete.cmd()[0]):
            if msg[0]=="#":
                nmsg = msg
                nickname=""
            elif msg in globalv.miscVars[0]:
                nmsg=".*@"+globalv.miscVars[0][msg].split('@')[1]
                nickname=msg
            else:
                nmsg=msg
                nmsg=nmsg.replace('*','.*').replace('..*','.*')
            fullCMD=nmsg
            if fullCMD not in [x[0] for x in settingsHandler.readSettingRaw("coreIgnorance","ignorance")]:
                settingsHandler.writeSetting("coreIgnorance",["ignorance","nickname"],[fullCMD,nickname])
                return ["PRIVMSG $C$ :"+amsg+ " successfully ignored, cap'n!"]
            else:
                return ["PRIVMSG $C$ :"+amsg+" is already ignored, m'lord!"]
        else:
            return ["PRIVMSG $C$ :Go away."]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !ignore module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!ignore [user or regex hostmask pattern]"]
