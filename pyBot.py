#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import sys
import traceback
import threading
import difflib
import Queue
import os
sys.path.insert(0, "functions")
sys.path.insert(0, os.path.join("plugins","realtime"))
sys.path.insert(0, os.path.join("plugins","command"))
sys.path.insert(0, os.path.join("plugins","input"))
sys.path.insert(0, os.path.join("plugins","postprocess"))
sys.path.insert(0, os.path.join("plugins","preprocess"))
sys.path.insert(0, "plugins")
import globalv
if len(sys.argv)>1:
    globalv.database=sys.argv[1]
    print "Using",globalv.database,"as coreDB"
import time
import random
import security
import pluginHandler
import aliasHandler 
import securityHandler
import settingsHandler
import shlex
from pluginArguments import pluginArguments
from pluginFormatter import formatOutput, formatInput
from asyncInputHandler import inputSystem
load_plugin=pluginHandler.load_plugin
unload_plugin=pluginHandler.unload_plugin
isAllowed=securityHandler.isAllowed
isBanned=securityHandler.isBanned
load_alias=aliasHandler.load_alias
save_alias=aliasHandler.save_alias

#local variables
on=1
lastChannelMessage=""
okToSend=False
nickname=settingsHandler.readSetting("core","nickname")
password=settingsHandler.readSetting("core","password")
owner=settingsHandler.readSetting("core","owner")
server=settingsHandler.readSetting("core","server")
port=int(settingsHandler.readSetting("core","port"))

#update global variables
globalv.nickname=nickname

#IRC protocol message type constants
privmsg="PRIVMSG"
notice="NOTICE"
nick="NICK"
motd="372"
motdEnd="001"
namesList="353"
namesListEnd="366"
NickInUse="433"
join="JOIN"
part="PART"
Null=0

#Define Local Classes
class asyncInput(object):
    def __init__(self,Queue, inputQueue):
        self.Queue=Queue
        while True:
            data = irc.recv(4096)
            self.Queue.put(data)
    def gettype(self):
        return "input"
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the main IRC input module"]

#Define local functions			
def sendithread(msg):
    outputQueue.put(msg)
def send(msg): #Sends the argument straight to the server
    def actuallySend(msg):
        starter=""
        if not okToSend and msg.split()[0]=="PRIVMSG":
            return
        if len(msg)>400: #If the length is greater than 200 characters, split it up into more messages (To avoid breaking!)
            starter=msg.split(':')[0]+":" #But we want to keep the message type (Which is almost certainly PRIVMSG, but still)
            start=msg.find(' ',390)
            omsg=msg[start:800]
            appendQueueMessage=False
            if len(msg)>800:
                globalv.outputQueue.append(starter+msg[800:])
                appendQueueMessage=True
            msg=msg[:start]
            if appendQueueMessage:
                msg+="\x02(More messages in queue - use !more to read)\x02"
        try:
            irc.send(msg.encode('utf-8') + "\r\n") #Yeah, I'm this lazy.
            if msg.split()[0] not in ["JOIN","WHOIS"] and msg.split(':',1)[-1].split()[0] not in ["\x01PING"]:
                time.sleep(1)
        except Exception as (errorNumber, error):
            print "X-- Send Failure!"
            print "X--",msg
            print "X--",error
            if errorNumber==32:
                sys.exit(0)
        if starter!="":
            time.sleep(1)
            send(starter+omsg.decode('utf-8')) #Recursive function, because we shouldn't need too many iterations and it's quicker than a for loop.
    if msg!=[""]:
        if type(msg) is list:
            if len(msg)>15:
                globalv.outputQueue+=msg[15:]
                msg=msg[:15]
            for line in msg:
                for plugin in globalv.loadedPostprocess.keys():
                    try:
                        line=globalv.loadedPostprocess[plugin].action(line)
                    except Exception as detail:
                        print "Postprocess failure in plugin", plugin, "because:", detail
                actuallySend(line)
        else:
            for plugin in globalv.loadedPostprocess.keys():
                try:
                    msg=globalv.loadedPostprocess[plugin].action(msg)
                except:
                    pass
            actuallySend(msg)



def message(msg, chan): #Shorthand to send a message to a particular channel
    send('PRIVMSG '+chan+' :'+msg) #Yes, I AM this lazy, actually.

