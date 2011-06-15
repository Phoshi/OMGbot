# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import time
import re
import htmlentitydefs
class pluginClass(plugin):
    def gettype(self):
        return "postprocess"
    def action(self, complete):
        def unescape(text):
            def fixup(m):
                text = m.group(0)
                if text[:2] == "&#":
                    # character reference
                    try:
                        if text[:3] == "&#x":
                            return unichr(int(text[3:-1], 16))
                        else:
                            return unichr(int(text[2:-1]))
                    except ValueError:
                        pass
                elif text[:4]=="x26#":
                    return unichr(int(text[4:-1]))
                elif text[:2]=="\u":
                    return unichr(int(text[2:],16))
                else:
                    # named entity
                    try:
                        text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
                    except KeyError:
                        pass
                return text # leave as is
            text=re.sub("&#?\w+;", fixup, text)
            text=re.sub("x26#[0-9]+;", fixup, text)
            text=re.sub("\\\\u[0-9]+", fixup, text)
            return text
        return unescape(unescape(complete)) #Run twice because sometimes HTML identities get escaped - this isn't what we want.
    def describe(self, complete):
        msg=complete.message()
        sender=complete[0].split(' ')
        sender=sender[2]
        return ["PRIVMSG $C$ :I am the plugin that shows output loggery in the bot's terminal.","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :None."]
