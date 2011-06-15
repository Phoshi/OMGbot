# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
from securityHandler import isAllowed
from userlevelHandler import getLevel
import re
import random
import settingsHandler
import os
import urllib
import urllib2
class pluginClass(plugin):
    def __level__(self):
        return 50
    def __init_db_tables__(self, name):
        settingsHandler.newTable(name, "quotesLocation", "userRequirementAdd","userRequirementRemove")
        settingsHandler.writeSetting(name,["quotesLocation","userRequirementAdd","userRequirementRemove"],[name,"None","elevated"])
    def gettype(self):
        return "command"
    def action(self, complete):
        msg=complete.message()
        nick=complete.userMask()
        sender=complete.channel()
        amsg=msg
        if not os.path.exists(os.path.join("config",settingsHandler.readSetting(complete.cmd()[0],"quotesLocation")+".txt")):
            file=open(os.path.join("config",settingsHandler.readSetting(complete.cmd()[0],"quotesLocation")+".txt"),"w")
            file.close()
        if msg=="":
            zozo = open(os.path.join("config",settingsHandler.readSetting(complete.cmd()[0],"quotesLocation")+".txt"), 'r')
            lines = zozo.read()
            zozo.close()
            lines=lines.split('\n\n')[:-1]
            retNum=random.randint(0,len(lines)-1)
            returner=["PRIVMSG $C$ :Quote #"+str(retNum+1)+" of "+str(len(lines))+":"]
            for line in lines[retNum].split('\n'):
                returner.append("PRIVMSG $C$ :"+str(line))
            return returner
        elif msg.split()[0].isdigit():
            msg=msg.split()[0]
            quotes = open(os.path.join("config",settingsHandler.readSetting(complete.cmd()[0],"quotesLocation")+".txt"), 'r')
            lines = quotes.read()
            quotes.close()
            lines=lines.split('\n\n')[:-1]
            retNum=int(msg)
            if retNum>len(lines):
                return ["PRIVMSG $C$ :There is no quote #"+str(retNum)]
            returner=["PRIVMSG $C$ :Quote #"+str(retNum)+" of "+str(len(lines))+":"]
            for line in lines[retNum-1].split('\n'):
                returner.append("PRIVMSG $C$ :"+str(line.decode('utf-8')))
            return returner
        elif msg.split()[0]=="modify":
            quoteNum=int(msg.split()[1])-1
            toAppend=' '.join(msg.split()[2:])
            quotes = open(os.path.join("config",settingsHandler.readSetting(complete.cmd()[0],"quotesLocation")+".txt"), 'r')
            lines = quotes.read()
            quotes.close()
            lines=lines.split('\n\n')[:-1]
            if int(quoteNum)>len(lines):
                return ["PRIVMSG $C$ :There is no quote #"+str(retNum)]
            lines[int(quoteNum)]=toAppend.replace('| ','\n')
            quotes = open(os.path.join("config",settingsHandler.readSetting(complete.cmd()[0],"quotesLocation")+".txt"), 'w')
            quotes.write('\n\n'.join(lines)+'\n\n')
            quotes.close()
            return ["PRIVMSG $C$ :Modified that quote!"] 

        elif msg.split()[0]=="append":
            quoteNum=int(msg.split()[1])-1
            toAppend=' '.join(msg.split()[2:])
            quotes = open(os.path.join("config",settingsHandler.readSetting(complete.cmd()[0],"quotesLocation")+".txt"), 'r')
            lines = quotes.read()
            quotes.close()
            lines=lines.split('\n\n')[:-1]
            if int(quoteNum)>len(lines):
                return ["PRIVMSG $C$ :There is no quote #"+str(retNum)]
            lines[int(quoteNum)]+=toAppend.replace('| ','\n')
            quotes = open(os.path.join("config",settingsHandler.readSetting(complete.cmd()[0],"quotesLocation")+".txt"), 'w')
            quotes.write('\n\n'.join(lines)+'\n\n')
            quotes.close()
            return ["PRIVMSG $C$ :Appended onto that quote!"] 

        elif msg.split()[0].lower()=="dump":
            quotes = open(os.path.join("config",settingsHandler.readSetting(complete.cmd()[0],"quotesLocation")+".txt"), 'r')
            data={"paste_code":quotes.read()}
            data=urllib.urlencode(data)
            req = urllib2.Request("http://pastebin.com/api_public.php", data)
            response = urllib2.urlopen(req)
            msg=response.read()
            return ["PRIVMSG $C$ :"+msg]
        else:
            allowedRemove=(isAllowed(nick)>=getLevel(complete.cmd()[0])) if settingsHandler.readSetting(complete.cmd()[0],"userRequirementRemove")=="elevated" \
                    else complete.user()==settingsHandler.readSetting("core","owner") if settingsHandler.readSetting(complete.cmd()[0],"userRequirementRemove")=="owner" else 1
            allowedAdd=(isAllowed(nick)>=getLevel(complete.cmd()[0])) if settingsHandler.readSetting(complete.cmd()[0],"userRequirementAdd")=="elevated" \
                    else complete.user()==settingsHandler.readSetting("core","owner") if settingsHandler.readSetting(complete.cmd()[0],"userRequirementAdd")=="owner" else 1
            if msg.split()[0].lower()=="remove" and allowedRemove:
                with open(os.path.join("config",settingsHandler.readSetting(complete.cmd()[0],"quotesLocation")+".txt"), 'r') as file:
                    lines = file.read()
                lines=lines.split('\n\n')
                lines.pop(int(msg.split()[1])-1)
                with open(os.path.join("config",settingsHandler.readSetting(complete.cmd()[0],"quotesLocation")+".txt"),'w') as file:
                    file.write('\n\n'.join(lines))
                return ["PRIVMSG $C$ :Alright, removed that quote!"]
            elif msg.split()[0].lower()=="add" and allowedAdd:
                msg=' '.join(msg.split()[1:])
                zozo = open(os.path.join("config",settingsHandler.readSetting(complete.cmd()[0],"quotesLocation")+".txt"), 'r')
                lines = zozo.read()
                zozo.close()
                lines=lines.split('\n\n')
                fullCMD=msg.replace(' | ','\n')
                file = open(os.path.join("config",settingsHandler.readSetting(complete.cmd()[0],"quotesLocation")+".txt"), 'a')
                file.write(fullCMD + "\n\n")
                file.close()
                return ["PRIVMSG $C$ :Quote added as #"+str(len(lines))]
        if len(msg.split())>0:
            with open(os.path.join("config",settingsHandler.readSetting(complete.cmd()[0],"quotesLocation")+".txt"), 'r') as file:
                fileLines = file.read()
            lines=[]
            for index, line in enumerate(fileLines.split('\n\n')):
                lines.append((index, line))
            random.shuffle(lines)
            if msg.split()[0]=="find":
                searchFor=' '.join(msg.lower().split()[1:])
            else:
                searchFor=msg

            for index, line in lines:
                if line.lower().find(searchFor)!=-1:
                    returner=[]
                    returner.append("PRIVMSG $C$ :Quote #%s of %s:"%(index+1, len(lines)-1))
                    for l in line.split('\n'):
                        returner.append("PRIVMSG $C$ :"+l)
                    return returner
            return ["PRIVMSG $C$ :No quotes matching your input!"]
        return ["PRIVMSG $C$ :The input you have given is invalid! Try !help :)"]
    def describe(self, complete):
        msg=complete.message()
        sender=complete[0].split(' ')
        sender=sender[2]
        return ["PRIVMSG $C$ :I am the !quote module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!quote [add/remove/quote index/blank] [OPTIONAL quote text or index to remove]"]
