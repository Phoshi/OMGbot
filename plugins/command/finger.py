# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
class pluginClass(plugin):
	def gettype(self):
		return "command"
	def action(self, complete):
		msg=complete.message()
		globalv.timeUsers[msg.split()[0]]=complete.channel()
		print globalv.timeUsers
		return ["PRIVMSG "+msg.split()[0]+" :FINGER"]
	def describe(self, complete):
		return ["PRIVMSG $C$ :I am the !time module. I return a user's local time.","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!time [user]"]
