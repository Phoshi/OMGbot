# -*- coding: utf-8 -*-
from plugins import plugin
from bitlyServ import bitlyimport globalv,reclass pluginClass(plugin):	def gettype(self):		return "command"	def action(self, complete):		msg=complete.message()
		if re.match("https?://.*",msg)==None:
			msg="http://"+msg		return ["PRIVMSG $C$ :"+bitly(msg)]	def describe(self, complete):		return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]