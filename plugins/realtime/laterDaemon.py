# -*- coding: utf-8 -*-
from plugins import plugin
from pluginFormatter import formatOutput
from pluginArguments import pluginArguments
import os
import globalv
class pluginClass(plugin):
	def gettype(self):
		return "realtime"
		
	def getLater(self,Name):
		if Name=="" or Name not in globalv.miscVars[3]:
			laterFile = open(os.path.join("config","later.txt"))
			lines=laterFile.read()
			laterFile.close()
			lines=lines.split('\n')
			lines.reverse()	
			for line in lines:
				globalv.miscVars[3].update({line.split('##')[0]:line.split('##')[1:]})
		if Name in globalv.miscVars[3]:
			return globalv.miscVars[3][Name]
		else:
			return ""
		
	def remLater(self,Name):	
		laterFile=open(os.path.join("config","later.txt"))
		file=laterFile.read()
		fullLaters=[]
		temp=file.split('\n')
		temp.reverse()
		for line in temp:
			if line!=Name+"##"+globalv.miscVars[3][Name][0]+"##"+globalv.miscVars[3][Name][1]:
				fullLaters.append(line)
		fullLaters.reverse()
		fullLaters='\n'.join(fullLaters)
		laterFile.close()
		laterFile=open(os.path.join("config","later.txt"),"w")
		laterFile.write(fullLaters)
		laterFile.close()
		del globalv.miscVars[3][Name]
	
	def action(self, args):
		complete=args.complete()[1:].split(':',1)
		if len(complete[0].split())>2:
			msg=args.message()
			laterMessages = self.getLater(args.user())
			msg=[]
			if args.channel!=globalv.nickname:
				if laterMessages!="":
					if laterMessages[1].split()[0] in globalv.loadedPlugins.keys():
						toSend=pluginArguments(":"+laterMessages[0]+" PRIVMSG $C$ :"+globalv.commandCharacter+laterMessages[1])
						output=globalv.loadedPlugins[laterMessages[1].split()[0]].action(toSend)
						print output,'###'
						msg+=(formatOutput(output,args))
					else:
						msg+=(["PRIVMSG $C$ :Hey, "+args.user()+": "+laterMessages[0].split('!')[0]+" said "+laterMessages[1]])
					self.remLater(args.user())
					msg+=["PRIVMSG $C$ :(From "+laterMessages[0].split('!')[0]+" to "+args.user()+")"]
					return msg
		return [""]
	def describe(self, complete):
		return ["PRIVMSG $C$ :I am the ! module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!"]
