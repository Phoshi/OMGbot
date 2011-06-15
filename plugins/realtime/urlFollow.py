# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import re
import urllib
import urllib2
import xml.sax.saxutils
import mimetypes
import time
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
class pluginClass(plugin):
    def __init__(self):
        self.specialDomains={"http://www.youtube.com":parseYoutube, "http://adf.ly":parseAdfly}
    def gettype(self):
        return "realtime"
    def action(self, complete):
        complete=complete.complete()[1:].split(':',1)
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

                        except Exception as detail:
                            print detail
                            if str(detail)!="<urlopen error [Errno -2] Name or service not known>":
                                return ["PRIVMSG $C$ :URLFollow Error: "+str(detail)]
                        if domain not in self.specialDomains:
                            title=re.findall("<\s*title\s*>(.*?)</title\s*>", page, re.I)
                            if len(title)>0:
                                title=title[0]
                                title=re.sub("\s\s+", " ", title).strip()
                                return ['PRIVMSG $C$ :Title: '+title.decode('utf-8')+ ' (at '+domain.decode('utf-8')+')']
                            else:
                                if url!=fullURL:
                                    return ['PRIVMSG $C$ :Target URL: %s'%fullURL]
                        else:
                            return self.specialDomains[domain](url, page)
                    except Exception as detail:
                        print "Exception:",detail
        return [""]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the plugin that follows URLs","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :None - I monitor all input, if you have a url in your text, I will find it."]
