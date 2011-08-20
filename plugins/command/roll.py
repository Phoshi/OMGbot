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

        try:
            split = re.findall(r"(\d*)[dD](\d+)(.*)", dice)[0]
        except IndexError:
            raise Exception("Die must be in [x]dy[func] format")
        if (split[0]==""):
            numDice=1
        else:
            numDice = int(split[0])
        if (split[1]==""):
            return "You must provide a number of sides from your dice"
        numSides = int(split[1])
        if (numDice < 1):
            numDice = 1
        if (numSides < 2):
            return "Your dice must have more than one side!"

        functions = re.findall("([a-zA-Z+-])(\d*)", split[2])

        for die in range(numDice):
            diceRoll = random.randint(1, numSides)
            rolls.append(diceRoll)

        originalRolls = rolls[:]
        returnNumberNotTotal = False
        totalOffset = 0
        forceUseOriginalRoll = False
        if (len(functions)>0):
            for function, argumentToFunction in functions:
                argumentToFunction = int(argumentToFunction) if (argumentToFunction!="") else 0
                rolls = self.process(rolls, function, argumentToFunction, numSides)
                if (len(rolls) >= len(originalRolls)):
                    originalRolls = rolls[:]
                if (function=="s"):
                    returnNumberNotTotal = True
                elif (function=="+"):
                    totalOffset+=argumentToFunction
                elif (function=="-"):
                    totalOffset-=argumentToFunction
                elif (function=="S"):
                    forceUseOriginalRoll = True


        if (returnNumberNotTotal):
            total = len(rolls)
        else:
            total = sum(rolls) + totalOffset
        processedRolls = rolls[:]
        if self.verbose and len(originalRolls)>1:
            if (len(rolls) < len(originalRolls) or forceUseOriginalRoll):
                rolls = originalRolls
            formattedRolls = []
            numBolded = 0
            for die in rolls:
                if die not in processedRolls or numBolded >= len(processedRolls):
                    bold = ""
                else:
                    bold = "\x02"
                    numBolded+=1
                formattedRolls.append("%s%s%s"%(bold, die, bold))
            if (len(formattedRolls)>20):
                return "%s ... %s = \x02%s\x02"%(", ".join(formattedRolls[:10]), ", ".join(formattedRolls[-10:]), total)
            return "%s = \x02%s\x02"%(", ".join(formattedRolls), total)
        else:
            return "%s"%total



    def process(self, rolls, function, argument, originalRoll):
        #if (function == "+"): #Offset each dice by this
        #    rolls = map(lambda die: die + argument, rolls)
        #elif (function == "-"):
        #    rolls = map(lambda die : die - argument, rolls)
        if (function == "k"): #Keep N highest dice
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
        elif (function == "S"): #Storyteller syntax - for a d10, above 7 is success, 10 is two successes, no successes and a die is a natural 1 is a critical failure
            #I figure I can make that more flexible, so xdySn has above n as success, ace as two
            successes = []
            for die in rolls:
                if (die==originalRoll):
                    successes.append(2)
                elif (die >= argument):
                    successes.append(1)
            if (len(successes) == 0 and len(filter(lambda die: die==1, rolls))>0):
                successes.append(-1)
            rolls = successes
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
            numRolls = len(dice.split())
            for die in dice.split():
                if (numRolls > 1):
                    results.append("%s: %s"%(die, self.roll(die)))
                else:
                    results.append("%s"%self.roll(die))
            outputQueue.put(" || ".join(results))
        except Exception as e:
            outputQueue.put(e)

    def __init__(self):
        self.verbose = True
    def action(self, complete):
        dice = complete.message()
        if (dice == "help"):
            return ["PRIVMSG $C$ :Syntax: http://lmwcs.com/rptools/wiki/Dice_Expressions"]
        mode=""
        diceRolls=[]
        name=[]
        users=[]
        for die in dice.split():
            if (die == "-name"):
                mode = "name"
            elif (die == "-users"):
                mode = "users"
            elif (die == "-totals"):
                self.verbose = False
            elif (die == "-verbose"):
                self.verbose = True
            elif (mode == ""):
                diceRolls.append(die)
            elif (mode=="name"):
                name.append(die)
            elif (mode=="users"):
                users.append(die)


        name = " ".join(name)
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
