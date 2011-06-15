# -*- coding: utf-8 -*-
from plugins import plugin
import settingsHandler
import globalv
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        msg=complete.message()
        plugins=settingsHandler.readSetting("'core-userlevels'","plugin,level")
        returner=[]
        output=[]
        if msg=="":
            for plugin, level in plugins:
                if int(level)>0:
                    returner.append(':'.join((plugin,level)))
                out=', '.join(returner)
            output.append("PRIVMSG $C$ :"+out)
            output.append("PRIVMSG $C$ :All other functions do not require elevation")
        elif msg.split()[0]=="-list":
            if len(msg.split())==1:
                for plugin, level in plugins:
                    returner.append(':'.join((plugin,level)))
                out=', '.join(returner)
                output.append("PRIVMSG $C$:"+out)
            else:
                yes=[]
                no=[]
                if msg.split()[1].isdigit():
                    userlevel=int(msg.split()[1])
                else:
                    userlevel=settingsHandler.readSetting("autoidentifyd","level",where="nickname='%s'"%msg.split()[1])
                    if userlevel==[]:
                        userlevel="0"
                    userlevel=int(userlevel)
                for plugin, level in plugins:
                    if len(msg.split())!=2 or int(level)>0:
                        if int(level)>userlevel:
                            no.append(plugin)
                        else:
                            yes.append(plugin)
                output.append("PRIVMSG $C$ :Can use: "+', '.join(yes))
                output.append("PRIVMSG $C$ :Can not use: "+', '.join(no))
                if userlevel>=100:
                    output.append("PRIVMSG $C$ :Can not be ignored.")
                elif userlevel>=20:
                    output.append("PRIVMSG $C$ :Channelwide ignores will not take effect.")
                else:
                    output.append("PRIVMSG $C$ :All ignores take effect")

        elif msg.split()[0] in globalv.loadedPlugins.keys():
            if len(msg.split())==1:
                for plugin, level in plugins:
                    if plugin.lower()==msg.split()[0].lower():
                        output.append("PRIVMSG $C$ :"+plugin+":"+level)
            elif msg.split()[1].isdigit():
                settingsHandler.updateSetting("'core-userlevels'","level", msg.split()[1], where="plugin='%s'"%msg.split()[0])
                output.append("PRIVMSG $C$ :Altered access requirements for that plugin")
            elif msg.split()[1] in globalv.loadedPlugins.keys():
                 for plugin, level in plugins:
                    if plugin.lower()==msg.split()[1].lower():
                        newLevel=level
                        break
                 settingsHandler.updateSetting("'core-userlevels'","level", newLevel, where="plugin='%s'"%msg.split()[0])
                 output.append("PRIVMSG $C$ :Equalised plugin requirements")

        return output
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
