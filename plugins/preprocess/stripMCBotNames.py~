# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import re
import settingsHandler
class pluginClass(plugin):
    def gettype(self):
        return "preprocess"
    def __init_db_tables__(self, name):
        settingsHandler.newTable("stripMCBotNames", "minecraft","irc")
    def __init__(self):
        subs=settingsHandler.readSettingRaw("stripMCBotNames", "minecraft, irc")
        self.substitutions={}
        for sub in subs:
            self.substitutions[str(sub[0].lower())]=str(sub[1])

    def action(self, complete):
        msg=complete.fullMessage()
        if complete.type()!="PRIVMSG":
            return complete.complete()
        starter=':'+complete.complete()[1:].split(':',1)[0]
        try:
            if complete.user()=="sr388craft":
                message=re.findall("<([a-zA-Z0-9_]+)> (.*)", complete.fullMessage())
                print message, complete.fullMessage()
                if message==[]:
                    return complete.complete()
                message=message[0]
                name=message[0]
                msg=message[1]
                print name, self.substitutions.keys()
                if name.lower() in self.substitutions.keys():
                    user=self.substitutions[name.lower()]+'!'+globalv.nicks[self.substitutions[name.lower()]]
                else:
                    user="%s!nothing@nowhere.no.uk"%(name)
                starter=":%s PRIVMSG %s "%(user, complete.channel())
        except Exception as detail:
            print "BotName Failure"
            print detail

        return starter+':'+msg

    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
