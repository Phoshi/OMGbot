# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        streams = globalv.communication["drawfriendStreams"]
        activeStreams = []
        for stream in streams:
            if stream.isLive:
                activeStreams.append(stream)

        message = " - ".join(["%s: %s%s"%(stream.getName(), stream.getChannel(), " \x02Thread:\x02 %s"%stream.getThread() if stream.getThread()!="" else "") for stream in activeStreams])
        if message == "":
            message = "Nobody."
        return ["PRIVMSG $C$ :Now Streaming: %s"%message]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
