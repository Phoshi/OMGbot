# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import pickle
import sys
import os
import re

class pluginClass(plugin):
    def __init__(self):
        self.charIgnore = '!#*()"\'?,.\x01\x02\x03\x04\x05\x06\x07\x08\x16\xff\t\r\n'
        self.exceptions = [':)',':(','=)','=(',':|','>:(','>:)','._.',':\'(']

    def gettype(self):
        return "realtime"
        
    def action(self,complete):
        logUser = True
        if complete.channel()=="":
            return [""]
        if not complete.channel()[0] == '#' or not complete.type()=="PRIVMSG":
            return [""]
        
        if not ".*!"+complete.userMask().split('!',1)[1] in [x[0] for x in globalv.miscVars[2]]:
            logUser = False

        logpath = os.path.join('config','picturelogs','picturelog-%s'%complete.channel())
        words_channel = dict()
        
        if os.path.exists(logpath):
            with open(logpath) as logFile:
                words_channel = pickle.load(logFile)
                
        if logUser:
            logpath_u = os.path.join('config','picturelogs','picturelog-%s-%s'%(complete.channel(),complete.user()))
            words_user = dict()
            
            if os.path.exists(logpath_u):
                with open(logpath_u) as logFile:
                    words_user = pickle.load(logFile)
        
                
        words = complete.fullMessage().split()      

        first = True
        for word in words:
            if first and word[0] == '\x01':
                first = False
                continue

            word = word.lower()

            if word in self.exceptions:
                for cwords in [words_channel] + ([words_user] if logUser else []):
                    if word in cwords:
                        cwords[word] += 1
                    else:
                        cwords[word] = 1
                continue

            #remove text coloring characters
            word = re.sub("\x03\d\d?(,\d\d?)?", '', word)
                    
            word = word.lstrip(self.charIgnore).rstrip(self.charIgnore)
            for cwords in [words_channel] + ([words_user] if logUser else []):
                if word in cwords:
                    cwords[word] += 1
                else:
                    cwords[word] = 1

        with open(logpath,"w") as logFile:
            pickle.dump(words_channel,logFile)
        if logUser:
            with open(logpath_u,"w") as logFile:
                pickle.dump(words_user,logFile)
        
        return [""]

    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the picture module! Say !picture to see a piece of art made by you talking!"]
