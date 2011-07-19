# -*- coding: utf-8 -*-
from plugins import plugin
from pluginArguments import pluginArguments
from pluginFormatter import formatInput, formatOutput
import globalv
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        msg=complete.message()
        output=msg.split('>')[-1]
        if output==msg or len(output.split())!=1:
            output="$C$"
        else:
            msg=msg.split('>')[0]
        commandlist=msg.split('&&')
        returns=[]
        for msg in commandlist:
            msg=msg.replace('\|','__PIPE__')
            commands=msg.split('|')
            commands=map(lambda x: x.replace('__PIPE__','|'), commands)
            pluginOutput=""
            for command in commands:
                plugin=command.split()[0]
                args=' '.join(command.split()[1:])
                if globalv.loadedPlugins[plugin].__append_seperator__()==True:
                    args+="::"
                args+=pluginOutput
                arguments=pluginArguments(complete.complete())
                print "======", arguments.complete()
                firstBit=arguments.complete().split(' :')[0]
                arguments.setComplete(":"+firstBit+" :"+globalv.commandCharacter+plugin+" "+args)
                arguments=formatInput(arguments)
                pluginOutput=globalv.loadedPlugins[plugin].action(arguments)
                print pluginOutput
                if pluginOutput!=[""]:
                    starter=pluginOutput[0].split(' :')[0]
                    print starter
                    if starter.split()[0]=="PRIVMSG":
                        content=""
                        pluginOutput=[x for x in pluginOutput if x!=""]
                        for i,line in enumerate(pluginOutput):
                            content+=' :'.join(line.split(' :')[1:])+(" | " if i!=len(pluginOutput)-1 else "")
                            print content
                        pluginOutput=starter+(' :'+content if content!="" else "")
                        pluginOutput=' :'.join(pluginOutput.split(' :')[1:]) if command!=commands[-1] else pluginOutput
                        print pluginOutput
                else:
                    pluginOutput=""

            if type(pluginOutput)!=list:
                pluginOutput=pluginOutput.replace('$C$', output)
            else:
                pluginOutput=[x.replace('$C$', output) for x in pluginOutput]
            outputstr=formatOutput(pluginOutput,complete)
            if outputstr!="":
                #returns.append(outputstr)
                returns+=outputstr
        return returns
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
