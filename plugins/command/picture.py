# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import Image, ImageDraw, ImageFont
import urllib
import math
import pickle
import sys
import os

def _cmp_(a,b):
    if a[1]<b[1]:
        return 1
    if a[1]>b[1]:
        return -1
    if a[0]>b[0]:
        return 1
    if a[0]<b[0]:
        return -1
    return 0

class pluginClass(plugin):
    def __init__(self):
        self.charIgnore = '!#*()"\'?,.:\x01\x02\xff\x16\t\r\n'
        self.exceptions = [':)',':(','=)','=(',':|','>:(','>:)','._.',':\'(']

    def gettype(self):
        return "command"
        
    def action(self,complete):
        channel = complete.channel()
                
        words = complete.message().split()
        try:
            if len(words)>0:
                search_terms = []
                width = None
                height = None
                c = 0
                for word in words:
                    if word == '-search':
                        c = 10
                    elif c <= 1 and word.isdigit():
                        if c == 0:
                            width = int(word)
                        else:
                            height = int(word)
                        c += 1
                    elif c == 10:
                        search_terms.append(word.lower())
                    
                if width == None:
                    width,height = 1600,900
                elif height == None:
                    height = width
                        
                if words[0] == channel or words[0].isdigit():
                    return self.showPicture(os.path.join('config','picturelogs','picturelog-%s'%channel),channel,width,height, search_terms)
                else:
                    return self.showPicture(os.path.join('config','picturelogs','picturelog-%s-%s'%(channel,words[0])),channel+"-"+words[0],width,height, search_terms)
            else:
                return self.showPicture(os.path.join('config','picturelogs','picturelog-%s'%channel),channel,1600,900, [])
        except Exception as detail:
            print detail
            return ["PRIVMSG $C$ :Error: dimensions too big."]

    def showPicture(self, logpath, name, width,height, search_terms):
        print logpath
        if os.path.exists(logpath):
            with open(logpath) as logFile:
                words_dict = pickle.load(logFile)
        else:
            return ["PRIVMSG $C$ :He/she hasn't said anything yet or isn't registered/identified!"]

        filepath = os.path.join('config','picture-%s.png'%name)
        
        words = words_dict.items()
        words.sort(_cmp_)
        maxc = words[0][1]

        FONTPATH = '/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans-Bold.ttf'

        img = Image.new("RGB",(width,height),(255,255,255))
        g = ImageDraw.Draw(img)
        
        x,y = 0,height/2
        bottom,top = 0,0
        first = True
        d = 0
        up = True
        prevr = 1
        f = ImageFont.truetype(FONTPATH,50)
        
        for word,count in [(x_,y_) for x_,y_ in words]:
            r = int((50*math.log(count+1))/math.log(maxc+1))
            word_ = ' '+word+' '
            if prevr != r:
                f = ImageFont.truetype(FONTPATH,r)
            prevr = r
            size = g.textsize(word_, f)
            w,h = size
            
            if first:
                bottom = y+h/2.5
                top = y-h/2.5
                first = False
                
            if x+w > width and x > 0:
                x = 0
                if up:
                    y = top-h/2.5
                    top = y-h/2.5
                    d+=8
                else:
                    y = bottom+h/2.5
                    bottom = y+h/2.5
                up = not up
                if bottom >= height and top <= 0:
                    break
            if word in search_terms:
                g.text((x,y-h/2), word_, (255,0,0), f)
            elif word_.find('://')>=0:
                g.text((x,y-h/2), word_, (d,d,255), f)
            else:    
                g.text((x,y-h/2), word_, (d,d,d), f)
            x += w
            
        img.save("/home/py/public_html/channelImages/picture-%s.png"%name,"PNG")
        return ['PRIVMSG $C$ :http://terminus.mrflea.net:81/~py/channelImages/picture-%s.png'%urllib.quote(name)]

    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the picture module! Say !picture to see a piece of art made by you talking!"]
