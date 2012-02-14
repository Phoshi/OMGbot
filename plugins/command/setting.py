# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import settingsHandler
from securityHandler import isAllowed
from userlevelHandler import getLevel
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def __level__(self):
        return 100
    def action(self, complete):
        msg=complete.message()
        returns="Setting set, cap'n!"
        mode=plugin=setting=set=where=""
        mode=msg.split()[0]
        plugin=msg.split()[1]
        try:
            setting=msg.split()[2]
        except:
            setting=""
        try:
            set=' '.join(msg.split()[3:])
        except:
            set=""
        if len(set.split())<3:
            where = '1==1'
        elif set.split()[-2]=="WHERE":
            where=set.split()[-1]
            set=' '.join(set.split()[:-2])
        else:
            where="1==1"
        if isAllowed(complete.userMask())>=getLevel(complete.cmd()[0]):
            if mode=="update":
                settingsHandler.updateSetting(plugin, setting, set, where=where)
                returns="Setting updated, sir!"
            if mode=="delete":
                settingsHandler.deleteSetting(plugin, setting, set)
                returns="Setting removed, my lord!"
            if mode=="add":
                setting=setting.split('||')
                set=set.split('||')
                settingsHandler.writeSetting(plugin, setting, set)
                returns="Setting Set, Cap'n!"
            if mode=="drop-table":
                settingsHandler.dropTable(plugin)
                returns="Settings lost, comrade!"
            if mode=="list":
                columns=settingsHandler.readColumns(plugin)
                returns=', '.join(columns) 
            if mode=="current":
                results=settingsHandler.readSetting(plugin, setting)
                results=[str(x[0]) if len(x)==1 and type(x)==tuple else x for x in results] if type(results)==list else str(results)
                results=', '.join(results) if type(results)==list else results
                returns=results
            if mode=="commit":
                settingsHandler.db.commit()
                returns="Committed!"
            if mode=="copy":
                settingsHandler.executeQuery("INSERT INTO '%s' SELECT * FROM '%s'"%(msg.split()))
            if mode=="query":
                results=settingsHandler.executeQuery(' '.join(msg.split()[1:]))
                if results!=[]:
                    returns=str(results)
        else:
            returns="Sorry, you can't do this."
        return ["PRIVMSG $C$ :"+returns]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !settings module. I set settings.","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!setting [update|add|current|list] [plugin] [OPTIONAL field] [OPTIONAL value] [OPTIONAL WHERE clause"]
