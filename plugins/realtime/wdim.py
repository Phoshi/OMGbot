# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import time
import os
import pickle

class userState():
    def __init__(self, host, nick, line):
        self.hostMask = host
        self.nick = nick
        self.lastLine = line

class pluginClass(plugin):
    def __init__(self):
        self.dumppath = "" 
        self.users = []
        self.nLines = 0
        self.lastLines = []
        self.inited=False

    def gettype(self):
        return "realtime"
        
    def init(self, complete):

        self.dumppath = os.path.join('config','wdim-%s'%complete.channel())
        if os.path.exists(self.dumppath):
            with open(self.dumppath) as logFile:
                self.users = pickle.load(logFile)
                self.nLines = pickle.load(logFile)
                self.lastLines = pickle.load(logFile)
        else:
            self.users = []
            self.nLines = 0
            self.lastLines = []
        self.inited=True
    def action(self,complete):
        if not self.inited:
            self.init(complete)
        hostMask = complete.userMask()[complete.userMask().find('!')+1:]
        msg = complete.fullMessage()
        user = complete.user()

        MAX_LINES = 7
        
        if complete.type() == "PART" or complete.type() == "QUIT":
            userExists = False
            for u in self.users:
                if u.nick == user or u.hostMask == hostMask:
                    u.lastLine = nLines
                    userExists = True
                    break
            if not userExists:
                self.users.append(userState(hostMask, user, self.nLines))

        if complete.type() == "PRIVMSG":
            if complete.fullMessage().lower()[:15] == 'what did i miss':
                lastLine = -1
                for u in self.users:
                    if u.nick == user or u.hostMask == hostMask:
                        lastLine = u.lastLine
                        break
                if lastLine == -1:
                    nMissedLines = MAX_LINES
                else:
                    nMissedLines = self.nLines - lastLine
                nLog = min(nMissedLines, MAX_LINES)
                message = ["PRIVMSG $C$ :While you were absent %d lines were typed. Printing last %d:"%(nMissedLines, nLog)]
                for line in self.lastLines[-nLog:]:
                    message += ["PRIVMSG $C$ :%s"%line]
                return message
            else:
                self.nLines += 1
                        
                if msg.split()[0]=="\x01ACTION":
                    msg=' '.join(msg.split()[1:])[:-1]
                else:
                    msg="* "+msg
                message="[%(time)s] * %(user)s %(umessage)s" % {"time":time.strftime("%d %b %y %H:%M"), "user":user,"umessage":msg}

                self.lastLines.append(message)
                if len(self.lastLines) > 7:
                    self.lastLines = self.lastLines[1:]
                with open(self.dumppath, "w") as logFile:
                    pickle.dump(self.users, logFile)
                    pickle.dump(self.nLines, logFile)
                    pickle.dump(self.lastLines, logFile)
                
        return []

    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the What-did-I-miss? module! Say 'what did I miss' to see what you missed!"]
