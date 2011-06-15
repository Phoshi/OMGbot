# -*- coding: utf-8 -*-
import globalv
import settingsHandler
import re
from commandParser import getArguments
from pluginArguments import pluginArguments
def formatOutput(text,args):
    newText=[]
    if type(text)!=list:
        text=[text]
    for lines in text:
        lines=lines.replace('$U$', args.user())
        lines=lines.replace('$C$', args.channel())
        newText.append(lines)
    return newText

def formatInput(arguments, aliases=globalv.aliasExtensions, preprocess=True):
    if settingsHandler.tableExists("'core-doNotExpand'")==False:
        settingsHandler.newTable("'core-doNotExpand'","doNotExpand")
    doNotExpand=[str(x[0]) for x in settingsHandler.readSettingRaw("'core-doNotExpand'","doNotExpand")]
    if aliases[arguments.cmd()[0]]!="":
        toAdd=aliases[arguments.cmd()[0]][1:]
        result=re.findall("\$([0-9][0-9]?[\+-]?)\$",toAdd)
        suchAThingExists=re.search('\$..?.?\$',toAdd)
        if result!=[]:
            for value in result:
                if value.find('+')==-1 and value.find('-')==-1:
                    if (len(arguments.cmd()))>int(value):
                        toAdd=toAdd.replace("$"+value+"$",arguments.cmd()[int(value)])
                    else:
                        if int(value)!=1:
                            toAdd=toAdd.replace("$"+value+"$"," ")
                        else:
                            toAdd=toAdd.replace("$"+value+"$",arguments.user())
                elif value.find('+')!=-1:
                    value=value[:-1]
                    if (len(arguments.cmd()))>(int(value)-1):
                        toAdd=toAdd.replace("$"+value+"+$",' '.join(arguments.cmd()[int(value):]))
                    else:
                        toAdd=toAdd.replace("$"+value+"+$"," ")
                elif value.find('-')!=-1:
                    value=value[:-1]
                    if (len(arguments.cmd()))>int(value):
                        toAdd=toAdd.replace("$"+value+"-$",' '.join(arguments.cmd()[1:][:int(value)]))
                    else:
                        toAdd=toAdd.replace("$"+value+"-$"," ")
        if toAdd.find('$*$')!=-1:
            toAdd=toAdd.replace('$*$',' '.join(arguments.cmd()[1:]))
        if toAdd.find('$URL$')!=-1:
            toAdd=toAdd.replace('$URL$',' '.join(arguments.cmd()[1:]).replace(' ','%20'))
        if suchAThingExists!=None:
            msg=globalv.commandCharacter+arguments.cmd()[0]+" "+toAdd
        else:
            msg=arguments.complete()[1:].split(' :',1)[1]+aliases[arguments.cmd()[0]]
        ret=arguments.complete()[1:].split(' :',1)
        ret[1]=msg
        arguments.setComplete(':'+' :'.join(ret))
    if arguments.cmd()[0] not in doNotExpand and preprocess:
        arguments=expand(arguments)

    return arguments
def expand(complete):
    print "Starting expansion of", complete.fullMessage()
    string=complete.fullMessage()
    while getArguments(string)!=[]:
        positions=getArguments(string)
        positions.sort(key=lambda list: list[0])
        positions.reverse()
        topDepth=positions[0][0]
        positions=filter(lambda position:position[0]==topDepth, positions)
        for position in positions:
            command=string[position[1]:position[2]][1:-1] #Extract the command/arguments and then cut off the $ delimiters.
            if '(' in command:
                command=command.split('(',1)
                command[-1]=command[-1][:-1]
                command=' '.join(command)
            string=list(string)
            for i in range(position[1], position[2]):
                del string[position[1]]
            expansions=dict(settingsHandler.readSettingRaw("'core-expansions'","trigger,command"))
            if command.split()[0] in globalv.loadedPlugins.keys() or command.split()[0] in expansions.keys():
                if command.split()[0] in expansions.keys():
                    command=expansions[command.split()[0]]
                inputString=":%s PRIVMSG %s :%s"%(complete.userMask(), complete.channel(), "!%s"%command)
                input=formatInput(pluginArguments(inputString))
                pluginOutput=globalv.loadedPlugins[command.split()[0]].action(input)
                pluginOutput=map(lambda output:output.split(' :',1)[1], pluginOutput)
                commandResult=' | '.join(pluginOutput)
            else:
                commandResult=command
            string.insert(position[1], str(commandResult))
            string=''.join(string)
    complete.setMessage(string)
    string=complete.fullMessage()
    for variable in globalv.variables.keys():
        if complete.fullMessage().find(variable)!=-1:
            string=re.sub("~%s~"%variable,str(globalv.variables[variable]),string)
            ret=complete.complete()[1:].split(' :',1)
            ret[1]=string
            complete.setComplete(':'+' :'.join(ret))
    return complete
def expandExpansions(toExpand, complete=None):
    def runPluginReturnOutput(matchObj):
        command=expanDict[matchObj.group(1)]
        if matchObj.group(2) is not None:
            arguments=matchObj.group(2)[1:-1]
        else:
            arguments=""
        appendOnto=True
        for index, content in enumerate(arguments.split()):
            if "$%s$"%index in command:
                command=command.replace("$%s$"%index, content)
                appendOnto=False
        if "$*$" in command:
            command=command.replace("$*$",arguments)
            appendOnto=False
        if appendOnto:
            command="%s %s"%(command, arguments)
        inputString=":%s PRIVMSG %s :%s"%(toExpand.userMask(), toExpand.channel(), "!%s"%command)
        input=formatInput(pluginArguments(inputString))
        pluginOutput=' | '.join(globalv.loadedPlugins[command.split()[0]].action(input))
        output=' :'.join(pluginOutput.split(' :')[1:])
        return output
    if type(toExpand) in [str,unicode]:
        isObj=False
    else:
        isObj=True
    if settingsHandler.tableExists("'core-expansions'")==False:
        settingsHandler.newTable("'core-expansions'","trigger","command")
    allCommands=[[x.replace('(','\(').replace(')', '\)'),x] for x in globalv.loadedPlugins.keys()]
    expansions=settingsHandler.readSettingRaw("'core-expansions'","trigger,command") + allCommands
    expanDict={}
    for trigger, command in expansions:
        expanDict[trigger]=command
        if isObj:
            string=toExpand.fullMessage()
            #if string.find("$%s$"%trigger)!=-1:
            if re.findall("(\$%s(\(.*?\))?\$)"%trigger, string)!=[]:
                string=re.sub("\$(%s)(\(.*?\))?\$"%trigger,runPluginReturnOutput,string)
                ret=toExpand.complete()[1:].split(' :',1)
                ret[1]=string
                toExpand.setComplete(':'+' :'.join(ret))
        else:
            if complete==None:
                usermask="dummy!dummy@dummy"
                channel="#dummy"
            else:
                usermask=complete.userMask()
                channel=complete.channel()
            #if toExpand.find("$%s$"%trigger)!=-1:
            if re.findall("(\$%s(\(.*?\))?\$)"%trigger, toExpand)!=[]:
                toExpand=re.sub("\$(%s)(\(.*?\))?\$"%trigger,runPluginReturnOutput,toExpand)
    for variable in globalv.variables.keys():
        if toExpand.fullMessage().find(variable)!=-1:
            string=re.sub("~%s~"%variable,str(globalv.variables[variable]),string)
            ret=toExpand.complete()[1:].split(' :',1)
            ret[1]=string
            toExpand.setComplete(':'+' :'.join(ret))
    return toExpand
