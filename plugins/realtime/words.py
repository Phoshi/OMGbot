# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import settingsHandler
class pluginClass(plugin):
    def gettype(self):
        return "realtime"
    def __init_db_tables__(self, name):
        settingsHandler.newTable(name, "trigger","text")
    def action(self, complete):
        triggertexts=settingsHandler.readSettingRaw("words","trigger, text")
        text={}
        for trigger, texts in triggertexts:
            text[trigger]=texts
        if complete.fullMessage() in text.keys():
            return ["PRIVMSG $C$ :"+text[complete.fullMessage()]]
        return [""]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the kick shield module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :Kick me. Go on, try it."]
