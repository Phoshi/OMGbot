# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import re
import shlex
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def __append_seperator__(self):
        return True
    def action(self, complete):
        msg=str(complete.message().split('::')[0])
        msg=shlex.split(msg)
        return ["PRIVMSG $C$ :"+re.sub(msg[0],msg[1],str(complete.message().split('::',1)[1]),999).decode('utf-8')]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
