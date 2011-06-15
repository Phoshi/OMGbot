# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        msg=complete.message()
        user=msg.split()[0] if len(msg.split())>0 else complete.user()
        if user[0]=='#':
            for cuser in globalv.channelUsers[complete.channel()]:
                globalv.timeUsers[cuser]=complete.channel()
        globalv.timeUsers[user]=complete.channel()
        return ["PRIVMSG "+user+" :TIME"]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !time module. I return a user's local time.","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!time [user]"]
