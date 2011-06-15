# -*- coding: utf-8 -*-
from plugins import plugin
import time
import globalv
class asyncInput(object):
	def __init__(self,Queue,stop,X,Y, channel):
		self.Queue=Queue
		while stop.isSet()==False:
			Queue.put("#PRIVMSG "+channel+" :"+X+"\r\n")
			time.sleep(int(Y))
	def gettype(self):
		return "input"
	def describe(self, complete):
		return ["PRIVMSG $C$ :I SAY X EVERY Y"]
