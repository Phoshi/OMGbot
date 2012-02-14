# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import urllib
import urllib2
from bitlyServ import bitly
import re
import random
import cookielib
import time

class pluginClass(plugin):
    def __init__(self):
        cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        try:
            r = self.opener.open('http://ponibooru.413chan.net/post/list')
        except:
            pass

        self.recent = []
        
    def gettype(self):
        return "command"

    def action(self, complete):
        tags = complete.message()
            
        query = urllib.urlencode(dict([["tags",tags]]))
        url = "http://ponibooru.413chan.net/post/list/%s/1"%urllib.quote(tags)

        try:
            req=self.opener.open(url)
        except urllib2.HTTPError as error:
            if '406' in str(error):
                if len(tags.split(' ')) > 4:
                    return ["PRIVMSG $C$ :More than 4 tags are not allowed."]
                if '-' in tags:
                    return ["PRIVMSG $C$ :You may not search for exclusive tags only."]
                
                return ["PRIVMSG $C$ :Unacceptable input (reason unknown)."]
            return ["PRIVMSG $C$ :Sankaku channel seems down!"]
            
        content=req.read()
        pages = re.findall("/post/list/([0-9]+)", content)
        if pages!=[]:
            maxPage = int(max(pages, key=lambda x: int(x)))
            newPage = random.randint(1,maxPage)
            url = "http://ponibooru.413chan.net/post/list/%s/%s"%(urllib.quote(tags), newPage)
            content = self.opener.open(url).read()

        pattern = r"href='(.+?)'.+?title='(.+?) // .+?'.+?src='(.+?)'"

        matches = re.findall(pattern, content)

        start = 0
        for u, t in self.recent:
            if t < time.time() - 15 * 60:
                start += 1

        recent = [x for x,y in self.recent[start:]]

        possibilites = []
        
        for href,title, src in matches:
            if not href in recent:
                possibilites.append((href, src, title))

        if possibilites == []:
            return ["PRIVMSG $C$ :No pictures found!"]
        
        match = random.choice(possibilites)

        self.recent.append((match[0], time.time()))

        url = "http://ponibooru.413chan.net/"+match[0]
        tags = []
        tags_old = match[2].split(' ')
        rating = 'unknown'
        
        for tag in tags_old:
            if tag[:7] == 'rating:':
                rating = tag[7:]
                break
            tags += [tag]

        total_length = 0
        i = 0
        
        for tag in tags:        
            if total_length + len(tag) > 150:
                tags = tags[:i] + ['...']
                break
            i += 1
            total_length += len(tag)
        tags = ' '.join(tags)
        print tags
        
        return ["PRIVMSG $C$ :" + bitly(url) + " (tags: " + unicode(tags, 'utf-8') + ")"]
    
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !ponies module! See http://ponibooru.413chan.net/ext_doc/index for a full list of features.",
                "PRIVMSG $C$ :Example usage:",
                "PRIVMSG $C$ :!ponies wallpaper blonde_hair",
                "PRIVMSG $C$ :!ponies applejack rainbow_dash rating=q"]
