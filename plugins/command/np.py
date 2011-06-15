# -*- coding: utf-8 -*-
# This Python file uses the following encoding: utf-8
from plugins import plugin
from bitlyServ import bitly
import globalv
import re,urllib2
import settingsHandler
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def __init_db_tables__(self, name):
        settingsHandler.newTable(name, "IRCnick", "LASTFMnick")
    def action(self, complete):
        msg=complete.message()
        user=complete.user()
        users={}
        for nicknick in settingsHandler.readSetting(complete.cmd()[0], "IRCnick, LASTFMnick"):
            users.update({nicknick[0].lower():nicknick[1]})
        if msg!="":
            user=msg
        if len(msg.split())>=2:
            if msg.split()[0]=="-link":
                settingsHandler.writeSetting(complete.cmd()[0], ["IRCnick","LASTFMnick"], [complete.user(), ' '.join(msg.split()[1:])])
                return ["PRIVMSG $C$ :Linked %s to %s"%(complete.user(),  ' '.join(msg.split()[1:]))]
        try:
            if user.lower() in users.keys():
                name=users[user.lower()]
            else:
                name=user
            url="http://ws.audioscrobbler.com/1.0/user/"+name+"/recenttracks.rss"
            p=urllib2.urlopen(url).read()
            p=re.search("<description>Last 10 tracks submitted to Last.fm</description>(.*)</item>",p,re.DOTALL).group(1)
            l=re.search("<link>(.*?)</link>",p,re.DOTALL).group(1)
            p=re.search("<title>(.*?)</title>",p,re.DOTALL).group(1)
            if len(l)>50:
                l=bitly(l)
            p=p.split('\xe2\x80\x93')
            msg=user+" is listening to"+p[1].decode('utf-8')+" by "+p[0].decode('utf-8')+" ("+l+")"
        except:
            msg="I don't know what "+user+" is listening to. Sorry."
        return ["PRIVMSG $C$ :"+msg]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !np module. I grab what a designated last.fm user is listening to!","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [OPTIONAL user|-link] [OPTIONAL last.fm nickname to link to]"]
