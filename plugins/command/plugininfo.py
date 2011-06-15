# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import urllib2
import urllib
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        msg=complete.message()
        message=[]
        if msg in globalv.aliasExtensions:
            if globalv.aliasExtensions[msg]!="":
                message.append("PRIVMSG $C$ :"+msg+" is an alias to a plugin, with arguments: "+globalv.aliasExtensions[msg])
        try:
            output=globalv.loadedPlugins[msg].describe(complete)
            message+=output
        except:
            try:
                output=globalv.loadedRealtime[msg].describe(complete)
                message+=output
            except Exception as detail:
                print detail
                message.append("PRIVMSG $C$ :"+"Syntax: "+globalv.commandCharacter+complete.cmd()[0]+" [command]")
                plugins=globalv.loadedPlugins.keys()
                data={"paste_code":globalv.commandCharacter+", !".join(plugins),"paste_private":1,"paste_expire_date":"1H"} 
                data=urllib.urlencode(data)
                req = urllib2.Request("http://pastebin.com/api_public.php", data)
                response=urllib2.urlopen(req).read()
                message.append("PRIVMSG $C$ :Loaded commands: %s"%response)
        return message
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !help module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!help [plugin/alias]"]
