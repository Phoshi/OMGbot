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
        r = self.opener.open('http://chan.sankakucomplex.com/en/post/index')

        self.recent = []
        
    def gettype(self):
        return "command"

    def action(self, complete):
        tags = complete.message()
            
        query = urllib.urlencode(dict([["tags",tags]]))
        url = "http://chan.sankakucomplex.com/en/post/index.content?limit=150&"+query

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

        pattern = r'href="(.+?)".+?src="(.+?)".+?title="(.+?)"'

        matches = re.findall(pattern, content)

        start = 0
        for u, t in self.recent:
            if t < time.time() - 15 * 60:
                start += 1

        recent = [x for x,y in self.recent[start:]]

        possibilites = []
        
        for href,src,title in matches:
            if not href in recent:
                possibilites.append((href, src, title))

        if possibilites == []:
            return ["PRIVMSG $C$ :No pictures found!"]
        
        match = random.choice(possibilites)

        self.recent.append((match[0], time.time()))

        if match[1].find('download')>-1:
            url = 'http://chan.sankakucomplex.com' + match[0]
        else:
            url = match[1].replace('preview/','')
            url = re.sub('http://c\d','http://chan',url)
            try:
                urllib2.urlopen(url)
            except:
                url = url[:-3] + 'png'
                try:
                    urllib2.urlopen(url)
                except:
                    url = url[:-3] + 'gif'
                    try:
                        urllib2.urlopen(url)
                    except:
                        url = match[0]

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
        
        return ["PRIVMSG $C$ :" + bitly(url) + " (rating: \x02" + rating + "\x02, tags: " + unicode(tags, 'utf-8') + ")"]
    
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !sankaku module! See http://chan.sankakucomplex.com/help/cheatsheet for a full list of features.",
                "PRIVMSG $C$ :Example usage:",
                "PRIVMSG $C$ :!sankaku wallpaper blonde_hair",
                "PRIVMSG $C$ :!sankaku touhou ribbon wings rating:questionable"]
