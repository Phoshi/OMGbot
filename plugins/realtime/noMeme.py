# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import settingsHandler
import re
class pluginClass(plugin):
    def gettype(self):
        return "realtime"
    def __init_db_tables__(self, name):
        settingsHandler.newTable(name, "meme")
    def __init__(self):
        self.strikes={}
        self.banStrikes={}
    def action(self, complete):
        triggertexts=[x[0].lower() for x in settingsHandler.readSettingRaw("noMeme","meme")]
        returns=""
        for text in triggertexts:
            if re.findall(text,complete.fullMessage().lower())!=[]:
                if complete.user() not in self.strikes.keys():
                    self.strikes[complete.user()]=1
                else:
                    self.strikes[complete.user()]+=1
                if self.strikes[complete.user()]==1:
                    returns="PRIVMSG $C$ :That word/phrase is banned, $U$. This is your first warning (%s)"%re.findall(text,complete.fullMessage().lower())[-1]
                elif self.strikes[complete.user()]==2:
                    returns="PRIVMSG $C$ :$U$, this is your last warning. No saying that. (%s)"%re.findall(text,complete.fullMessage().lower())[-1]

                elif self.strikes[complete.user()]>=3:
                    self.strikes[complete.user()]==0
                    returns="KICK $C$ $U$ :Out. Now."
                    if complete.user() not in self.banStrikes.keys():
                        self.banStrikes[complete.user()]=1
                    else:
                        self.banStrikes[complete.user()]+=1
                    if self.banStrikes[complete.user()]>=3:
                        returns=["MODE $C$ +b "+globalv.miscVars[0][complete.user()],returns,"MODE $C$ -b "+globalv.miscVars[0][complete.user()]]
        return returns
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the kick shield module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :Kick me. Go on, try it."]
