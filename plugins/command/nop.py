# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        return [""]
    def describe(self, complete):
        return ["PRIVMSG $C$ :TOUCH ME AND I'LL FUCK YOUR SHIT","KICK $C$ $U$ :COURTESY OF MY BIG, FAT ASS."]
