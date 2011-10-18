# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import urllib2
def getHumanReadable(bytes):
    suffixes = ["", "KB", "MB", "GB"]
    suffixIndex = 0
    while bytes > 1024:
        bytes /= 1024.0
        suffixIndex+=1
    return "%.2f %s"%(bytes, suffixes[suffixIndex])
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        urlobject = urllib2.urlopen(complete.message())
        status = urlobject.code
        type = urlobject.headers.type
        if "server" in urlobject.headers.keys():
            server = urlobject.headers["server"]
        else:
            server = "Unknown"
        size = len(urlobject.read())
        return ["PRIVMSG $C$ :[HTTP %s] Type: %s; Size: %s bytes (%s); Server: %s"%(status, type, size, getHumanReadable(size), server)]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
