# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import re
import htmllib
import urllib2,urllib
import settingsHandler

def unescape(s):
    p = htmllib.HTMLParser(None)
    p.save_bgn()
    p.feed(s)
    return p.save_end()

class pluginClass(plugin):
    def __init_db_tables__(self, name):
        settingsHandler.newTable(name, "showTitle")
        settingsHandler.writeSetting(name,"showTitle","True")
    def gettype(self):
        return "command"
    def action(self, complete):
        msg=complete.message()
        url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q='+msg.replace(' ', '%20')
        try:
            response = urllib2.urlopen(url)
            page = response.read()
            result = re.search("(?P<url>\"url\":\"[^\"]+)", page).group('url').decode('utf-8')
            result=result[7:]
            title = re.search("(?P<url>\"titleNoFormatting\":\"[^\"]+)", page).group('url').decode('utf-8')
            title=title[21:]
            titleString=unescape(title)+" (at "+urllib.unquote(result)+')' if settingsHandler.readSetting(complete.cmd()[0],"showTitle")=="True" else urllib.unquote(result)
        except:
            titleString="No results!"
        return ["PRIVMSG $C$ :"+titleString]
    def describe(self, complete):
        msg=complete.message()
        return ["PRIVMSG $C$ :I am the !google module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!google [phrase]"]
