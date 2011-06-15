# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import urllib2, urllib
import re
from settingsHandler import readSetting
class pluginClass(plugin):
    def __init_db_tables__(self,name):
        import settingsHandler
        settingsHandler.newTable(name, "url", "regex","numMatches","matchText")
        settingsHandler.writeSetting(name,["url","regex","numMatches","matchText"],["http://google.com/complete/search?output=toolbar&q=$*$",".*","1","Autocomplete Results:"])
    def gettype(self):
        return "command"
    def action(self, complete):
        argument=complete.message().replace(' ','%20')
        url=readSetting(complete.cmd()[0],"url")
        regex=readSetting(complete.cmd()[0],"regex")
        numReturns=int(readSetting(complete.cmd()[0],"numMatches"))
        page=urllib2.urlopen(url.replace('$*$',argument)).read()
        matches=re.findall(regex,page, re.DOTALL)
        try:
            matches=[re.sub("<.*?>","",match).replace('\n','').replace('\r','') for match in matches]
            #matches=[re.sub("x3c.*?x3e","",match) for match in matches]
        except Exception as detail:
            print detail
            print "printRegexMatchFromWebpage didn't go so well in the removing HTML tags thing"
        ret=[]
        if readSetting(complete.cmd()[0],"matchText")!="":
            ret.append(readSetting(complete.cmd()[0],"matchText")) 
        for i in range(min(len(matches), numReturns)):
            if type(matches[i])==str:
                ret.append(re.sub("[^a-zA-Z0-9.,{}()[\]?\\/!\"$%^&*:;@'~#<>=+\-\s]","",matches[i]))
            elif type(matches[i])==tuple:
                ret.append(' '.join(matches[i]))
        if ret==[]:
            ret.append("No matches.")
        ret=["PRIVMSG $C$ :"+r.decode('utf-8') for r in ret]
        return ret
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !printRegexMatchFromWebpage module. I print out strings from a web page that match a regular expression.","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!printRegexMatchFromWebpage [input]"]
