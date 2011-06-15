# -*- coding: utf-8 -*-
#Startup Script
#Initialise Variables
#Super important, deleting these is a Bad Idea
import os
import sys
from asyncInputHandler import inputSystem
database=sys.argv[1] if len(sys.argv)>1 else "config.db"
loadedPlugins={}
loadedRealtime={}
loadedSpecial={}
loadedPostprocess={}
loadedPreprocess={}
aliasExtensions={}
loadedAliases={}
accessRights={}
ignoredUsers=[]
bannedChannels=[]
timeUsers={}
channelUsers={}
loadedInputs={}
input=inputSystem()
outputQueue=[]
from pickle import load
with open(os.path.join("config","variables")) as file:
    variables=load(file)
del load
#It's nice to keep these steady
nickname=""
commandCharacter="!"
miscVars=[]
from settingsHandler import readSetting
masks={}
nicks=dict([(nick, mask) for nick, mask in readSetting("'core-nickmasks'","nick,hostmask")])
miscVars.append(nicks)
miscVars.append(nickname) #Stores the bot's current nickname [1]
miscVars.append([]) #OMGbot Identified Users [2]
miscVars.append({}) #Later variables[3]
miscVars.append({}) #Topics [4]
channels=readSetting("coreAutoJoin","channel")
if type(channels[0])==tuple:
    channels=[x[0] for x in channels]
elif type(channels[0])==unicode:
    channels=[channels]
pluginList=[]
for line in open(os.path.join("config","autoloading.txt")):
    pluginList.append(line.strip())
