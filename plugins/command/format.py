# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import re
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def __append_seperator__(self):
        return True
    def action(self, complete):
        print "X"
        msg=complete.message()
        formatRules=msg.split('::')[0]
        output=formatRules
        toFormat=msg.split('::')[1]
        highest=[int(x) for x in re.findall("\$([0-9]+)",formatRules)]
        if highest!=[]:
            highest.sort()
            highest=highest[-1]
            for x in xrange(highest+1):
                try:
                    output=output.replace("$%s"%x,toFormat.split()[x])
                except:
                    print "formatter: Index failure"
        output=output.replace("$*",toFormat)
        return ["PRIVMSG $C$ :"+output]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