def parse(msg):
    arguments=pluginArguments(msg)
    global load_plugin 
    global unload_plugin 
    global isAllowed 
    global isBanned 
    global load_alias 
    global save_alias 

    if not isBanned(arguments):
        if arguments.cmd()[0]=="reimportGlobalVariables" and arguments.user()=="PY":
            reload(globalv)
            reload(pluginHandler)
            reload(aliasHandler)
            reload(securityHandler)
            load_plugin=pluginHandler.load_plugin
            unload_plugin=pluginHandler.unload_plugin
            isAllowed=securityHandler.isAllowed
            isBanned=securityHandler.isBanned
            load_alias=aliasHandler.load_alias
            save_alias=aliasHandler.save_alias
            load_plugin("load")
            message("Reloaded globalv variables. You may encounter some slight turbulence as we update.",arguments.channel())
        elif arguments.cmd()[0] in globalv.loadedPlugins.keys():
            if arguments.cmd()[0] not in globalv.accessRights[arguments.user()]:
                try:
                    arguments=formatInput(arguments)
                    output=globalv.loadedPlugins[arguments.cmd()[0]].action(arguments)
                    output=formatOutput(output,arguments)
                    if type(output)==list:
                        output=[x for x in output if x!=""]
                    send(output)
                except Exception as detail:
                    print arguments.cmd()[0], "failed:",str(detail)
                    traceback.print_tb(sys.exc_info()[2])
            else:
                output=globalv.loadedPlugins[arguments.cmd[0]].disallowed(formatInput(arguments))
                send(formatOutput(lines,arguments))
        else:
            verboseAutoComplete = True if settingsHandler.readSetting("coreSettings", "verboseAutoComplete")=="True" else False
            if not verboseAutoComplete:
                return
            command=arguments.cmd()[0]
            nearMatches=difflib.get_close_matches(command, globalv.loadedPlugins.keys(), 6, 0.5)
            nearestMatch=difflib.get_close_matches(command, globalv.loadedPlugins.keys(),1,0.6)
            commandExists = os.path.exists(os.path.join("plugins","command",command+".py"))
            if nearMatches==[]:
                if not commandExists:
                    returns=["PRIVMSG $C$ :No such command!"]
                else:
                    returns=["PRIVMSG $C$ :Command not loaded!"]
            elif nearestMatch==[]:
                if not commandExists:
                    returns=["PRIVMSG $C$ :No such command! Did you mean: %s"%', '.join(nearMatches)]
                else:
                    returns=["PRIVMSG $C$ :Command not loaded! Did you mean: %s"%', '.join(nearMatches)]
            else:
                newArguments=arguments.complete()[1:]
                constructArguments=newArguments.split(' :',1)
                commands=constructArguments[1].split()
                commands[0]=globalv.commandCharacter+nearestMatch[0]
                constructArguments[1]=' '.join(commands)
                newArguments=':'+' :'.join(constructArguments)
                parse(newArguments)
                if len(nearMatches)>1:
                    returns=["PRIVMSG $C$ :(Command name auto-corrected from %s to %s [Other possibilities were: %s])"%(arguments.cmd()[0], nearestMatch[0], ', '.join(nearMatches[1:]))]
                else:
                    returns=["PRIVMSG $C$ :(Command name auto-corrected from %s to %s)"%(arguments.cmd()[0], nearestMatch[0])]



            send(formatOutput(returns, arguments))


