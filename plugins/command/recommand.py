# -*- coding: utf-8 -*-
from plugins import plugin
import globalvclass pluginClass(plugin):	def gettype(self):		return "command"	def action(self, complete):		msg=complete.message()
		globalv.commandCharacter=msg.replace('"','')		return ["PRIVMSG $C$ :Alright, done that!"]	def describe(self, complete):		msg=complete.message()		sender=complete[0].split(' ')		sender=sender[2]		return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]