# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import settingsHandler
import datetime
from pluginArguments import pluginArguments
from pluginFormatter import formatOutput, formatInput
import time
def getMessage(id):
    return settingsHandler.readSetting("laterd","message",where="id='%s'"%id)
def getRecipient(id):
    return settingsHandler.readSetting("laterd","recipient",where="id='%s'"%id)
def getSender(id):
    return settingsHandler.readSetting("laterd","sender",where="id='%s'"%id)
def getSenderMask(id):
    return settingsHandler.readSetting("laterd","senderMask",where="id='%s'"%id)
def getTimestamp(id):
    return datetime.datetime.fromtimestamp(int(settingsHandler.readSetting("laterd","timestamp",where="id='%s'"%id)))
def getAnonymous(id):
    return settingsHandler.readSetting("laterd","anonymous",where="id='%s'"%id)=="1"
def correctChannel(id, channel):
    messageChannel=settingsHandler.readSetting("laterd", "channel", where="id='%s'"%id)
    return (channel.lower() in [messageC.lower() for messageC in messageChannel.split('|')] or messageChannel=="")
def setMessageSent(id):
    print "Attempting to set complete"
    settingsHandler.updateSetting("laterd", "sent", "1", where="id='%s'"%id)
    print "Set complete!"

def totalSeconds(td):
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6

def GetTimeUntilDatetime(toDiff):
    times = [
            ("week", 7 * 24 * 60 * 60), 
            ("day", 24 * 60 * 60),
            ("hour", 60*60), 
            ("minute", 60)
            ]
    difference = totalSeconds((toDiff - datetime.datetime.now()))
    isFuture = difference > 0
    difference = abs(difference)
    timeDif = [0, 0, 0, 0]
    retString = []

    for timeIndex, timeEntry in enumerate(times):
        while difference > timeEntry[1]:
            difference-=timeEntry[1]
            timeDif[timeIndex]+=1
        if (timeDif[timeIndex] > 0):
            retString.append("%s %s%s"%(str(timeDif[timeIndex]), timeEntry[0], ("s" if timeDif[timeIndex]!=1 else "")))


    if (difference > 0):
        retString.append("%s %s%s"%(str(int(difference)), "second", ("s" if difference!=1 else "")))

    if len(retString) > 1:
        retString = ", ".join(retString[:-1]) + " and " + retString[-1]
    else:
        retString = retString[0]
    if not isFuture:
        retString += " ago"
    return retString

class pluginClass(plugin):
    def gettype(self):
        return "realtime"
    def __init_db_tables__(self, name):
        settingsHandler.newTable("laterd", "id", "recipient","sender","senderMask","timestamp","message", "channel", "anonymous",  "sent")
    def action(self, complete):
        user=complete.user()
        if complete.type()!="PRIVMSG":
            return [""]
        returns=[]
        messages=settingsHandler.readSettingRaw("laterd","id",where="('"+user.lower()+"' GLOB recipient OR recipient GLOB '*|"+user.lower()+"|*') AND sent='0'")
        if messages!=[]:
            for message in messages:
                wipeMessage=True

                messageID=str(message[0])
                try:
                    sender=getSender(messageID)
                    senderMask=getSenderMask(messageID)
                    timestamp=getTimestamp(messageID)
                    messageText=getMessage(messageID)
                    plugin=messageText.split()[0]
                    if not correctChannel(messageID, complete.channel()):
                        continue
                    if plugin in globalv.loadedPlugins.keys():
                        arguments=pluginArguments(':'+senderMask+" PRIVMSG "+complete.channel()+" :!"+messageText.replace('$recipient$', user).replace('$*$', complete.fullMessage()))
                        arguments=formatInput(arguments)
                        message=globalv.loadedPlugins[plugin].action(arguments)
                        if message in [[],[""]]:
                            wipeMessage=False
                        #returns+=[m.decode('utf-8') for m in message]
                        returns+=message
                        if message!=[""] and message!=[]:
                            msg=message[0]
                            if msg.split()[0]=="PRIVMSG" or msg.split()[0]=="NOTICE":
                                location=msg.split()[1]
                            else:
                                location="$C$"
                            if not getAnonymous(messageID):
                                returns.append("PRIVMSG "+location+" :From "+sender+" to "+user+" "+GetTimeUntilDatetime(timestamp))
                        if wipeMessage:
                            setMessageSent(messageID)
                    else:
                        returns.append("PRIVMSG $C$ :"+messageText)
                        if not getAnonymous(messageID):
                            returns.append("PRIVMSG $C$ :From "+sender+" to "+user+" "+GetTimeUntilDatetime(timestamp))
                        setMessageSent(messageID)
                    if len(returns) >= 13:
                        break
                except Exception as detail:
                    print "There was an error in one of the later messages:",detail
                    setMessageSent(messageID)

        return returns
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
