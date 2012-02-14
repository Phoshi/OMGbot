# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import urllib
import urllib2
import cookielib
import re
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        cookiejar = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))

        url = complete.message()
        ID = None
        authKey = None
        matchRegex = r"https://docs.google.com/document/d/(.*?)/[^&]*[&?]authkey=(.*)"
        matches = re.match(matchRegex, url)
        if matches:
            ID = matches.group(1)
            authKey = matches.group(2)
        else:
            matchRegex = r"https://docs.google.com/document/d/(.*?)/"
            matches = re.match(matchRegex, url)
            if matches:
                ID = matches.group(1)
            else:
                matchRegex = r"https://docs.google.com/document/pub\?id=(.*)"
                matches = re.match(matchRegex, url)
                if matches:
                    ID = match.group(1)
        newUrl = r"https://docs.google.com/feeds/download/documents/Export?docID=%s&exportFormat=txt&format=txt"%ID
        if not ID:
            return ["PRIVMSG $C$ :Story download failure!"]
        documentText = opener.open(newUrl).read()

        data={"paste_code":documentText,"paste_private":1,"paste_expire_date":"1H"}
        data=urllib.urlencode(data)
        req = urllib2.Request("http://pastebin.com/api_public.php", data)
        response = urllib2.urlopen(req)
        url = response.read()
        return ["PRIVMSG $C$ :"+url]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
