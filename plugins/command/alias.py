# -*- coding: utf-8 -*-
from plugins import plugin
from aliasHandler import load_alias
from securityHandler import isAllowed
from userlevelHandler import getLevel
import globalv
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def __level__(self):
        return 50
    def action(self, complete):
        msg=complete.message()
        pluginBlacklist=["special"]
        if msg.split()[0] in pluginBlacklist and not (isAllowed(complete.userMask())>=getLevel(complete.cmd()[0])):
            msg=["PRIVMSG $C$ :Restricted plugin!"]
        if msg.split()[0] not in globalv.loadedPlugins.keys():
            try:
                load_alias(msg.split()[0], ' '.join(msg.split()[1:]))
                msg=["PRIVMSG $C$ :Alias successful."]
            except:
                msg=["PRIVMSG $C$ :Alias unsuccessful. Are you sure %s is a valid plugin?"%msg.split()[1]]

        else:
            msg=[]
            message=lambda x:msg.append("PRIVMSG $C$ :"+x)
            message("Alias unsuccessful. Syntax: "+globalv.commandCharacter+"alias [word] [command] [optional arguments]")
            message("Optional Arguments can include $C$, which will expand to the channel name, $U$, which will expand to the username of the person who sends it.")
            message("You can also use $number$ style syntax, where number is a one or two digit number representing the word of the input to take. (As in, $2$ would extract \"hi\" from \"!command hey hi\". Additionally, a + or - after the number can be used to grab all words before or after that word.")
        return msg
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !alias module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!alias [what] [plugin] [arguments]"]
