# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import os
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        msg=[x for x in str(complete.message())]
        file=open(os.path.join("config","russian.txt"),'r').read()
        file=file.split('\n\n\n')
        lowercase=file[0].split('\n\n')
        lowercase=[x.split('\n') for x in lowercase]
        uppercase=file[1].split('\n\n')
        uppercase=[x.split('\n') for x in uppercase]
        print lowercase
        for letter in range(len(msg)):
            if msg[letter] in lowercase[0]:
                msg[letter]=lowercase[1][lowercase[0].index(msg[letter])]
            if msg[letter] in uppercase[0]:
                msg[letter]=uppercase[1][uppercase[0].index(msg[letter])]
        print msg
        return ["PRIVMSG $C$ :"+''.join(msg).decode('utf-8')]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
