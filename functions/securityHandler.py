# -*- coding: utf-8 -*-
import globalv,re,settingsHandler
def isAllowed(nick):
    try:
        for mask in globalv.miscVars[2]:
            if re.search(mask[0].replace('[','\['), nick, re.I | re.DOTALL)!=None:
                return int(mask[1])
    except: 
        print "\x07"
        print mask
        print nick
    return 0

def isBanned(complete):
    toIgnore=[x[0] for x in settingsHandler.readSettingRaw("coreIgnorance","ignorance")]
    hostmasks=[mask for mask in toIgnore if mask.find("@")!=-1]
    try:
        channels=[channel.lower() for channel in toIgnore if channel[0]=="#"]
    except IndexError:
        print "Alert - ignorance failure, one of your ignrance entries is 0-length!"
        if isAllowed(complete.userMask())>=20:
            return 0
        else:
            return 1
    nick=complete.user()
    if isAllowed(complete.userMask())>=100:
        return 0
    if nick in globalv.miscVars[0]:
        for line in hostmasks:
            try:
                if re.match("^"+line.rstrip()+"$", globalv.miscVars[0][nick],re.I)!=None:
                    print "User is ignored"
                    return 1
                
            except Exception as detail:
                print "There is an invalid entry in your ignorance list"
                with open("crashLog.txt","a") as file:
                    file.write("\nSecurity Handler Failure: "+str(detail))
    if complete.channel().lower() in channels:
        if isAllowed(complete.userMask())>=10:
            print "Channel is ignored but user is above"
            return 0
        else:
            print "Channel is ignored"
            return 1
    return 0
