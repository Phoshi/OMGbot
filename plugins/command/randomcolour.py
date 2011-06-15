# -*- coding: utf-8 -*-
from plugins import plugin
import globalv,random
class pluginClass(plugin):
	def gettype(self):
		return "command"
	def action(self, complete):
		msg=complete.message()
		return ["PRIVMSG $C$ :\x03"+str(random.randint(2,12))+msg]
	def describe(self, complete):
		msg=complete.message()
		sender=complete[0].split(' ')
		sender=sender[2]
		return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
