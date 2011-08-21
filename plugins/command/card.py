# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import random
class card(object):
    suit = ""
    rank = ""
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    def name(self):
        if (self.suit==""):
            return self.rank
        return "%s of %s"%(self.rank, self.suit)
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def __init__(self):
        self.cards = self.generateDeck()
    def generateDeck(self):
        suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
        ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
        cards=[]
        for suit in suits:
            for rank in ranks:
                cards.append(card(suit, rank))
        cards.append(card("", "Joker"))
        cards.append(card("", "Joker"))

        random.shuffle(cards)
        return cards

    def action(self, complete):
        if complete.message()=="shuffle":
            self.cards = self.generateDeck()
            return ["PRIVMSG $C$ :Shuffled the deck!"]
        if len(self.cards)==0:
            return ["PRIVMSG $C$ :Out of cards! Shuffle the deck, please"]
        newCard = self.cards.pop(0)
        return ["PRIVMSG $C$ :%s"%newCard.name()]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
