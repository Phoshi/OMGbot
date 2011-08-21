# -*- coding: utf-8 -*-
from plugins import plugin
import globalv

import urllib, urllib2, cookielib
import difflib
import re

class Akinator:
    answers = {
        'yes': 0,
        'very': 0,
        
        'no': 1,
        'not at all': 1,
        
        'i don\'t know': 2,
        'dunno': 2,
        'maybe': 2,
        
        'probably': 3,
        'i think so': 3,
        'kind of': 3,
        'kinda': 3,
        'sorta': 3,
        'partially': 3,
        
        'probably not': 4,
        'unlikely': 4,
        'not really': 4,
        'i think not': 4,
    }

    end_answers = {
        'yes': 0,
        'no': 1,
        'not exactly': 1,
        'too general': 1,
    }
    
    current_page = ''

    session_ended = False

    def newSession(self):
        urllib2.install_opener(urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar())))
        
        c = urllib2.urlopen('http://en.akinator.com/new_session.php?prio=0&joueur=OMGbot&partner_id=0&age=23&sexe=M&email=&ms=0&remember=0&engine=0')
        self.current_page = c.read()
        question = re.search('<br>(.+?)<script', self.current_page).group(1)
        self.partie, self.signature = re.search('commenceSession\((\d+),(\d+)', self.current_page).groups()
        self.next_url = 'http://en.akinator.com/repondre_propose.php?prio=0&partie=%s&signature=%s&nqp=0&trouvitude=0&reponse=%s&step_prop=-1&fq=&engine=0' % (self.partie, self.signature, '%d')
        self.question_number = 0
        self.has_solution = False
        self.session_ended = False
        return [("PRIVMSG $C$ :Question N\xb0 1: %s" % question).decode('latin-1')]

    def answer(self, answer):
        if self.session_ended:
            return ["PRIVMSG $C$ :Please start a new game by typing !akinator new"]

        if self.has_solution:
            answer = answer.lower()
            close_matches = difflib.get_close_matches(answer, self.end_answers)
            if len(close_matches) > 1 and close_matches[0] != answer:
                return ["PRIVMSG $C$ :Did you mean: '%s'" % "', '".join(close_matches)]
            if len(close_matches) == 0:
                return ["PRIVMSG $C$ :I cannot accept that as an answer."]

            match = self.end_answers[close_matches[0]]
            if match == 0:
                self.session_ended = True
                return ["PRIVMSG $C$ :Great! Guessed right one more time! I love playing with you!"]

            if self.question_number == 40:
                self.session_ended = True
                c = urllib2.urlopen('http://en.akinator.com/liste_best.php?prio=0&partie=%s&signature=%s&nqp=40&age=23&engine=0' % (self.partie, self.signature))
                self.current_page = c.read()
                alts = re.findall('>([^<>]+)</a></td>', self.current_page)
                alts = [("PRIVMSG $C$ :\x1f%s\x1f" % '\x1f, \x1f'.join(alts)).decode('latin-1')]
                return ["PRIVMSG $C$ :Bravo! You have defeated me. Other things I was thinking of:"] + alts            
            url = self.next_url
            self.has_solution = False
        else:
            answer = answer.lower()
            close_matches = difflib.get_close_matches(answer, self.answers)
            if len(close_matches) > 1 and close_matches[0] != answer:
                return ["PRIVMSG $C$ :Did you mean: '%s'" % "', '".join(close_matches)]
            if len(close_matches) == 0:
                return ["PRIVMSG $C$ :I cannot accept that as an answer."]
            
            match = close_matches[0]
            self.response = self.answers[match]

            url = self.next_url % self.response
        
        c = urllib2.urlopen(url)
        self.current_page = c.read()

        if 'I think of ...' in self.current_page:
            solution = re.search('ouvre_photo\(".+?",-?\d+,"(.+?)","(.*?)",\d+', self.current_page)
            if len(solution.group(2)) > 0:
                solution = solution.group(1) + " (%s)" % solution.group(2)
            else:
                solution = solution.group(1)
            self.next_url = 'http://en.akinator.com/continue_partie.php?prio=0&partie=%s&signature=%s&nqp=%d&age=23&engine=0' % (self.partie, self.signature, self.question_number)
            print self.next_url
            self.has_solution = True
            return [("PRIVMSG $C$ :I think of ... %s" % solution).decode('latin-1')]

        self.next_url = re.search('window.location="(.+?)"', self.current_page).group(1)
        self.next_url = 'http://en.akinator.com/%s%s&step_prop=-1' % (self.next_url, '%d')

        question = re.search('</center>([^<]+)', self.current_page).group(1)
        self.question_number = int(re.search('Question N\xb0 (\d+)', self.current_page).group(1))
        return [("PRIVMSG $C$ :Question N\xb0 %d: %s" % (self.question_number, question)).decode('latin-1')]

class pluginClass(plugin):
    def __init__(self):
        self.akinators = {}

    def gettype(self):
        return "command"
        
    def action(self,complete):
        channel = complete.channel()
                
        msg = complete.message()

        if channel not in self.akinators:
            self.akinators[channel] = Akinator()

        if msg == 'new':
            return self.akinators[channel].newSession()
        else:
            return self.akinators[channel].answer(msg)

    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the akinator plugin! Say !akinator new to start a new game."]
