# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import urllib, urllib2
class pluginClass(plugin):
    def gettype(self):
        return "postprocess"
    def action(self, complete):
        starter, message = complete.split(' :', 1)
        if len(complete) > 400:
            data={"paste_code":message,"paste_private":1,"paste_expire_date":"1H"}
            data=urllib.urlencode(data)
            req = urllib2.Request("http://pastebin.com/api_public.php", data)
            response = urllib2.urlopen(req)
            message=response.read()
            
        return ' :'.join((starter, message))
    def describe(self, complete):
        msg=complete.message()
        sender=complete[0].split(' ')
        sender=sender[2]
        return ["PRIVMSG $C$ :I am the plugin that shows output loggery in the bot's terminal.","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :None."]
