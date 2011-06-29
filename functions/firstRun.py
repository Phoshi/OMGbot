import settingsHandler
import pickle
import os
def createDatabase():
    settingsHandler.newTable("core", "nickname", "password", "owner", "server", "port")
    newName = raw_input("Bot Name? ")
    newPassword = raw_input("Nickname password? ")
    newOwner = raw_input("Owner name? ")
    newServer = raw_input("Connect to what server? ")
    newPort = raw_input("On what port (6667 is standard)? ")
    settingsHandler.writeSetting("core", ["nickname", "password", "owner", "server", "port"],
            [newName, newPassword, newOwner, newServer, newPort])
    settingsHandler.newTable("'core-nickmasks'", "nick", "hostmask")
    newChannel = raw_input("Channel to auto-join? ")
    settingsHandler.newTable("coreAutoJoin", "channel")
    settingsHandler.writeSetting("coreAutoJoin", ["channel"], [newChannel])

    settingsHandler.newTable("alias", "aliasName", "aliasPlugin", "aliasArguments")
    settingsHandler.newTable("'core-userlevels'", "plugin", "level")
    settingsHandler.newTable("coreIgnorance", "ignorance", "nickname")
    settingsHandler.newTable("'core-input'", "input", "definition")
    settingsHandler.newTable("'core-expansions'", "trigger", "command")
    settingsHandler.newTable("'core-doNotExpand'", "doNotExpand")
    settingsHandler.newTable("autoidentifyd", "nickname", "level")
    settingsHandler.writeSetting("autoidentifyd", ["nickname", "level"], [newOwner, "1000"])


def createVariables():
    with open(os.path.join("config","variables"),'w') as file:
        pickle.dump({},file,pickle.HIGHEST_PROTOCOL)

def createAutoload():
    settingsHandler.newTable("coreAutoLoad", "plugin", "loadAs")
    settingsHandler.writeSetting("coreAutoLoad", ["plugin", "loadAs"], ["load", "load"])
    settingsHandler.writeSetting("coreAutoLoad", ["plugin", "loadAs"], ["autoidentifyd", "autoidentifyd"])
