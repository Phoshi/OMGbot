# -*- coding: utf-8 -*-
from plugins import plugin
import feedparser

import globalv
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        msg=complete.message()
        #Parse the data, returns a tuple: (data for channels, data for items)
        feed=feedparser.parse(msg)
        return ["PRIVMSG $C$ :Latest entry from "+feed.feed.title+": "+feed.entries[0].title+" (at "+feed.entries[0].link+")"]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
