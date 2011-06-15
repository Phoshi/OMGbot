# -*- coding: utf-8 -*-
from plugins import plugin
import globalv, security
class pluginClass(plugin):
	def gettype(self):
		return "command"
	def action(self, complete):
		reload(security)
		globalv.miscVars[2]=security.users()
		return ["PRIVMSG $C$ :"+"Shield integrity restored, now operating at 100% of practical capacity."]
	def describe(self, complete):
		msg=complete.message()
		sender=complete[0].split(' ')
		sender=sender[2]
		return ["PRIVMSG $C$ :I am the !resecure module. I reload user permissions from the database.","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!resecure"]