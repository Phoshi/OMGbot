# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
class pluginClass(plugin):
	def gettype(self):
		return "command"
	def action(self, complete):
		return ["PRIVMSG $C$ :"+str(globalv.input.getPrimaryProducerStatus())]
	def describe(self, complete):
		return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
