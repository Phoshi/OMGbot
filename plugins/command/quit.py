# -*- coding: utf-8 -*-
from plugins import plugin
from securityHandler import isAllowed
from settingsHandler import readSetting
from userlevelHandler import getLevel
import globalv
class pluginClass(plugin):
    def __level__(self):
        return 200
	def __init_db_tables__(self,name):
		import settingsHandler
		settingsHandler.newTable(name,"userRequirement")
		settingsHandler.writeSetting(name,"userRequirement","elevated")
	def gettype(self):
		return "command"
	def action(self, complete):
		msg=complete.message()
		sender=complete.userMask()
		userAllowed=(isAllowed(sender)>=getLevel(complete.cmd()[0])) if readSetting(complete.cmd()[0],"userRequirement")=="elevated" else sender==readSetting(complete.cmd()[0],"username") if readSetting(complete.cmd()[0],"userRequirement")=="owner" else 1
		if userAllowed:
			if msg=="":
				msg="QQ"
			return ["QUIT :"+msg]
		else:
			return ["KICK $C$ $U$ :Yeah, no."]
	def describe(self, complete):
		msg=complete.message()
		sender=complete[0].split(' ')
		sender=sender[2]
		return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
