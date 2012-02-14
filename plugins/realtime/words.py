# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import settingsHandler
import re
from pluginHandler import run_command
class pluginClass(plugin):
    def gettype(self):
        return "realtime"
    def __init_db_tables__(self, name):
        settingsHandler.newTable(name, "trigger","text")
    def action(self, complete):
        message = str(complete.fullMessage())
        triggertexts=settingsHandler.readSettingRaw("words","trigger, text")
        triggertexts.reverse()
        text={}
        for trigger, texts in triggertexts:
            matchObj = re.search(trigger, message, re.I)
            if matchObj is not None:
                for i in xrange(0, 99):
                    if texts.find("$%s$"%i):
                        try:
                            texts = texts.replace("$%s$"%i, matchObj.group(i))
                        except IndexError:
                            pass
                print texts
                return run_command(texts, complete)
                        

        if complete.fullMessage().lower() in text.keys():
            return ["PRIVMSG $C$ :"+text[complete.fullMessage().lower()]]
        return [""]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the kick shield module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :Kick me. Go on, try it."]
