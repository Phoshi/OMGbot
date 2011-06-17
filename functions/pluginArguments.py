# -*- coding: utf-8 -*-
if __name__!="__main__":
    import globalv
import traceback
class pluginArguments(object):
    def __init__(self, content):
        self.argument=content
    def message(self):
        try:
            message=self.argument[1:].split(' :',1)[1]
            if __name__!="__main__":
                message=message[len(globalv.commandCharacter):]
            message=' '.join(message.split()[1:])
            return message
        except Exception as e:
            print e
            return ""
    def fullMessage(self):
        try:
            message=self.argument[1:].split(' :',1)[1]
            return message
        except:
            return ""
    def cmd(self):
        message=self.argument[1:].split(' :',1)[1]
        if __name__!="__main__":
            message=message[len(globalv.commandCharacter):]
        return message.split()
    def channel(self):
        try:
            channel=self.argument[1:].split(' :',1)[0].split()
            if channel[1]=="PRIVMSG" or channel[1]=="PART" or channel[1]=="KICK":
                if __name__!="__main__":
                    if channel[2]==globalv.nickname:
                        return channel[0].split('!')[0].lower()
                return channel[2].lower()
            elif channel[1]=="JOIN":
                return self.argument[1:].split()[2].lower().strip(':')
            elif channel[1]=="MODE" or channel[1]=="TOPIC":
                return self.argument[1:].split()[2]
            return ""
        except Exception as e:
            print e
            return ""
    def user(self):
        return self.argument[1:].split()[0].split('!')[0]
    def userMask(self):
        return self.argument[1:].split()[0]
    def setMessage(self, message):
        self.argument=":"+' :'.join([self.argument[1:].split(' :',1)[0],message])
    def type(self):
        message=self.argument[1:] if self.argument[0]==":" else self.argument
        message=message.split(' :',1)[0].split()
        if message[0]=="PING":
            return "PING"
        else:
            return message[1]
    def complete(self):
        return self.argument
    def setComplete(self, complete):
        self.argument=complete

if __name__=="__main__":
    args=pluginArguments(":PY!apycalling@py.py PRIVMSG #sr388 :!ping")
    print args.user(), "said", args.message(), "in", args.channel()
    print args.userMask(), "is their hostmask, and the message type was a", args.type()
    print args.cmd()
