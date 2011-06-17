# -*- coding: utf-8 -*-
from plugins import plugin
import time
import globalv
class asyncInput(object):
	def __init__(self,Queue, inputQueue,X,Y, channel):
        running = True
		self.Queue=Queue
		while running:
            while not inputQueue.empty():
                data = inputQueue.get()
                if data=="stop":
                    running = False
                    break

			Queue.put("#PRIVMSG "+channel+" :"+X+"\r\n")
			time.sleep(int(Y))
	def gettype(self):
		return "input"
	def describe(self, complete):
		return ["PRIVMSG $C$ :I SAY X EVERY Y"]
