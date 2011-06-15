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
        msg=complete.message().split('::')
        if len(msg)>1:
            stdin=msg[1]
            args=msg[0]
        else:
            stdin=' '.join(complete.message().split()[1:])
            args=complete.message().split()[0]
        args=int(args)
        msg=stdin[:stdin.find(' ',args)]
        return ["PRIVMSG $C$ :"+msg+('...' if len(stdin)>args else '')]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
