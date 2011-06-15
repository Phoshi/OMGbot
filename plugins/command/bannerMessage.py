# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import urllib
import urllib2
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        message=complete.message()
        url="http://64digits.com/index.php?cmd=banner&submit=true"
        data={'b_message':message}
        encoded=urllib.urlencode(data)
        urllib2.urlopen(url, encoded).read()
        return ["PRIVMSG $C$ :Sent that request."]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
