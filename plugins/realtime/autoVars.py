# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import re
import urllib2
import xml.sax.saxutils
import mimetypes
def fixXMLEntities(match):
    value=int(match.group()[2:-1])
    return chr(value)
class pluginClass(plugin):
    def gettype(self):
        return "realtime"
    def __init__(self):
        self.lastargs=""
    def action(self, complete):
        if re.findall("https?://[^\s]*",complete.fullMessage())!=[]:
            globalv.variables['lasturl']=re.findall("https?://[^\s]*",complete.fullMessage())[-1]

        if complete.type()=="JOIN":
            globalv.variables['lastjoin']=complete.user()
        if complete.type()=="QUIT":
            globalv.variables['lastquit']=complete.user()
        if complete.type()=="PART":
            globalv.variables['lastpart']=complete.user()
        if complete.type()=="KICK":
            globalv.variables['lastkick']=complete.complete().split(':')[1].split()[-1]
        if complete.fullMessage().startswith(globalv.commandCharacter) and "!!" not in complete.message():
            globalv.variables['!!']=complete.message()
        return [""]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the plugin that follows URLs","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :None - I monitor all input, if you have a url in your text, I will find it."]
