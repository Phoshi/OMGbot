# -*- coding: utf-8 -*-
#Startup Script
#Initialise Variables
#Super important, deleting these is a Bad Idea
import os
import sys
database=sys.argv[1] if len(sys.argv)>1 else "config.db"
if not os.path.exists("config"):
    os.makedirs("config")
import firstRun
from asyncInputHandler import inputSystem
from settingsHandler import readSetting, tableExists, readSettingRaw
#First Run checkign
if not tableExists("core"):
	firstRun.createDatabase()
	firstRun.createVariables()
	firstRun.createAutoload()
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
basePlugin={}
communication={}
from pickle import load
with open(os.path.join("config","variables")) as file:
    variables=load(file)
del load
#It's nice to keep these steady
nickname=""
commandCharacter="!"
miscVars=[]
masks={}
nicks=dict([(nick, mask) for nick, mask in readSettingRaw("'core-nickmasks'","nick,hostmask")])
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
for line in readSettingRaw("coreAutoLoad", "plugin, loadAs"):
    pluginList.append(line)
