# -*- coding: utf-8 -*-
from plugins import plugin
import globalv,glob,os
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        ignoreThese=["aliases","blank","globalv","plugins","security","bitlyServ"]
        files=[]
        for file in glob.glob(os.path.join("plugins","*.py")):
            file=file.split(os.path.sep)[1].split('.')[0]
            if (file not in globalv.loadedPlugins.keys() and file not in globalv.loadedRealtime.keys() and file not in globalv.loadedSpecial.keys() and file not in ignoreThese):
                files.append(file)
        return ["PRIVMSG $C$ :Currently unloaded plugins are: "+', '.join(files)]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !unloaded module, I list plugins that aren't loaded - but could be.","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!unloaded"]
