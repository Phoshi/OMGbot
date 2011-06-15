# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import re
import urllib
import urllib2
import xml.sax.saxutils
import mimetypes
def fixXMLEntities(match):
    value=int(match.group()[2:-1])
    return chr(value)
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        logindata={'email':"AHPhoshi@gmail.com", "password":"11235813","type":"quote", "tags":complete.channel()}
        message=complete.message()
        if len(message.split())>1:
            if message.split()[-2].lower()=="-by":
                name=message.split()[-1]
                message=' '.join(message.split()[:-2])
            else:
                name=""
        logindata.update({"quote":message})
        if name!="":
            logindata.update({"source":name})
        uploadData=urllib.urlencode(logindata)
        req=urllib2.Request("http://www.tumblr.com/api/write",uploadData)
        con=urllib2.urlopen(req)
        return ["PRIVMSG $C$ :Added that post."]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the plugin that follows URLs","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :None - I monitor all input, if you have a url in your text, I will find it."]
