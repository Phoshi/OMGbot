# -*- coding: utf-8 -*-
from plugins import plugin
import globalv,time
import settingsHandler
class pluginClass(plugin):
    def __init_db_tables__(self, name):
        settingsHandler.newTable(name, "timeLimit", "numberLimit")
        settingsHandler.writeSetting(name,["timeLimit","numberLimit"],["30","6"])
    def __init__(self):
        self.userlist=[]
    def gettype(self):
        return "realtime"
    def action(self, args):
        complete=args.complete()[1:].split(':',1)
        if len(complete)==2:
            if len(complete[0].split())==3:
                msg=args.message()
                if complete[1].startswith(globalv.commandCharacter):
                    self.userlist.append([complete[0].split('!')[0],time.time()])
                    earliestTimes={}
                    latestTimes={}
                    numberOfTimes={}
                    for line in self.userlist:
                        if line[0] not in earliestTimes.keys():
                            earliestTimes[line[0]]=line[1]
                        else:
                            if earliestTimes[line[0]]>line[1]:
                                earliestTimes[line[0]]=line[1]
                        if line[0] not in latestTimes.keys():
                            latestTimes[line[0]]=line[1]
                        else:
                            if latestTimes[line[0]]<line[1]:
                                latestTimes[line[0]]=line[1]
                        if line[0] not in numberOfTimes.keys():
                            numberOfTimes[line[0]]=0
                        else:
                            numberOfTimes[line[0]]+=1
                    for user in earliestTimes.keys():
                        if latestTimes[user]-earliestTimes[user]<int(settingsHandler.readSetting("noSpam","timeLimit")):
                            if numberOfTimes[user]>=int(settingsHandler.readSetting("noSpam","numberLimit")):
                                userMask=globalv.miscVars[0][user]
                                if not userMask in globalv.ignoredUsers:
                                    settingsHandler.writeSetting("coreIgnorance",["ignorance","nickname"],['.*@'+userMask.split('@')[1],user])
                                    self.userlist=[]
                                    return ["PRIVMSG $C$ :Oi, $U$, shut up for christ's sake."]
                        elif numberOfTimes[user]>=2:
                            self.userlist=[]
        return [""]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
