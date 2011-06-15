# -*- coding: utf-8 -*-
from plugins import plugin
import globalv

class AlreadyAPieceThereException(Exception):
		def __init__(self):
			pass
		def __str__(self):
			return "Piece already there!"


class TicTacToe(object):
	def __init__(self,XUser,OUser):
		self.board=[" "]*9
		self.Users=[XUser,OUser]
		
	def setBit(self,where,what):
		numbers="x678345012"
		where=int(numbers[int(where)])
		if what.lower()=="x" or what.lower()=="o":
			if self.board[where]==" ":
				self.board[where]=what
			else:
				raise AlreadyAPieceThereException
	def checkFinished(self):
		finishedArray=[[0,1,2],[3,4,5],[6,7,8], # vertical
						[0,3,6],[1,4,7],[2,5,8], # horizontal
						[0,4,8],[2,4,6]] #Diagonal
		finished=0
		for check in finishedArray:
			if self.board[check[0]]==self.board[check[1]]==self.board[check[2]]:
				if self.board[check[0]]!=" ":
					finished=1
				
		return finished
	def printState(self,turn):
		board=self.board
		state=['PRIVMSG $C$ :'+'|'.join(board[0:3]),'PRIVMSG $C$ :'+'|'.join(board[3:6]),'PRIVMSG $C$ :'+'|'.join(board[6:9]),'PRIVMSG $C$ :It is now '+self.User(turn)+"'s turn"]
		return state
	def User(self,turn):
		if turn=="X":
			return self.Users[0]
		else:
			return self.Users[1]
			
class pluginClass(plugin):
	def gettype(self):
		return "command"
	import random

	def __init__(self):
		self.currentGame=TicTacToe("PY","OMGbot")
		self.turn="X"
		self.isDone=1
	def action(self, complete):
		msg=complete.message()
		nick=complete.user()
		moves=[str(i+1) for i in range(9)]
		X="X"
		O="O"
		if msg.split()[0:2]==["new","game"]:
			try:
				self.currentGame=TicTacToe(msg.split()[2],msg.split()[3])
				self.turn="X"
				self.isDone=0
				msg="Ok, it's "+msg.split()[2]+"'s go!"
			except:
				msg="Needs two user names!"
		if not self.isDone:
			if msg in moves:
				print nick, self.currentGame.User(self.turn)
				if nick==self.currentGame.User(self.turn):
					move=int(msg)
					try:
						self.currentGame.setBit(int(move),self.turn)
						msg="ok! Set position "+str(move)+" to "+self.turn
						if self.turn==X:
							self.turn=O
						else:
							self.turn=X
						if self.currentGame.checkFinished():
							if self.turn==X:
								nturn=O
							else:
								nturn=X
							msg="Well done, "+self.currentGame.User(nturn)+", you won!"
							self.isDone=1
							return ["PRIVMSG $C$ :"+msg]
						return self.currentGame.printState(self.turn)
					except Exception as detail:
						msg="Space already taken."
						print detail
				else:
					msg="No, silly, it's "+self.currentGame.User(self.turn)+"'s turn. let them go."
			elif msg=="check":
				return self.currentGame.printState(self.turn)
		else:
			msg="No game in progress. Syntax: TicTacToe new game [player 1] [player 2]"
		return ["PRIVMSG $C$ :"+msg]
	def describe(self, complete):
		return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]