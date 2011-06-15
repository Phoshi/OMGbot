# -*- coding: utf-8 -*-
import settingsHandler
def getLevel(*pluginName):
    try:
        level=settingsHandler.readSetting("'core-userlevels'", "level", where="plugin='%s'"%pluginName[0])
        if level==[]:
            level=0
        else:
            level=int(level)
        return level
    except Exception as detail:
        print "An Exception Occured grabbing the user requirements for",pluginName,":"+str(detail)
        return 10000
