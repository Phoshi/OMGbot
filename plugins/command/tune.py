from plugins import plugin
from bitlyServ import bitly

import re
import wave
import math

class pluginClass( plugin ):
    def gettype(self):
        return "command"
    
    def __init__(self):
        self.functions = {'sine':self.sine,
                          'triangle':self.triangle,
                          'square':self.square,
                          'saw':self.sawup,
                          'sawup':self.sawup,
                          'sawdown':self.sawdown
                          }
        
        self.re_settings = re.compile('(%s)?\s*(\d+)?[.+o-]' % ('|'.join(self.functions.keys())))
        self.re_term = re.compile('(?P<duration>[.+o-]+)(?P<notes>((?:[a-g][b#]?[1-8]|#))+)')
        self.re_init = re.compile('([.+o-]+(?:[^.+o-]|\s)+)\s*')
        self.re_note = re.compile('[a-g][b#]?[1-8]')
        self.deltas = {}

        self.framerate = 22050

        self.deltas['#'] = 0

        for i in range(1,8):
            oc = str(i)
            ocf = 13.75 * (2 ** i)
            self.deltas['c' + oc]  = ocf * (2 ** (3/12.0)) / self.framerate
            
            self.deltas['c#' + oc] = ocf * (2 ** (4/12.0)) / self.framerate
            self.deltas['db' + oc] = self.deltas['c#' + oc]
            
            self.deltas['d' + oc]  = ocf * (2 ** (5/12.0)) / self.framerate
            
            self.deltas['d#' + oc] = ocf * (2 ** (6/12.0)) / self.framerate
            self.deltas['eb' + oc] = self.deltas['d#' + oc]
            
            self.deltas['e' + oc]  = ocf * (2 ** (7/12.0)) / self.framerate
            
            self.deltas['f' + oc]  = ocf * (2 ** (8/12.0)) / self.framerate
            
            self.deltas['f#' + oc] = ocf * (2 ** (9/12.0)) / self.framerate
            self.deltas['gb' + oc] = self.deltas['f#' + oc]
            
            self.deltas['g' + oc]  = ocf * (2 ** (10/12.0)) / self.framerate
            
            self.deltas['g#' + oc] = ocf * (2 ** (11/12.0)) / self.framerate
            self.deltas['ab' + oc] = self.deltas['g#' + oc]
            
            self.deltas['a' + oc]  = 2 * ocf / self.framerate

            self.deltas['a#' + oc] = 2 * ocf * (2 ** (1/12.0)) / self.framerate
            self.deltas['bb' + oc] = self.deltas['a#' + oc]
            
            self.deltas['b' + oc]  = 2 * ocf * (2 ** (2/12.0)) / self.framerate

    def sine(self, phase):
        return math.sin(phase * 2 * math.pi)

    def square(self, phase):
        return (1 if phase < 0.5 else -1)

    def triangle(self, phase):
        if phase < 0.5:
            return -1+phase*4
        else:
            return 1-(phase-0.5)*4

    def sawup(self, phase):
        return phase*2-1

    def sawdown(self, phase):
        return 1-phase*2

    def action(self, complete):
        m = complete.message().lower()

        fileName = complete.user() + '.wav'

        settings = self.re_settings.match(m)
        if settings:
            if settings.group(1) and settings.group(1) in self.functions:
                f = self.functions[settings.group(1)]
            else:
                f = self.triangle
                
            if settings.group(2):
                bpm = int(settings.group(2))
            else:
                bpm = 120
        else:
            f = self.triangle
            bpm = 120

        speed = 60.0 * self.framerate / (bpm * 4)

        if speed < 300:
            return ["PRIVMSG $C$ :Range error: too fast."]
        
        terms = self.re_init.findall(m)

        if len(terms) == 0:
            return ["PRIVMSG $C$ :Parsing error: please revise your tune."]

        data = ''

        d = {}

        currentlyPlaying = []

        for note in self.deltas:
            d[note] = 0

        length = 0

        durations = {}
        termnotes = {}

        for term in terms:
            m = self.re_term.match(term)
            if m == None:
                return ["PRIVMSG $C$ :Error: Could not parse term %s" % term]
            
            notes = self.re_note.findall(term)

            for note in notes:
                if not note in d:
                    return ["PRIVMSG $C$ :Error: Note %s not supported." % note]

            termnotes[term] = set(notes)
            
            duration = 0
            for c in m.group('duration'):
                if c == '.':
                    duration += 1
                elif c == '-':
                    duration += 2
                elif c == '+':
                    duration += 4
                elif c == 'o':
                    duration += 8
            durations[term] = duration

            length += duration * speed

        if length > 2300000:
            return ["PRIVMSG $C$ :Error: estimated file size too large."]
            
        for term in terms:
            duration = durations[term]
            notes = termnotes[term]
            
            m = self.re_term.match(term)

            i = 0

            for note in d:
                if not note in notes:
                    d[note] = 0

            fade = 1
            while i < duration * speed:
                a = 0
                for note in notes:
                    d[note] += self.deltas[note]
                    if d[note] > 1:
                        d[note] -= 1
                    a += f(d[note])

                a = min(max(int(32767.5 * a * fade / 4),-32768),32767)
                
                data += wave.struct.pack('h', a)
                i += 1
                fade -= 0.00001
                if fade < 0:
                    fade = 0
                            
        w = wave.open('/home/py/public_html/tunes/' + fileName, 'wb')
        w.setframerate(self.framerate)
        w.setnchannels(1)
        w.setsampwidth(2)
        w.writeframes(data)
        w.close()

        return ['PRIVMSG $C$ :' + bitly('http://terminus.mrflea.net:81/~py/tunes/' + fileName)]

    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !tune module. ",
                "PRIVMSG $C$ :To create a tune, the argument string has to have the following format:",
                "PRIVMSG $C$ :tune = ['sine'|'square'|'triangle'][bpm](duration note octave)+",
                "PRIVMSG $C$ :BPM is optional (default value of 120)",
                "PRIVMSG $C$ :duration is a sum of symbols: .-+o would mean '.' (1/16th) + '-' (1/8th) + '+' (1/4th) + 'o' (half) = note length of 15/16th ",
                "PRIVMSG $C$ :note is one of the following values: A, A#, Bb, C, C#, Db, D, D#, Eb, E, F, F#, G, G#, Ab",
                "PRIVMSG $C$ :octave has to lie in the range [1,7] - from C1 to B7"
                ]
            
                
