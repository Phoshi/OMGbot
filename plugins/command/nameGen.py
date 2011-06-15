# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        import random
        vowels = ('a','e','i','o','u')
        consonants = ('q','w','r','t','y','p','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m','q','w','r','t','y','p','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m')
        nextMustBeVowel=("x" ,"p" ,"s" ,"v" ,"j" ,"n" ,"d" ,"c" ,"b" ,"h" ,"g" ,"k")
        vowelLength=len(vowels)-1
        consonantLength=len(consonants)-1
        def generateName(number,randGen=random):
            name = mustBe = ""
            vowelOr=round(randGen.random())
            for value in xrange(0,number):
                if mustBe:
                    name+=mustBe
                    mustBe=""
                elif vowelOr>0:
                    toAdd=vowels[int(round(randGen.random()*vowelLength))]
                    name+=toAdd
                    vowelOr=0 if random.randint(0,100)<80 else 1
                else:
                    toAdd=consonants[int(round(randGen.random()*consonantLength))]
                    name+=toAdd
                    if (toAdd in nextMustBeVowel):
                        vowelOr=1
                    else:
                        vowelOr=round(randGen.random())
                if name[value]=='q':
                    mustBe="u"
            return name.capitalize()
        return ["PRIVMSG $C$ :"+generateName(int(complete.message()))]
def describe(self, complete):
    return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
