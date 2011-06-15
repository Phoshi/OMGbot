# -*- coding: utf-8 -*-
from plugins import plugin
from pluginArguments import pluginArguments
from pluginFormatter import formatInput, formatOutput
import globalv
import operator
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        argumentString = ":null!nobody@nowhere PRIVMSG nothing :!sr388"
        argumentsObject = formatInput(pluginArguments(argumentString))
        numbers={}
        if complete.message().isdigit()==False:
            totalIterations = 10000
        else:
            totalIterations=int(complete.message())
        for i in xrange(0,totalIterations):
            output = globalv.loadedPlugins['sr388'].action(argumentsObject)[0]
            number = output.split()[3][1:]
            if number in numbers:
                numbers[number]+=1
            else:
                numbers[number]=1
        sortedNumbers = sorted(numbers.iteritems(), key=operator.itemgetter(1))
        sortedNumbers.reverse()
        minHits=(0, totalIterations)
        maxHits=(0,0)
        total=0
        for number in sortedNumbers:
            total+=number[1]
        mean = total/len(sortedNumbers)
        devTotal=0

        for number in sortedNumbers:
            devTotal+= (number[1]-mean)**2
            if number[1]>maxHits[1]:
                maxHits = number
            elif number[1]<minHits[1]:
                minHits = number

        devMean = devTotal/len(sortedNumbers)
        stdDev = devMean**0.5


        return ["PRIVMSG $C$ :Total iterations: %s; Most often picked quote: %s (with %s hits); Least often picked quote: %s (with %s hits); Results have a standard devation of %s"%(totalIterations, maxHits[0], maxHits[1], minHits[0], minHits[1], stdDev)]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
