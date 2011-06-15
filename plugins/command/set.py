# -*- coding: utf-8 -*-
from plugins import plugin
from aliasHandler import save_alias
from userlevelHandler import getLevel
from securityHandler import isAllowed
import settingsHandler
import globalv
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def __level__(self):
        return 100
    def action(self, complete):
        msg=complete.message()
        msgBack=[]
        message=lambda x:msgBack.append("PRIVMSG $C$ :"+x)
        if isAllowed(complete.userMask())>=getLevel(complete.cmd()[0]):
            if msg.split()[0]!="-remove":
                result=save_alias(msg)
                print globalv.loadedAliases.keys()
                if result==1:
                    message("Alias Saved.")
                elif result==2:
                    message("Alias unsuccessful. Alias is already set.")
                else:
                    message("Alias unsuccessful. Make sure you have previously !alias-ed this command")
                    print globalv.loadedAliases.keys()
            else:
                settingsHandler.deleteSetting("alias","aliasName",msg.split()[1])
                message("Alias Removed")
        else:
            message("Alias unsuccessful. This action requires higher priviledges. Use "+globalv.commandCharacter+"alias for temporary aliases.")
        return msgBack
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !set module. I promote aliases. An un-set alias will reset when the bot resets.","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!set [alias]"]
