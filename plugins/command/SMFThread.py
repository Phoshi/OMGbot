# -*- coding: utf-8 -*-
from plugins import plugin
from SMFThreadInformation import SMFThread
import globalv
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        msg=complete.message()
        thread=SMFThread(msg)
        print thread.thread
        msg=thread.thread['thread']['title']+thread.thread['entriesByID'][thread.postID]['name']
        return ["PRIVMSG $C$ :"+msg]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
