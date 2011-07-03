# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import re
import urllib
import urllib2
import xml.sax.saxutils
from bitlyServ import bitly
import mimetypes
import time
import settingsHandler
def fixXMLEntities(match):
    value=int(match.group()[2:-1])
    return chr(value)
def parseYoutube(url, pageData):
    if re.findall("watch\?v=", url)!=[]:
        title=re.findall("<\s*title\s*>.*YouTube -[\s]*(.*?)</title\s*>", pageData, re.I)[0]
        uploader = re.findall(r"user/(.*?)\"", pageData, re.I)[0]
        print uploader
        print pageData.find('length_seconds')
        length = re.findall(r"amp;length_seconds=([0-9]*)", pageData)[0]
        print length
        length = time.strftime("%M:%S", time.gmtime(int(length)))
        return ["PRIVMSG $C$ :Video: %s by %s (%s)"%(title.decode('utf-8'),uploader,length)]
    else:
        title=re.findall("<\s*title\s*>(.*?)</title\s*>", pageData, re.I)[0]
        domain = re.search("(?P<url>https?://[^/\s]+)", url).group("url")
        return ["PRIVMSG $C$ :Title: %s (at %s)" % (title.decode('utf-8'), domain.decode('utf-8'))]

def doNothing(url, pageData):
    return [""]
def parseAdfly(url, pageData):
    realUrl = re.findall("var url = '(.*?)'",pageData)[0]
    Req = urllib2.Request(realUrl,None,{"User-Agent":"Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"})
    response=urllib2.urlopen(Req,None, 15)
    page=response.read(50000)
    page=page.replace('\n','')
    fullURL=response.geturl()
    title=re.findall("<\s*title\s*>(.*?)</title\s*>", page, re.I)
    if len(title)>0:
        title=title[0]
        title=re.sub("\s\s+", " ", title).strip()
        domain = re.search("(?P<url>https?://[^/\s]+)", fullURL).group("url")
        return ['PRIVMSG $C$ :Title: '+title.decode('utf-8')+ ' (at '+domain.decode('utf-8')+')']
    else:
        return ['PRIVMSG $C$ :Target URL: %s'%fullURL]
def parsePonibooru(url, pageData):
    tags = re.findall("value='([^']*)' id='tag_editor'>", pageData)[0]
    stats = re.findall("<div id='Statisticsleft'>(.*?<)/div>", pageData)[0]
    print stats
    id = re.findall("Id:\s([0-9]*)", stats)[0]
    print id
    size = re.findall("Size: (.+?)<", stats)[0].strip()
    print size
    filesize = re.findall("Filesize: (.+?)<", stats)[0].strip()
    print filesize
    source = re.findall("Source: <a href='(.+?)'", stats)
    if (source != []):
        source = source[0].strip()
        if len(source) > 20:
            source = bitly(source)
    else:
        source = ""
    return ["PRIVMSG $C$ :Image Tags: %s; Dimensions: %s; Filesize: %s; %s"%(tags, size, filesize, "Source: %s;"%source if source!="" else "")]
class pluginClass(plugin):
    def __init__(self):
        self.specialDomains={"http://www.youtube.com":parseYoutube, "http://adf.ly":parseAdfly,
                "https?://[^.]*.deviantart.com":doNothing, "http://ponibooru.413chan.net":parsePonibooru}
    def gettype(self):
        return "realtime"
    def __init_db_tables__(self, name):
        settingsHandler.newTable(name, "showDomainLink")
        settingsHandler.writeSetting(name, ["showDomainLink"], ["true"])
    def getDomainMatch(self, domain):
        print "Matching",domain
        for key in self.specialDomains.keys():
            print "Trying",key
            if re.match(key, domain)!=None:
                print "Matched",key
                return key
        print "No match"
        return False
    def action(self, complete):
        complete=complete.complete()[1:].split(' :',1)
        showDomain = True if settingsHandler.readSetting("urlFollow", "showDomainLink")=="true" else False
        if len(complete[0].split())>2:
            if complete[0].split()[1]=="PRIVMSG":
                msg=complete[1]
                sender=complete[0].split(' ')
                sender=sender[2]
                if msg.find('http://')!=-1 or msg.find('https://')!=-1:

                    url = re.search(".*(?P<url>https?://[^\s#]+)", msg).group("url")
                    print url
                    if url[-1]=="":
                        url=url[0:-1]
                    if msg.split()[0]=="ACTION":
                        return [""]
                    domain = re.search("(?P<url>https?://[^/\s]+)", msg).group("url")
                    isDomain=re.findall("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", domain)
                    if isDomain!=[]:
                        return [""]
                    try:
                        try:
                            Req = urllib2.Request(url,None,{"User-Agent":"Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"})
                            response=urllib2.urlopen(Req,None, 15)
                            page=response.read(50000)
                            page=page.replace('\n','')
                            fullURL=response.geturl()
                            domain = re.search("(?P<url>https?://[^/\s]+)", fullURL).group("url")

                        except Exception as detail:
                            print detail
                            if str(detail)!="<urlopen error [Errno -2] Name or service not known>":
                                return ["PRIVMSG $C$ :URLFollow Error: "+str(detail)]
                        if not self.getDomainMatch(domain):
                            title=re.findall("<\s*title\s*>(.*?)</title\s*>", page, re.I)
                            if len(title)>0:
                                title=title[0]
                                title=re.sub("\s\s+", " ", title).strip()
                                return ['PRIVMSG $C$ :Title: '+title.decode('utf-8')+ (' (at '+domain.decode('utf-8')+')' if showDomain else "")]
                            else:
                                if url!=fullURL:
                                    return ['PRIVMSG $C$ :Target URL: %s'%fullURL]
                        else:
                            return self.specialDomains[self.getDomainMatch(domain)](url, page)
                    except Exception as detail:
                        print "Exception:",detail
        return [""]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the plugin that follows URLs","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :None - I monitor all input, if you have a url in your text, I will find it."]
