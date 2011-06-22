# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import os
import settingsHandler
import difflib
from securityHandler import isAllowed
from userlevelHandler import getLevel
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def __level__(self):
        return 50
    def action(self, complete):
        msg=complete.message()
        amsg=msg
        if isAllowed(complete.userMask())<getLevel(complete.cmd()[0]):
            return ["PRIVMSG $C$ :No."]
        if msg=="*":
            #settingsHandler.deleteSetting("coreIgnorance","1","1")
            settingsHandler.dropTable("coreIgnorance")
            settingsHandler.newTable("coreIgnorance","ignorance","nickname")
            return ["PRIVMSG $C$ :Unignored everything, my lord"]
        if msg in globalv.miscVars[0]:
            msg=globalv.miscVars[0][msg]
        try:
            if amsg in [x[0] for x in settingsHandler.readSettingRaw("coreIgnorance","ignorance")]:
                settingsHandler.deleteSetting("coreIgnorance","ignorance",amsg)
                return ["PRIVMSG $C$ :"+amsg + " successfully unignored, cap'n!"]
            msg=".*@"+msg.split('@')[1] if msg.find('@')>0 else msg
            if msg in [x[0] for x in settingsHandler.readSettingRaw("coreIgnorance","ignorance")]:
                settingsHandler.deleteSetting("coreIgnorance","ignorance",msg)
                return ["PRIVMSG $C$ :"+amsg + " successfully unignored, cap'n!"]
            else:
                matches=difflib.get_close_matches(msg,[x[0] for x in settingsHandler.readSettingRaw("coreIgnorance","ignorance")],3,0.4)
                matches=["None"] if matches==[] else matches
                globalv.variables['ignored']=matches[0]
                return ["PRIVMSG $C$ :"+msg+" is not ignored, commander! Near matches: "+', '.join(matches)+". ~ignored~ set to nearest match."]
        except Exception as detail:
            return ["PRIVMSG $C$ :"+msg+" not unignored: "+str(detail)]
        return ["PRIVMSG $C$ :"+amsg + " successfully unignored, cap'n!"]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !unignore module. Unlike !ignore, anybody can use me, except those who are ignored.","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!unignore [regex-hostmask]"]
