# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import re
import urllib, urllib2

class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        query = {'q':'define: %s' % complete.message()}
        url = 'http://www.google.com/search?sclient=psy&hl=en&site=&source=hp&%s&btnG=Search' % (urllib.urlencode(query))
        headers = {
            'Host': 'www.google.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'
        }
        req = urllib2.Request(url, headers = headers)
        first = urllib2.urlopen(req)
        source = first.read()

        url = re.search('/search[^\'"]+tbs=dfn:1[^\'"]+', source)
        if url:
            url = 'http://www.gooogle.com' + url.group(0).replace('&amp;','&')
        else:
            return ["PRIVMSG $C$ :No Definitions."]

        req = urllib2.Request(url, headers = headers)
        first = urllib2.urlopen(req)
        source = first.read()

        info = re.search('<li style="list-style:none">(?P<definition>.+?)</li>.+?url=(?P<source>.+?)&', source)
        if info == None:
            return ["PRIVMSG $C$ :No Definitions."]
        
        definition = info.group('definition')
        source = info.group('source')
        source = urllib.unquote(source)
        
        return ["PRIVMSG $C$ :%s" % definition, "PRIVMSG $C$ :from %s" % source]
    def describe(self, complete):
        msg=complete.message()
        return ["PRIVMSG $C$ :I am the !define module. I use google to define words!","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!define [word]"]
