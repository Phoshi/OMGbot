# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        streams = globalv.variables["drawfriendStreams"]
        activeStreams = []
        for stream in streams:
            if stream.isLive:
                activeStreams.append(stream)

        message = "; ".join(["%s: %s"%(stream.getName(), stream.getChannel()) for stream in activeStreams])
        if message == "":
            message = "Nobody."
        return ["PRIVMSG $C$ :Now Streaming: %s"%message]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
