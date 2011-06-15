# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
from securityHandler import isAllowed
from userlevelHandler import getLevel
import difflib
import settingsHandler
class pluginClass(plugin):
    def __init_db_tables__(self, name):
        settingsHandler.newTable(name,"key","value")
    def gettype(self):
        return "command"
    def action(self, complete):
        msg=complete.message()
        returner=""
        elevated = getLevel(complete.userMask()) >= isAllowed(complete.cmd()[0])
        if msg=="":
            returner="This is the %s dictionary. Run !%s -list for a list of known values!"%(complete.cmd()[0], complete.cmd()[0])
        elif msg.split()[0]=="-add" and elevated:
            settingsHandler.writeSetting(complete.cmd()[0],["key","value"], [msg.split()[1],' '.join(msg.split()[2:])])
            returner="Key:Value pair added!"
        elif msg.split()[0]=="-delete" and elevated:
            settingsHandler.deleteSetting(complete.cmd()[0],"key",msg.split()[1])
            returner="Key removed!"
        elif msg.split()[0]=="-list":
            keypairs=[x[0] for x in settingsHandler.readSettingRaw(complete.cmd()[0],"key")]
            returner=', '.join(keypairs)
        elif msg.split()[0]=="-random":
            keypairs=settingsHandler.readSettingRaw(complete.cmd()[0],"key, value")
            pairs={}
            for keypair in keypairs:
                pairs[keypair[0].lower()]=keypair[1]
            import random
            keys=pairs.keys()
            random.shuffle(keys)
            returner=keys[0]+": "+pairs[keys[0]]
        else:
            keypairs=settingsHandler.readSettingRaw(complete.cmd()[0],"key, value")
            pairs={}
            for keypair in keypairs:
                pairs[keypair[0].lower()]=keypair[1]
            if unicode(msg.split()[0]).lower() in pairs.keys():
                returner=pairs[unicode(msg.split()[0]).lower()]
            elif "default" not in pairs.keys():
                returner="No definition."
                matches=difflib.get_close_matches(msg.split()[0],pairs.keys(),10,0.1)
                if len(matches)>0:
                    returner+=" Perhaps you meant: "+', '.join(matches[:-1])
                    if len(matches)>1:
                        returner+=" or "+matches[-1]
                else:
                    returner+=" No similar definitions"
            else:
                returner=pairs['default']
        if returner=="":
            return [""]
        return ["PRIVMSG $C$ :"+returner]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !text2text module. I provide simple dictionary lookups.","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!text2text [-add|-delete|-list] key [definition]"]
