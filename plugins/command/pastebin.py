# -*- coding: utf-8 -*-
from plugins import plugin
import globalv, urllib2,urllib
import time
import datetime
import os
import re
import sys
sys.path.append("/home/py/.python/")
import datetime, dateutil.parser
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        readFile=complete.message()
        data={"paste_code":readFile,"paste_private":1,"paste_expire_date":"1H"}
        data=urllib.urlencode(data)
        req = urllib2.Request("http://pastebin.com/api_public.php", data)
        response = urllib2.urlopen(req)
        msg=response.read()
        print msg
        return ["PRIVMSG $C$ :"+msg]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !pastebinLogs module. I return a pastebin URL with the logs of today - [msg].","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!pastebinLogs [offset]"]
