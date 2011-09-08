# -*- coding: utf-8 -*-
from plugins import plugin
from urlparse import urljoin
import globalv
import urllib
import urllib2
import re
import random

class Image:
    imageUrl = ""
    tags = []
    dimensions = ""
    source = ""
    def __init__(self, url, tags, dimensions, source):
        self.imageUrl = url
        self.tags = tags
        self.dimensions = dimensions
        self.source = source
    def ToString(self):
        tags = ", ".join(self.tags[:15]) or "Unknown Tags"
        size = self.dimensions or "Unknown Size"
        source = self.source or "No Source"

        return "%s - %s (%s) - \x02Source:\x02 %s"%(self.imageUrl, str(tags), size, source)



class Site:
    searchUrl = ""
    imageRegex = ""
    additionalTags = []
    pageRegexes = {}
    translationDict = {}
    ResultImage = None
    Name = ""

    def __init__(self, name, searchUrl, imageRegex, additionalTags, pageRegexes, translations = {}):
        self.Name = name
        self.searchUrl = searchUrl
        self.imageRegex = imageRegex
        self.additionalTags = additionalTags
        self.pageRegexes = pageRegexes
        self.translationDict = translations

    def Search(self, tags):
        searchTags = " ".join(self.additionalTags + map(lambda tag:tag if not tag in self.translationDict else self.translationDict[tag], tags.split(' ')))
        searchPage = self.searchUrl % urllib.quote_plus(searchTags)
        print searchPage

        request = urllib2.urlopen(searchPage, None, 10)
        page = request.read()

        images = re.findall(self.imageRegex, page)
        random.shuffle(images)

        if (len(images) == 0):
            raise Exception("No Results!")
        imageUrl = urljoin(searchPage, images[0])

        self.ResultImage = self.parseImagePage(imageUrl)

    def parseImagePage(self, pageURL):
        request = urllib2.urlopen(pageURL, None, 10)
        page = request.read()
        tags = []
        dimensions = ""
        source = ""

        if ("tags" in self.pageRegexes):
            tags = re.findall(self.pageRegexes["tags"], page)
        if ("dimensions" in self.pageRegexes):
            dimensions = (re.findall(self.pageRegexes["dimensions"], page) or ["0x0"])[0]
        if ("source" in self.pageRegexes):
            source = (re.findall(self.pageRegexes["source"], page) or ["No Source"])[0]
        image = Image(pageURL, tags, dimensions, source)
        return image


def getSiteList(explicit = False):
    sites = []
    bestPonyDict = {"best_pony":"twilight_sparkle"}
    ponibooruImageRegexDict = {"tags":r"name='tag_edit__tags' value='(.*?)'",
            "dimensions":r"<br>Size: (\d+x\d+)",
            "source":r"<br>Source: <a href='(.*?)'>"}
    ponibooruDefaultTags = []
    if (explicit):
        ponibooruDefaultTags.append("rating=e")
    ponibooru = Site("Ponibooru", "http://ponibooru.413chan.net/post/list/%s/1", "<span class=\"thumb\"><a href='(.*?)'>", ponibooruDefaultTags, ponibooruImageRegexDict, bestPonyDict)
    sites.append(ponibooru)

    E621TranslationDict = {"rainbow_dash":"rainbow_dash_(mlp)",
            "applejack":"applejack_(mlp)",
            "twilight_sparkle":"twilight_sparkle_(mlp)",
            "pinkie_pie":"pinkie_pie_(mlp)",
            "fluttershy":"fluttershy_(mlp)",
            "rarity":"rarity_(mlp)",
            "scootaloo":"scootaloo_(mlp)",
            "sweetie_belle":"sweetie_belle_(mlp)",
            "applebloom":"applebloom_(mlp)",
            "gilda":"gilda_(mlp)",
            "best_pony":"twilight_sparkle_(mlp)"}

    E621ImageRegexDict = {"tags":r"<title>(.*?)</title>"}
    E621DefaultTags = ["friendship_is_magic"]
    if (not explicit):
        E621DefaultTags.append("-rating:explicit")
    else:
        E621DefaultTags.append("rating:explicit")
    E621 = Site("E621", "http://e621.net/post?tags=%s&searchDefault=Search", r"href=\"(/post/show/.*?)\"", E621DefaultTags, E621ImageRegexDict, E621TranslationDict)
    sites.append(E621)

    if (explicit):
        r34ImageRegexDict = {"tags":"<a class='tag_name' href='.*?'>(.*?)</a>"}
        FiveOhTwoBadGateway = Site("R34", "http://rule34.paheal.net/post/list/%s/1", r"href='(/post/view/.*?)'", ["friendship_is_magic"], r34ImageRegexDict, bestPonyDict)
        sites.append(FiveOhTwoBadGateway)


    if (not explicit):
        bronibooruImageRegexDict = {"tags":"<title>(.*?)</title>"}
        bronibooru = Site("Bronibooru", "http://bronibooru.mlponies.com/post?tags=%s&searchDefault=Search",  r"href=\"(/post/show/.*?)\"", [], bronibooruImageRegexDict, bestPonyDict)
        sites.append(bronibooru)
    return sites



class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        message = complete.message()
        explicit = False
        specificSite = None
        args = []
        for word in message.split():
            if (word[0]=="-"):
                if (word=="-explicit"):
                    explicit = True
                else:
                    specificSite = word[1:]
            else:
                args.append(word)
        sites = getSiteList(explicit)
        site = None
        if (specificSite!=None):
            for maybeSite in sites:
                if (maybeSite.Name.lower()==specificSite.lower()):
                    site = maybeSite 
        if (site == None):
            random.shuffle(sites)
            site = sites[0]

        message = ' '.join(args)

        try:
            try:
                site.Search(message)
            except urllib2.URLError:
                site = sites[1]
                site.Search(message)
            result = site.ResultImage
            return ["PRIVMSG $C$ :%s: %s"%(site.Name, result.ToString())]
        except Exception as e:
            return ["PRIVMSG $C$ :%s: %s"%(site.Name, e)]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
