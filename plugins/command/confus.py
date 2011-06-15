from plugins import plugin
import globalv
from random import shuffle
import string
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def action(self, complete):
        lx = [ord(c) for c in string.ascii_lowercase]
        ly = lx[:]
        ux = [ord(c) for c in string.ascii_uppercase]
        uy = ux[:]
        nx = [ord(c) for c in string.digits]
        ny = nx[:]
        px = [ord(c) for c in string.punctuation]
        py = px[:]
        shuffle(lx)
        shuffle(ly)
        shuffle(ux)
        shuffle(uy)
        shuffle(nx)
        shuffle(ny)
        shuffle(px)
        shuffle(py)
        return ["PRIVMSG $C$ :" + unicode(complete.message(), 'utf-8').translate(dict(zip(lx + ux + nx + px, ly + uy + ny + py))).encode('utf-8')]
    def describe(self, complete):
        return ["PRIVMSG $C$ :changes letters to other letters! :D"]
