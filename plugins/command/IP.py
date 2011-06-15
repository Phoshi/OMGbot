# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import socket
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        msg=complete.message()
        if msg.startswith("http://"):
            msg=msg[7:]
        ip=str(socket.gethostbyname(msg))
        return ["PRIVMSG $C$ :"+ip.decode('utf-8')]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
