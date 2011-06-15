from plugins import plugin
import globalv
import itertools
class pluginClass(plugin):
    colors = itertools.cycle(['\x03' + '{0:02d}'.format(i) for i in [4, 7, 8, 9, 11, 12, 13, 6]])
    def gettype(self):
        return "command"
    def action(self, complete):
        return ["PRIVMSG $C$ :" + ''.join([next(self.colors) + c for c in complete.message()]) + "\x03"]
    def describe(self, complete):
        return ["PRIVMSG $C$ :zephyrtronium improved rainbow :)"]
