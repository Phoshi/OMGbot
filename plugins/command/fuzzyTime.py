# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        def makeFuzzyTime(hour, minute):
            minuteMessages=[(range(0,5),"%s o'clock"), (range(5,10),"five past %s"), (range(10,15), "ten past %s"), \
            (range(15,20),"quarter past %s"), (range(20,25), "twenty past %s"), (range(25,30), "twenty five past %s"), (range(30,35), "half past %s"), \
            (range(35,40), "twenty five to %s"), (range(40,45), "twenty to %s"), (range(45, 50), "quarter to %s"), (range(50,55), "ten to %s"), \
            (range(55,60), "five to %s")]
            hourNames=["midnight", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", \
            "eleven", "noon", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven"]
            minuteMessages=map(lambda tup: list(tup), minuteMessages)
            for message in minuteMessages:
                message[0]=tuple(map(lambda x: x-2, list(message[0])))
                message[0]=tuple(map(lambda x: x+60 if x<0 else x, list(message[0])))
                if minute in message[0]:
                    if minute > 33: #35 minutes to end "half past", plus the two minute wiggle room
                        hour+=1
                        if hour>23:
                            hour=0
                    if message[1]=="%s o'clock" and hour in [0, 12] and minute in minuteMessages[0][0]:
                        return hourNames[hour]
                    return (message[1]%hourNames[hour]) + (" AM" if 0 < hour < 12 else "" if 12 < hour else "")
        hour=int(complete.message().split(':')[0])
        minute=int(complete.message().split(':')[1])
        return ["PRIVMSG $C$ :"+makeFuzzyTime(hour, minute)]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
