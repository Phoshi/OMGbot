# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import re
import htmllib
import random
import urllib2,urllib
import settingsHandler
import random

def unescape(s):
    p = htmllib.HTMLParser(None)
    p.save_bgn()
    p.feed(s)
    return p.save_end()

class pluginClass(plugin):
    def __init_db_tables__(self, name):
        settingsHandler.newTable(name, "showTitle","showLink","showLyrics","showPreview")
        settingsHandler.writeSetting(name,["showTitle","showLink","showLyrics","showPreview"],["True","False","False","False"])
    def __init__(self):
        url = 'http://ocremix.org/'
        response = urllib2.urlopen(url)
        page = response.read()
        result = re.findall("<a href=\"/remix/OCR([0-9]*)/\">", page)
        result.sort()
        self.songID=int(result[-1])
    def gettype(self):
        return "command"
    def action(self, complete):
        def isNumber(string):
            try:
                int(string)
                return True
            except:
                return False
        msg=complete.message()
        showTitle=True if settingsHandler.readSetting(complete.cmd()[0],"showTitle")=="True" else False
        showLink=True if settingsHandler.readSetting(complete.cmd()[0],"showLink")=="True" else False
        showLyrics=True if settingsHandler.readSetting(complete.cmd()[0],"showLyrics")=="True" else False
        showPreview=True if settingsHandler.readSetting(complete.cmd()[0],"showPreview")=="True" else False
        songID=random.randint(0,self.songID)+1
        page=False
        try:
            if msg!="" and msg!="latest":
                if isNumber(msg)==False:
                    url="http://ocremix.org/quicksearch/remix/?qs_query="+msg.replace(' ','+')
                    response = urllib2.urlopen(url)
                    page=response.read() 
                    ID=re.findall("<a href=\"/remix/OCR([0-9]*)/\" ",page)
                    songID=int(ID[0])
                elif int(msg)>0:
                    songID=int(msg)
                else:
                    print songID, self.songID
                    songID=self.songID+int(msg)

            elif msg=="latest":
                url = 'http://ocremix.org/'
                response = urllib2.urlopen(url)
                page = response.read()
                result = re.findall("<a href=\"/remix/OCR([0-9]*)/\">", page)
                result.sort()
                self.songID=int(result[-1])
                songID=self.songID
            page=False
            while page==False:
                try:
                    url="http://ocremix.org/remix/OCR"+str(songID).rjust(5,"0")+"/"
                    response = urllib2.urlopen(url)
                    page=response.read()
                except:
                    songID=random.randint(0,self.songID)+1
            remixer=re.findall("ReMixer\(s\)</strong>:.(.*?)</li>",page)
            remixer=re.findall("<a href=[^>]*>([^<]*)</a>",''.join(remixer))
            remixed=re.findall("Song\(s\)</strong>:.(.*?)</li>",page)
            remixed=re.findall("<a href=[^>]*>([^<]*)</a>",''.join(remixed))
            albumName=re.findall("Album</strong>: Featured on.(.*?)</li>",page)
            if albumName!=[]:
                albumName=re.findall("<a href=[^>]*>([^<]*)</a>",''.join(albumName))[0]
            else:
                albumName=""
            links=re.findall("<a href=\"(.*?)\">Download from .*?</a>",page)
            random.shuffle(links)
            remixer=', '.join(remixer)
            remixed=', '.join(remixed)
            result = re.findall("<title>([^<]*)</title>", page)
            title=result[0]
            title='-'.join(title.split(' - ')[:-1])
            try:
                if showLyrics:
                    lyrics=re.findall('<div id="panel-lyrics" style="display:none;">(.*?)</div>',page.replace('\n','||'))[0]
                    lyrics=re.sub("<.*?>","",lyrics)
                    lyrics=re.sub("^[\|\s]+","",lyrics).replace('||','\n')
                    if re.findall("[a-zA-Z]",lyrics)==[]:
                        lyricsLink=""
                        raise Exception("Lyrics empty!")
                    data={"paste_code":lyrics,"paste_private":1,"paste_expire_date":"10M"}
                    data=urllib.urlencode(data)
                    request=urllib2.Request("http://pastebin.com/api_public.php",data)
                    lyricsLink=" - "+urllib2.urlopen(request).read()
                else:
                    lyricsLink=""
            except:
                lyricsLink=""
            previewLink=" - http://youtube.com/watch?v="
            youtubeURL=re.findall("http://www.youtube.com/v/(.*?)&",page)
            if youtubeURL!=[] and showPreview:
                previewLink+=youtubeURL[0]
            else:
                previewLink=""
            output=("\x0312Random" if msg=="" else "\x0313Returned")+" OC Remix\x03: OCR"+str(songID).rjust(5,"0")+", "+(("\x0312"+title+'\x03 of \x0312'+remixed+'\x03 by \x0312'+remixer+'\x03'+((' from \x0312'+albumName+'\x03') if albumName!="" else "")+' - ') if showTitle==True else "")+(url if showLink==False else links[0]) + lyricsLink + previewLink
        except Exception as detail:
            detail=str(detail)
            if detail=="HTTP Error 404: Not Found":
                failureReason="404: Song not found"
            elif detail=="list index out of range":
                failureReason="No results"
            else:
                failureReason=detail
            output="No OC Remix: "+failureReason
        return ["PRIVMSG $C$ :"+output.decode('utf-8')]
    def describe(self, complete):
        msg=complete.message()
        return ["PRIVMSG $C$ :I am the !ocr module, I handle OCRemix functions!","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!ocr [OPTIONAL ocr ID | Text to search for | latest]"]
