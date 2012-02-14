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
        self.languages = {}
        for a,b in self.langTable:
            self.languages[a] = b
            self.languages[a.lower()] = b
            self.languages[b] = a

    def gettype(self):
        return "command"

    def action(self, complete):
        msg=str(complete.message()); #######

        if (msg == ""):
            return ["PRIVMSG $C$ :Invalid Parameters"]

        args = shlex.split(msg)

        langFrom = "auto"
        langTo = "en"

        text = args[0]

        if len(args) >= 3:
            if args[1] == 'to':
                try:
                    langTo = self.languages[args[2].lower()]
                    if len(langTo) > 2:
                        raise Exception()
                except:
                    return ["PRIVMSG $C$ :Translation failure! :("]
                if len(args) > 3 and args[3] == 'from':
                    try:
                        langFrom = self.languages[args[4].lower()]
                        if len(langFrom) > 2:
                            raise Exception()
                    except:
                        return ["PRIVMSG $C$ :Translation failure! :("]
            elif args[1] == 'from':
                try:
                    langFrom = self.languages[args[2].lower()]
                    if len(langFrom) > 2:
                        raise Exception()
                except:
                    return ["PRIVMSG $C$ :Translation failure! :("]
                if len(args) > 3 and args[3] == 'to':
                    try:
                        langTo = self.languages[args[4].lower()]
                        if len(langTo) > 2:
                            raise Exception()
                    except:
                        return ["PRIVMSG $C$ :Translation failure! :("]
            else:
                text = ' '.join(args)
        else:
            text = ' '.join(args)

        query = urllib.urlencode({"text": text})
        url = "http://translate.google.com/translate_a/t?client=t&%s&hl=en&sl=%s&tl=%s&multires=1&otf=2&ssel=4&tsel=4&sc=1" % (query, langFrom, langTo)

        headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:8.0) Gecko/20100101 Firefox/8.0',
                    'Referer': 'http://translate.google.com/'}
        req=urllib2.urlopen(urllib2.Request(url, headers=headers))
        content=req.read()

        print content

        encoding=req.headers['content-type'].split('charset=')[-1]
        ucontent = unicode(content, encoding)

        #Parse source language
        sourceLanguage = re.search(',"(\w+)",,', ucontent)
        if sourceLanguage is None:
            sourceLanguage = ''
        else:
            sourceLanguage = sourceLanguage.group(1)

        if sourceLanguage in self.languages:
            sourceLanguage = self.languages[sourceLanguage]
        else:
            sourceLanguage = ''
            
        #Parse translation
        translation = re.search('\[\[\["(.+?)"', ucontent)
        if translation is None:
            return ["PRIVMSG $C$ :Translation failure! :("]
        translation = translation.group(1)

        if sourceLanguage != '':
            return ["PRIVMSG $C$ :" + translation + " (translated from "+sourceLanguage+")"]
        else:
            return ["PRIVMSG $C$ :" + translation]


    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !translate module",
                "PRIVMSG $C$ :Example usage:",
                "PRIVMSG $C$ :!translate \"The cake is a lie!\" to German",
                "PRIVMSG $C$ :!translate \"Mark Borgerding died for our sins!\" to Italian",
                "PRIVMSG $C$ :!translate \"Het is meer dan negenduizend!\""]
