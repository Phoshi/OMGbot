# -*- coding: utf-8 -*-
from plugins import plugin
import re
import random
import globalv
class pluginClass(plugin):
#Dice expression syntax stolen shamelessly from
#http://lmwcs.com/rptools/wiki/Dice_Expressions
    def gettype(self):
        return "command"
    def roll(self, dice):
        if (type(dice)==int):
            return random.randint(1, dice)
        if (dice.isdigit()):
            return random.randint(1, int(dice))

        rolls = []

        split = re.findall(r"(\d+)[dD](\d+)(.*)", dice)[0]
        numDice = int(split[0])
        numSides = int(split[1])
        functions = re.findall("([a-zA-Z+-])(\d*)", split[2])

        for die in range(numDice):
            diceRoll = random.randint(1, numSides)
            rolls.append(diceRoll)

        if (len(functions)>0):
            for function, argumentToFunction in functions:
                argumentToFunction = int(argumentToFunction) if (argumentToFunction!="") else 0
                rolls = self.process(rolls, function, argumentToFunction, numSides)
                print function, argumentToFunction
                print rolls

        total = sum(rolls)
        return "%s = %s"%(", ".join([str(die) for die in rolls]), total)



    def process(self, rolls, function, argument, originalRoll):
        if (function == "+"): #Offset each dice by this
            rolls = map(lambda die: die + argument, rolls)
        elif (function == "-"):
            rolls = map(lambda die : die - argument, rolls)
        elif (function == "k"): #Keep N highest dice
            rolls.sort()
            rolls.reverse()
            rolls = rolls[:argument]
        elif (function == "d"): #Drop N lowest dice
            rolls.sort()
            rolls = rolls[argument:]
        elif (function == "r"):
            rolls = map(lambda die: self.roll(originalRoll) if die < argument else die, rolls)
        elif (function == "s"):
            rolls = filter(lambda die: die>=argument, rolls)
        elif (function == "e"):
            for die in rolls:
                if (die == originalRoll):
                    rolls.append(self.roll(originalRoll))



        return rolls

    def action(self, complete):
        dice = complete.message()
        return ["PRIVMSG $C$ :%s"%self.roll(dice)]

    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
