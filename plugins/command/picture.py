# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import Image, ImageDraw, ImageFont
import urllib
import math
import sys
import os
import re
import time
from bitlyServ import bitly

def wordCloud(frequencies, marks, fontpath, image_width = 1024, image_height = 800):
    words = frequencies

    words = sorted(words.items(), key = lambda (x,y): -y)
    maxcount = words[0][1]

    width = {}
    height = {}
    padding = {}
    font = {}
    color = {}

    minSize = 10
    maxSize = 48

    allFonts = {}

    for size in range(1,maxSize+1):
        allFonts[size] = ImageFont.truetype(fontpath, size)

    for word, count in words:
        F = count/float(maxcount)
        size = minSize + int((maxSize - minSize) * (F**0.45))
        f = allFonts[size]
        x,y = f.getsize(word)
        padding[word] = int(0.2*y)
        
        font[word] = f
        width[word], height[word] = x+padding[word],y+padding[word]
        v = 220 - 220 * (F**1.2)
        color[word] = (v,v,v)
        if word in marks:
            color[word] = (255,0,0)

    todo = [x for x,y in words]

    class Row:
        def __init__(self):
            self.elements = set()
        def add(self, e):
            self.elements.add(e)

    rows = [] 
    currentRow = None
    totalHeight = 0

    while len(todo):
        word = todo[0]
        del todo[0]
        found = False
        for row in rows:
            if row.width + width[word] <= image_width:
                found = True
                row.width += width[word]
                row.add(word)
                break
            
        if not found:
            if totalHeight+height[word] > image_height:
                break
            
            newRow = Row()
            newRow.add(word)
            newRow.width = width[word]
            newRow.height = height[word]
            rows.append(newRow)
            
            totalHeight += newRow.height

    im = Image.new('RGB', (image_width, image_height), (255,255,255))
    g = ImageDraw.Draw(im)

    y = 0
    for row in rows:
        x = 0
        for e in row.elements:
            ex, ey = padding[e]/2+x, y+padding[e]/2+(row.height-height[e])/2
            sr,sg,sb = color[e]
            g.text((ex, ey), e, (sr / 2, sg / 2, sb / 2), font[e])
            g.text((ex, ey), e, color[e], font[e])
            x += width[e]
        y += row.height
            
    return im

class pluginClass(plugin):
    re_markup = re.compile('(\x03\d{1,2}(\d{1,2})?|\x02|\x1F|\x16|\x0F)')
    
    def __init__(self):
        pass

    def gettype(self):
        return 'command'

    def action(self, complete):
        channel = complete.channel().lower()

        nickFilter = []
        nickExclude = []
        days = 10
        marks = []

        nextCommand=''
        terms = complete.message().split()
        i = 0
        try:
            while i < len(terms):
                if terms[i] == '-days':
                    days = int(terms[i+1])
                    i += 2
                elif terms[i] == '-nick':
                    j = i + 1
                    while j < len(terms) and terms[j][0] != '-':
                        j += 1
                    nickFilter += map(lambda x: x.lower(), terms[i+1:j])
                    i = j
                elif terms[i] == '-not':
                    j = i + 1
                    while j < len(terms) and terms[j][0] != '-':
                        j += 1
                    nickExclude += map(lambda x: x.lower(), terms[i+1:j])
                    i = j
                elif terms[i] == '-mark':
                    j = i + 1
                    while j < len(terms) and terms[j][0] != '-':
                        j += 1
                    marks += map(lambda x: x.lower(), terms[i+1:j])
                    i = j
                else:
                    raise Exception("Incorrect input")
        except Exception as e:
            print e
            return ["PRIVMSG $C$ :Invalid usage. Correct usage: %s%s [-days Number of days to "
                    "search] [-mark Words to highlight] [-nick Users to filter on] "
                    "[-not Users to exclude]"%(globalv.commandCharacter, complete.cmd()[0])]

        wordCollection = {}
        width = 1024
        height = 1024

        today=time.gmtime()
        currentYear=today[0]
        currentDay=today[7]

        logFails = 0

        relevantNicks = set()

        for offset in xrange(days):
            day = currentDay-offset
            year = currentYear
            if day <= 0:
                day += 365
                year-=1
            path=os.path.join("logs","LogFile - "+channel+"-"+str(year)+"-"+str(day))
            
            if not os.path.exists(path):
                print path
                logFails += 1
                if logFails > 3:
                    break
                else:
                    continue

            data=open(path).readlines()
            for line in data:
                line=re.search("^\[.*?\] \* (?P<nick>[^\s]*)( \*)? (?P<message>.+)", line)
                if line is None:
                    continue
                nick = line.group('nick').lower()
                if nick in nickExclude:
                    continue
                if nickFilter != []:
                    if nick not in nickFilter:
                        continue
                    else:
                        relevantNicks.add(nick)
                    
                message = line.group('message')
                message = self.re_markup.sub('',message)
                words = message.split()
                for word in words:
                    wordNew = word.rstrip('"\'!?]).,;:').lstrip('"\'([')
                    if wordNew == '':
                        wordNew = word
                    wordNew = wordNew.lower()
                    wordCollection[wordNew] = wordCollection.setdefault(wordNew,0)+1

        if len(wordCollection) == 0:
            return ["PRIVMSG $C$ :No words found!"]

        relevantNicks = sorted(relevantNicks)

        fileName = 'picture-%s' % channel
        if nickFilter != []:
            fileName += '-%s' % (','.join(relevantNicks))
        fileName += '.png'
        
        im = wordCloud(wordCollection, marks, r'/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans.ttf', width, height)
        im.save("/home/py/public_html/omgbot/images/%s" % fileName, "PNG")

        return ["PRIVMSG $C$ :" + bitly('http://achene.phantomflame.com/~py/omgbot/images/%s' % (fileName.replace('#','%23')))]
