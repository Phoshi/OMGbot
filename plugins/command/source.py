# -*- coding: utf-8 -*-
from plugins import plugin
import globalv, urllib2,urllib
import os
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        msg=complete.message()
        readFile=""
        if msg=="":
            return ["PRIVMSG $C$ :https://github.com/Phoshi/OMGbot"]
        if msg.find('.')==-1:
            if msg=="OMGbot": msg="../../pyBot"
            for plugindir in ["command","realtime", "postprocess", "preprocess", "input","../functions"]:
                if os.path.exists(os.path.join("plugins", plugindir, msg+".py")):
                    with open(os.path.join("plugins",plugindir,msg+".py")) as file:
                        readFile=file.read()
                        break
            if readFile=="":
                return ["PRIVMSG $C$ :No plugin by that name exists - are you trying to source an alias?"]
            data={"paste_code":readFile}
            data=urllib.urlencode(data)
            req = urllib2.Request("http://pastebin.com/api_public.php", data)
            response = urllib2.urlopen(req)
            msg=response.read()
            return ["PRIVMSG $C$ :"+msg]
        else:
            return ["PRIVMSG $C$ :Incorrect syntax! source [plugin name]"]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !source module. I return a pastebin URL with the source of a plugin.","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!source [plugin name]"]
