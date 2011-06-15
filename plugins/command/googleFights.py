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
        terms=[x.strip() for x in msg.split(',')]
        topResult=(0,'')
        resultScores={}
        for word in terms:
            url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q='+word.replace(' ', '%20')
            response = urllib2.urlopen(url)
            page = response.read()
            result = re.findall("estimatedResultCount.*?([0-9]+)\"", page)[0]
            result=int(result)
            resultScores[word]=result
            if result>topResult[0]:
                topResult=(result, word)
            otherTerms=[]
            for word in resultScores.keys():
                if word!=topResult[1]:
                    otherTerms.append(word+" with "+str(resultScores[word]))
        return ["PRIVMSG $C$ :Winner is "+topResult[1]+" with "+str(topResult[0])+" results!","PRIVMSG $C$ :Other results were: "+', '.join(otherTerms)]
    def describe(self, complete):
        msg=complete.message()
        return ["PRIVMSG $C$ :I am the !googleFights module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!googleFights [list of words to compare]"]
