# -*- coding: utf-8 -*-
from plugins import plugin
from pluginArguments import pluginArguments
import globalv
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        msg=complete.message()
        arguments=pluginArguments("no!body@nowhere PRIVMSG #nothing :!ocr kindred")
        result=globalv.loadedPlugins['ocr'].action(arguments)
        return ["PRIVMSG $C$ :"+result[0]]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
