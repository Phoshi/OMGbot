# -*- coding: utf-8 -*-
from plugins import plugin
import os

import re

from datetime import datetime, timedelta
import time
import random
import fnmatch

def sublistIndex(l1, l2):
    if len(l1) < len(l2):
        return -1
    k = 0
    while k < len(l1):
        h = 0
        while h < len(l2) and l1[k+h] == l2[h]:
            h += 1
            if k+h >= len(l1):
                break
        if h == len(l2):
            return k
        k += 1
    return -1

class pluginClass(plugin):
    def __init__(self):
        pass
    
    def gettype(self):
        return "command"

    def tuples(self, words):
        for i in range(len(words) - self.depth):
            yield words[i:i+self.depth+1]

    def isSentenceEnd(self, word):
        return word == '.' or word == '!' or word == '?'

    def includesPhrase(self):
        return len(includedPhrase) > 0

    def tupleToLowerKey(self, t):
        return tuple(map(lambda a: a.lower(), t))

    def generateMarkovText(self, words, cache):
        depth = self.depth
        
        endMark = self.tupleToLowerKey(words[-depth:])
        
        resetAtEnd = not endMark in cache
        
        seed = random.randint(0, len(words)-depth)
        current = tuple(words[seed:seed+depth])
        genWords = []

        phrasePos = -2

        self.chainFailure = False

        if len(self.startPhrase) > 0:
            start = self.startPhrase
            genWords.extend(start[:-depth])
            current = tuple(start[-depth:])
            
            endMark2 = self.tupleToLowerKey(self.startPhrase[-depth:])
        
            self.chainFailure = not endMark2 in cache

        while len(genWords) < self.outputLen:
            genWords.append(current[0])
            
            if len(genWords) == self.outputLen-depth+1:
                genWords.extend(current[1:])
                break
            if len(genWords) > self.outputLen-depth+1:
                rem = self.outputLen - len(genWords)
                if rem > 0:
                    genWords.extend(current[1:1+rem])
                break

            key = self.tupleToLowerKey(current)
            
            if (resetAtEnd and key == endMark) or (self.chainFailure and key == endMark2) or (random.randint(0,1) == 0 and self.isSentenceEnd(key[-1][-1])):
                genWords.extend(current[1:])
                
                seed = random.randint(0, len(words)-depth)
                current = tuple(words[seed:seed+depth])
            else:
                current = current[1:] + tuple([random.choice(cache[key])])

        return ' '.join(genWords)

    def usage(self):
        return 'Usage: !markov [-words %d] [-logs %d] [-filter %s [%s [%s ...]]] [-phrase %s] [-depth %d]'

    def parseArgs(self, args):
        self.outputLen = 60
        self.daysBack = 50
        self.nickFilter = ['*']
        self.startPhrase = []
        self.depth = 2

        i = 0
        while i < len(args):
            if args[i] == '-words':
                try:
                    self.outputLen = int(args[i+1])
                    if self.outputLen > 500:
                        return ["PRIVMSG $C$ :Error: too much words. (Max value: 500)"]
                    elif self.outputLen < 0:
                        return ["PRIVMSG $C$ :Error: negative length"]
                    elif self.outputLen == 1:
                        return ["PRIVMSG $C$ :Error: length of 1 word"]
                except:
                    return ["PRIVMSG $C$ :Invalid arg %s - %s" % (args[i+1], self.usage())]
                i += 2
            elif args[i] == '-depth':
                try:
                    self.depth = int(args[i+1])
                    if self.depth > 10:
                        return ["PRIVMSG $C$ :Error: Depth too big. (Max value: 10)"]
                    elif self.depth < 1:
                        return ["PRIVMSG $C$ :Error: depth smaller than 1"]
                except:
                    return ["PRIVMSG $C$ :Invalid arg %s - %s" % (args[i+1], self.usage())]
                i += 2
            elif args[i] == '-logs':
                try:
                    self.daysBack = int(args[i+1])
                    if self.daysBack > 500:
                        return ["PRIVMSG $C$ :Error: too much logs to read. (Max value: 500)"]
                    elif self.daysBack < 0:
                        return ["PRIVMSG $C$ :Error: negative number of logs"]
                except:
                    return ["PRIVMSG $C$ :Invalid arg %s - %s" % (args[i+1], self.usage())]
                i += 2
            elif args[i] == '-filter':
                self.nickFilter = args[i+1:]
                j = 0
                while j < len(self.nickFilter):
                    if self.nickFilter[j][0] == '-':
                        self.nickFilter = self.nickFilter[:j]
                        break
                    j += 1
                    
                if len(self.nickFilter) == 0:
                    return ["PRIVMSG $C$ :Invalid argument for -filter - %s" % self.usage()]
                
                i += len(self.nickFilter)+1
            elif args[i] == '-phrase':
                self.startPhrase = args[i+1:]
                j = 0
                while j < len(self.startPhrase):
                    if self.startPhrase[j][0] == '-':
                        self.startPhrase = self.startPhrase[:j]
                        break
                    j += 1
                    
                if len(self.startPhrase) == 0:
                    return ["PRIVMSG $C$ :Invalid argument for -phrase - %s" % self.usage()]
                i += len(self.startPhrase)+1
            elif args[i][0] == '-':
                return ["PRIVMSG $C$ :Invalid option %s - %s" % (args[i], self.usage())]
            else:
                return ["PRIVMSG $C$ :Invalid usage - %s" % self.usage()]

        return []

    def action(self, complete):
        if complete.channel()[0] != '#':
            return []

        channel = complete.channel()

        parseResult = self.parseArgs(complete.message().split())
        if len(parseResult) > 0:
            return parseResult
        
        today = time.gmtime()
        today = datetime(today.tm_year, today.tm_mon, today.tm_mday) #datetime.today()

        cache = {}

        re_message = re.compile('\[.+?\] \* (?P<poster>[A-Za-z0-9_-]+) \*? (?P<words>.+)')
        re_words = re.compile('[^\s]+')

        words = []

        phraseTooShort = len(self.startPhrase) < self.depth

        fileTries = 10

        for delta in range(self.daysBack):
            day = today - timedelta(days=delta)
            doty = int(day.strftime('%j'))
            path = os.path.join("logs","LogFile - %s-%d-%d" % (channel, day.year, doty))

            try:
                with open(path) as log:
                    lines = log.readlines()
            except:
                print path, 'not found'
                
                fileTries -= 1
                if fileTries > 0:
                    continue
                else:
                    break

            log_words = []

            for line in lines:
                message = re_message.search(line)
                if not message:
                    continue
                poster = message.group('poster')
                if poster == 'OMGbot':
                    continue
                
                ignore = True
                for f in self.nickFilter:
                    if fnmatch.fnmatch(poster.lower(), f.lower()):
                        ignore = False
                        break
                
                if ignore:
                    continue
                
                message = message.group('words').strip()
                if message[0] == '!':
                    continue
                if message[-1].isalnum():
                    message += '.'

                line_words = re_words.findall(message)

                log_words.extend(line_words)

            words = log_words + words

        """possibleExtensions = []

        L = len(self.startPhrase)"""
                        
        for ws in self.tuples(words):
            key = self.tupleToLowerKey(ws[:self.depth])

            """for d in range(1, min(self.depth, L+1)):
                if self.startPhrase[-d:] == ws[0:d]:
                    possibleExtensions.append(ws[d:])"""
            
            if key in cache:
                cache[key].append(ws[-1])
            else:
                try:
                    cache[key] = [ws[-1]]
                except Exception as detail:
                    print detail
                    print ws[-1]
                    return ["PRIVMSG $C$ :%s: %s"%(detail, ws[-1])]
                
        """if random.randint(0,1) == 0 and possibleExtensions != [] and tuple(self.startPhrase[-self.depth:]) not in cache:
            self.startPhrase.extend(random.choice(possibleExtensions))
            print 'adaptation:', self.startPhrase"""

        if len(words) < self.depth+1:
            return ["PRIVMSG $C$ :Not enough words found."]

        m = self.generateMarkovText(words, cache)
        
        if not m[0].istitle():
            m = m[0].upper() + m[1:]
        if m[-1].isalnum():
            m += '.'
        else:
            m = m[:-1] + '.'

        re_url = re.compile('https?://')

        markovText = ''
        endLine = False
        for i in xrange(len(m)):
            c = m[i]
            if endLine:
                if re_url.match(m[i:i+8]):
                    markovText += c
                else:
                    markovText += c.upper()
                if c.isalnum():
                    endLine = False
            else:
                markovText += c
                if self.isSentenceEnd(c) and i < len(m) - 1 and m[i+1] == ' ':
                    endLine = True

        output = ["PRIVMSG $C$ :" + markovText]

        if self.chainFailure:
            print 'Failed to chain starting phrase.'

        return output
    
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the MARKOV CHAIN plugin",
                "PRIVMSG $C$ :%s" % self.usage(),
                "PRIVMSG $C$ :Example:",
                "PRIVMSG $C$ :!markov -words 50 -logs 40 -filter PY sirX* -depth 3 -phrase Once upon a time"]