if __name__=="__main__":
    #Load plugins and aliases.
    print "Loading plugins..."
    for plugin, loadAs in globalv.pluginList:
        load_plugin(plugin, loadAs)
    print "Loading aliases..."
    for line in settingsHandler.readSetting("alias","aliasName, aliasPlugin, aliasArguments"):
        load_alias(line[0], ' '.join(line[1:]))
    print "Loading input sources..."
    if settingsHandler.tableExists("'core-input'"):
        for input in settingsHandler.readSettingRaw("'core-input'","input, definition"):
            if input[0] not in globalv.loadedInputs.keys():
                x=__import__(str(input[1].split()[0]))
                reload(x)
                arguments=str(' '.join(input[1].split()[1:]))
                arguments=arguments.split()
                globalv.loadedInputs[input[0]]=globalv.input.addInputSource(x.asyncInput,tuple(arguments))
            else:
                globalv.loadedInputs[input[0]].put(str(input[1]))
    else:
        settingsHandler.newTable("'core-input'","input", "definition")
    for input in globalv.loadedInputs.keys():
        globalv.loadedInputs[input].put("--init--")
    globalv.input.addInputSource(asyncInput)
    print "Loading output threads..."
    #outputQueue=Queue.Queue(10)
    #outputThread=threading.Thread(target=asyncOutput, args=(outputQueue,))
    #outputThread.start()
    #initialise connection
    irc = socket.socket (socket.AF_INET,socket.SOCK_STREAM) #Initialise the socket prior to connection
    irc.settimeout(380)#So we time-out when we time-out.
    print "Connecting to %s:%s..."%(server, port)
    irc.connect ((server,port)) #Connect!
    #irc.recv(4096) #Grab the hostname auth message to assure connection was successful.
    print "Connection Succesful!"
    globalv.input.startInputDaemons()
    send ('USER '+nickname+' * * :'+owner) #Tell the IRC server who we are
    send ('NICK '+nickname) #And what we're called.
    while on==1:
        try:
            if globalv.input.getPrimaryProducerStatus()==False:
                sys.exit(0)
            data = globalv.input.getInput()
            for datum in data.split('\r\n')[0:-1]:
                if datum[:1]!="#":
                    for plugin in globalv.loadedPreprocess.keys():
                        try:
                            datum=globalv.loadedPreprocess[plugin].action(pluginArguments(datum))
                        except Exception as detail:
                            print plugin, "failed:",detail
                            traceback.print_tb(sys.exc_info()[2])
                    if datum=="":
                        break
                    arguments=pluginArguments(datum)
                    for plugin in sorted(globalv.loadedRealtime.keys()):
                        try:
                            output=globalv.loadedRealtime[plugin].action(arguments)
                            send(formatOutput(output,arguments))
                        except Exception as detail:
                            print plugin, "failed:",str(detail)
                            traceback.print_tb(sys.exc_info()[2])
                    if datum.split()[0]=="ERROR":
                            sys.exit(0)
                    if datum.split()[0]=="PING":
                        send("PONG "+datum.split(':')[1])
                    if len(datum.split())>1:
                        if datum.split()[1]==NickInUse:
                            send("NICK SomebodyStole"+nickname+str(random.randint(0,50)))
                        if datum.split()[1]==motdEnd:
                            okToSend=True
                            send("NICKSERV IDENTIFY "+password)
                            for channel in globalv.channels:
                                send("JOIN "+channel)
                        if datum.split()[1]=="TOPIC":
                            globalv.miscVars[4].update({datum.split()[2]:' '.join(datum.split()[1:]).split(':',1)[1:]}) #Update the channel:topic disctionary whenever we get a topic change message
                        if datum.split()[1]=="332":
                            globalv.miscVars[4].update({datum.split()[3]:' '.join(datum.split()[1:]).split(':',1)[1:]}) #There are two different types of topic change message.
                        if datum.split()[1]==privmsg:
                            complete=datum[1:].split(' :',1) #Parse into [data, message] format
                            if complete[0].split()[0].split('!')[0] in globalv.miscVars[0].keys():
                                settingsHandler.updateSetting("'core-nickmasks'","hostmask",complete[0].split()[0].split('!')[1],where="nick='%s'"%complete[0].split()[0].split('!')[0])
                            else:
                                nickInfo=complete[0].split()[0].split('!')
                                settingsHandler.writeSetting("'core-nickmasks'",["nick","hostmask"],[nickInfo[0],nickInfo[1]])
                            stuff=datum.split()[0].split(':', 1)[1].split('!')
                            globalv.miscVars[0].update({stuff[0]:stuff[1]})
                            if stuff[0] not in globalv.accessRights.keys():
                                globalv.accessRights[stuff[0]]=security.accessRight(stuff[0])
                            if len(complete)>1:
                                if complete[1].startswith(globalv.commandCharacter):
                                    try:
                                        parse(datum)
                                    except Exception as detail:
                                        print "Base Plugin Exection Failure:",detail
                                        traceback.print_tb(sys.exc_info()[2])
                        elif datum.split()[1]==join:
                            stuff=datum.split()[0].split(':', 1)[1].split('!')
                            globalv.miscVars[0].update({stuff[0]:stuff[1]})
                        elif datum.split()[1]==nick and datum.split()[0].split('!')[0].split(':')[1]==globalv.nickname:
                            globalv.nickname=datum.split(':')[2]
                        else:
                            complete=datum[1:].split(' :',1) #Parse into [data, message] format
                            for plugin in globalv.loadedSpecial.keys():
                                try:
                                    output=globalv.loadedSpecial[plugin].action(arguments)
                                    send(formatOutput(output,arguments))
                                except Exception as detail:
                                    print plugin, "failed:",str(detail)
                                    traceback.print_tb(sys.exc_info()[2])
                else:
                    send(datum[1:])
        except KeyboardInterrupt:
            on=0
            send("QUIT :^c at console")
        except Exception as detail:
            print "System Failure:",detail
            with open("crashLog.txt","a") as file:
                file.write("\nCrashed! Reason: "+str(detail))
            send("QUIT :%s"%detail)
            raise
            sys.exit()
        #finally:
            #irc.close()
