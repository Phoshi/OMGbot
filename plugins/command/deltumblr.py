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
        logindata={'email':"AHPhoshi@gmail.com", "password":"11235813",}
        tumblrids=[]
        for message in complete.message().split():
            tumblrids.append(message.split('/')[-1])
        for tumblrid in tumblrids:
            logindata.update({"post-id":tumblrid})
            uploadData=urllib.urlencode(logindata)
            req=urllib2.Request("http://www.tumblr.com/api/delete",uploadData)
            con=urllib2.urlopen(req)
        return ["PRIVMSG $C$ :Erased that post."]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the plugin that follows URLs","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :None - I monitor all input, if you have a url in your text, I will find it."]
