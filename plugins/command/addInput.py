# -*- coding: utf-8 -*-
from plugins import plugin
from settingsHandler import readSetting
from pluginHandler import load_plugin, unload_plugin
from aliasHandler import load_alias
from securityHandler import isAllowed
from userlevelHandler import getLevel
import settingsHandler
import globalv
import sys
import shlex
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def __level__(self):
        return 150
    def action(self, complete):
        name=complete.message()
        msg="There was an error in your input!"
        if isAllowed(complete.userMask())<getLevel(complete.cmd()[0]):
            return [""]
        if name.split()[0]=="list":
            return ["PRIVMSG $C$ :"+' '.join(globalv.loadedInputs.keys())]
        elif name.split()[0]=="clean":
            newDict={}
            for plugin in globalv.loadedInputs.keys():
                if globalv.loadedInputs[plugin].isSet()==False:
                    newDict[plugin]=globalv.loadedInputs[plugin]
            globalv.loadedInputs=newDict
            return ["PRIVMSG $C$ :ID list cleaned up manually"]
        elif name.split()[0]=="kickstart":
            globalv.input.startInputDaemons()
            return ["PRIVMSG $C$ :Kickstarted stalling plugins manually"]
        elif name.split()[0]=="reboot":
            definition=settingsHandler.readSetting("'core-input'","definition",where="input='%s'"%name.split()[1])
            print "def"
            x=__import__(str(definition.split()[0]))
            reload(x)
            arguments=str(' '.join(definition.split()[1:]))
            arguments=shlex.split(arguments)
            globalv.loadedInputs[name.split()[1]]=globalv.input.addInputSource(x.asyncInput,tuple(arguments))
            globalv.input.startInputDaemons()
            msg="Rebooting input plugin..."
        elif name.split()[0]=="add":
            name= ' '.join(name.split()[1:])
            try:
                if name.split()[0] in globalv.loadedInputs.keys():
                    raise Exception("An input module with that ID already exists!")
                x=__import__(name.split()[1])
                reload(x)
                arguments=shlex.split(' '.join(name.split()[2:]))
                globalv.loadedInputs[name.split()[0]]=globalv.input.addInputSource(x.asyncInput,tuple(arguments))
                print arguments
                settingsHandler.writeSetting("'core-input'", ["input", "definition"], [name.split()[0], ' '.join(name.split()[1:])])
                globalv.input.startInputDaemons()
                msg="Plugin loaded successfully!"
            except Exception as detail:
                msg="Load failure: "+str(detail)
        elif name.split()[0]=="send":
            plugin = name.split()[1]
            command = " ".join(name.split()[2:])
            globalv.loadedInputs[plugin].put(command)
            msg = "Sent message to plugin"
        elif name.split()[0]=="autosend":
            name= ' '.join(name.split()[1:])
            settingsHandler.writeSetting("'core-input'", ["input", "definition"], [name.split()[0], ' '.join(name.split()[1:])])
            msg = "Plugin configuration added"
        elif name.split()[0]=="unautosend":
            settingsHandler.deleteSetting("'core-input'", "definition", ' '.join(name.split()[1:]))
            msg="Configuration removed!"
        return ["PRIVMSG $C$ :"+msg]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !addInput module!","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!addInput [name] [plugin name] [arguments to plugin]"]
