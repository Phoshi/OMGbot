# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import urllib
import urllib2
from bitlyServ import bitly
import re
import random

class pluginClass(plugin):
    def __init__(self):
        self.history = []
        
    def gettype(self):
        return "command"

    def action(self, complete):
        tags = complete.message()
            
        query = urllib.urlencode(dict([["tags",tags]]))
        url = "http://safebooru.org/index.php?page=dapi&s=post&q=index&limit=200&"+query

        try:
            req=urllib2.urlopen(url)
        except urllib2.HTTPError as error:
            if '406' in str(error):
                return ["PRIVMSG $C$ :Unacceptable input."]
            return ["PRIVMSG $C$ :Safebooru seems down!"]
            
        content = req.read()
        matches = re.findall(r'file_url="(.+?)"(?:.+?)rating="(?:s|q)" tags="\s?(.+?)\s?" id="(\d+?)"', content)

        if matches == []:
            return ["PRIVMSG $C$ :No pictures found!"]

        w_matches = []
        for match in matches:
            if not match[2] in self.history:
                w_matches.append(match)

        if w_matches == []:
            return ["PRIVMSG $C$ :No new picture found (Compared to the last 60 pictures)"]
        
        match = w_matches[random.randint(0, len(w_matches)-1)]

        self.history.append(match[2])
        self.history = self.history[-60:]

        url = match[0]

        tags = match[1].split(' ')

        total_length = 0
        i = 0
        
        for tag in tags:        
            if total_length + len(tag) > 280:
                tags = tags[:i] + ['...']
                break
            i += 1
            total_length += len(tag)
        tags = ' '.join(tags)
        
        return ["PRIVMSG $C$ :" + bitly(url) + " (tags: " + tags + ")"]
    
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !animu module! See http://safebooru.org/index.php?page=help&topic=cheatsheet for a full list of features.",
                "PRIVMSG $C$ :Example usage:",
                "PRIVMSG $C$ :!animu wallpaper blonde_hair",
                "PRIVMSG $C$ :!animu touhou ribbon wings"]
