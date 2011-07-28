# -*- coding: utf-8 -*-
from plugins import plugin
import re
import time
import random
import globalv
import shlex
import multiprocessing 
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
        if (numDice < 1):
            return "You must roll at least one die!"
        if (numSides < 2):
            return "Your dice must have more than one side!"

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
        elif (function == "r"): #reroll any die lower than N
            rolls = map(lambda die: self.roll(originalRoll) if die < argument else die, rolls)
        elif (function == "s"): #Only count dice larger or equal to N
            rolls = filter(lambda die: die>=argument, rolls)
        elif (function == "e"):
            while (len(filter(lambda die: die==originalRoll, rolls)) > 0):
                print "Exploded!"
                nrolls = []
                for die in rolls:
                    nrolls.append(self.roll(originalRoll))
                rolls = nrolls
        elif (function == "o"):
            for die in rolls:
                if (die == originalRoll):
                    rolls.append(self.roll(originalRoll))



        return rolls

    def rollHandler(self, dice, outputQueue):
        try:
            results = []
            for die in dice.split():
                results.append("%s: %s"%(die, self.roll(die)))
            outputQueue.put(" || ".join(results))
        except Exception as e:
            outputQueue.put(e)

    def action(self, complete):
        dice = complete.message()
        mode=""
        diceRolls=[]
        name=""
        users=[]
        for die in dice.split():
            if (die == "-name"):
                mode = "name"
            elif (die == "-users"):
                mode = "users"
            elif (mode == ""):
                diceRolls.append(die)
            elif (mode=="name"):
                name = die
            elif (mode=="users"):
                users.append(die)


        dice = " ".join(diceRolls)
        outputQueue = multiprocessing.Queue()
        rollThread = multiprocessing.Process(target=self.rollHandler, args=(dice, outputQueue))
        rollThread.start()
        now = time.time()
        while ((time.time() - now) < 5):
            time.sleep(0.05)
            if (not outputQueue.empty()):
                output=[]
                result = outputQueue.get()
                if (name != ""):
                    result = "%s (%s)"%(result, name)
                output.append("PRIVMSG $C$ :%s"%result)
                for user in users:
                    output.append("PRIVMSG %s :%s"%(user, result))
                print output
                return output
        rollThread.terminate()
        return ["PRIVMSG $C$ :Rolling took too long!"]

    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !roll module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!roll xdy[modes]*", "PRIVMSG $C$ :See http://lmwcs.com/rptools/wiki/Dice_Expressions for syntax details"]
