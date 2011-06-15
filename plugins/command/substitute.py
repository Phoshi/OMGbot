# -*- coding: utf-8 -*-
from plugins import plugin
from securityHandler import isAllowed
from userlevelHandler import getLevel
import settingsHandler
import globalv
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        msg=complete.message()
        if isAllowed(complete.userMask())>=getLevel(complete.cmd()[0]):
            trigger=msg.split()[0]
            command=' '.join(msg.split()[1:])
            try:
                if trigger not in [x[0] for x in settingsHandler.readSettingRaw("'core-expansions'","trigger")]:
                    settingsHandler.writeSetting("'core-expansions'",["trigger","command"],[trigger,command])
                else:
                    settingsHandler.updateSetting("'core-expansions'","command",command,where="trigger='%s'"%trigger)
                msg="%s will now substitute to the output of %s"%(trigger, command)
            except Exception as detail:
                msg="Failure: %s"%detail
        else:
            msg="Sorry, you need to be elevated to use this command!"



        return ["PRIVMSG $C$ :"+msg]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
