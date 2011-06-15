# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import urllib2
import urllib
import shlex
import re


class pluginClass(plugin):
    def __init__(self):
        self.langTable = [('Afrikaans', 'af'),
                          ('Albanian', 'sq'),
                          ('Arabic', 'ar'),
                          ('Armenian', 'hy'),
                          ('Azerbaijani', 'az'),
                          ('Basque', 'eu'),
                          ('Belarusian', 'be'),
                          ('Bulgarian', 'bg'),
                          ('Catalan', 'ca'),
                          ('Croatian', 'hr'),
                          ('Czech', 'cs'),
                          ('Danish', 'da'),
                          ('Dutch', 'nl'),
                          ('English', 'en'),
                          ('Estonian', 'et'),
                          ('Filipino', 'tl'),
                          ('Finnish', 'fi'),
                          ('French', 'fr'),
                          ('Galician', 'gl'),
                          ('Georgian', 'ka'),
                          ('German', 'de'),
                          ('Greek', 'el'),
                          ('Haitian Creole', 'ht'),
                          ('Hebrew', 'iw'),
                          ('Hindi', 'hi'),
                          ('Hungarian', 'hu'),
                          ('Icelandic', 'is'),
                          ('Indonesian', 'id'),
                          ('Irish', 'ga'),
                          ('Italian', 'it'),
                          ('Japanese', 'ja'),
                          ('Korean', 'ko'),
                          ('Latin', 'la'),
                          ('Latvian', 'lv'),
                          ('Lithuanian', 'lt'),
                          ('Macedonian', 'mk'),
                          ('Malay', 'ms'),
                          ('Maltese', 'mt'),
                          ('Norwegian', 'no'),
                          ('Persian', 'fa'),
                          ('Polish', 'pl'),
                          ('Portuguese', 'pt'),
                          ('Romanian', 'ro'),
                          ('Russian', 'ru'),
                          ('Serbian', 'sr'),
                          ('Slovak', 'sk'),
                          ('Slovenian', 'sl'),
                          ('Spanish', 'es'),
                          ('Swahili', 'sw'),
                          ('Swedish', 'sv'),
                          ('Thai', 'th'),
                          ('Turkish', 'tr'),
                          ('Ukrainian', 'uk'),
                          ('Urdu', 'ur'),
                          ('Vietnamese', 'vi'),
                          ('Welsh', 'cy'),
                          ('Yiddish', 'yi')]

    def gettype(self):
        return "command"

    def action(self, complete):
        msg=str(complete.message()); #######

        print msg

        if (msg == ""):
            return ["PRIVMSG $C$ :Invalid Parameters"]

        args = shlex.split(msg)

        if (len(args) != 1 and len(args) != 3 and len(args) != 5):
            return ["PRIVMSG $C$ :Invalid Parameters (Wrong number of arguments)"]

        langFrom = ""
        langTo = "en"

        if (len(args) >= 3):
            args[1]=str(args[1])
            if (args[1] == "to"):
                langTo=""
                for x in self.langTable:
                    if (x[0].lower()==args[2].lower()):
                        langTo=x[1]
                        break
                if (langTo==""):
                    return ["PRIVMSG $C$ :Cannot translate to " + args[2] + ", sorry!"]
            elif (args[1] == "from"):
                langFrom=""
                for x in self.langTable:
                    if (x[0].lower()==args[2].lower()):
                        langFrom=x[1]
                        break
                if (langTo==""):
                    return ["PRIVMSG $C$ :Cannot translate to " + args[2] + ", sorry!"]
            else:
                return ["PRIVMSG $C$ :Invalid Parameters (Use double quotes (\") to translate a sentence.)"]

        if (len(args) == 5):
            if (args[3] == args[2]):
                return ["PRIVMSG $C$ :Invalid Parameters (Args 3 and 2 are identical)"]
            if (args[3] == "to"):
                langTo=""
                for x in self.langTable:
                    if (x[0].lower()==args[4].lower()):
                        langTo=x[1]
                        break
                if (langTo==""):
                    return ["PRIVMSG $C$ :Cannot translate to " + args[4] + ", sorry!"]
            elif (args[3] == "from"):
                langFrom=""
                for x in self.langTable:
                    if (x[0].lower()==args[4].lower()):
                        langFrom=x[1]
                        break
                if (langTo==""):
                    return ["PRIVMSG $C$ :Cannot translate to " + args[4] + ", sorry!"]
            else:
                return ["PRIVMSG $C$ :Invalid Parameters (Use double quotes (\") to translate a sentence.)"]

        #text = unicode(args[0], 'utf-8')
        #query = urllib.urlencode(dict([["q",text.encode('utf-8')]]))
        query = urllib.urlencode(dict([["q",args[0]]]))
        url = "http://www.google.com/uds/Gtranslate?callback=google.language.callbacks.id101&context=22&langpair="+langFrom+"|"+langTo+"&key=notsupplied&v=1.0&"+query

        req=urllib2.urlopen(url)
        content=req.read()

        encoding=req.headers['content-type'].split('charset=')[-1]
        ucontent = unicode(content, encoding)

        start = ucontent.find('"translatedText":"') + 18
        if (langFrom==""):
            end = ucontent.find('","det')
            if (end==-1):
                if (ucontent.find('could not reliably detect source language')>-1):
                    return ["PRIVMSG $C$ :Could not reliably detect source language."]
                else:
                    return ["PRIVMSG $C$ :Translation failure! :("]
            detectedLang = ucontent[end+28:end+30]

        else:
            end = ucontent.find('"}')
            detectedLang = langFrom

        langFrom="an unknown language"
        for x in self.langTable:
            if (x[1]==detectedLang):
                langFrom=x[0]
                break

        translation = ucontent[start:end]
        print translation

        return ["PRIVMSG $C$ :" + translation + " (translated from "+langFrom[0].capitalize()+langFrom[1:]+")"]


    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !translate module",
                "PRIVMSG $C$ :Example usage:",
                "PRIVMSG $C$ :!translate \"The cake is a lie!\" to German",
                "PRIVMSG $C$ :!translate \"Mark Borgerding died for our sins!\" to Italian",
                "PRIVMSG $C$ :!translate \"Het is meer dan negenduizend!\""]
