# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import random
import settingsHandler
import re
class pluginClass(plugin):
	def gettype(self):
		return "postprocess"
	def __init_db_tables__(self,name):
		settingsHandler.newTable(name,"noKickUsers")
	def action(self, complete):
		noKickUsers=settingsHandler.readSetting("noKick","noKickUsers")
		noKickUsers=[x[0] if type(x)==tuple else x for x in noKickUsers]
		if complete.split()[0]=="KICK" and complete.split()[2] in noKickUsers:
			return ""
		else:
			return complete
	def describe(self, complete):
		return ["PRIVMSG $C$ :I am the !kick module","PRIVMSG $C$ :Usage: (Requires Elevated Bot Privileges)","PRIVMSG $C$ :!kick [user]"]
