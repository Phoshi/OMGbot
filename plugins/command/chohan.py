# -*- coding: utf-8 -*-
from plugins import plugin
import globalv
import random
import settingsHandler
class pluginClass(plugin):
    def gettype(self):
        return "command"
    def __init_db_tables__(self, name):
        if settingsHandler.tableExists("chohan")==False:
            settingsHandler.newTable("chohan", "nick","points")
    def __init__(self):
        self.total=0
        self.userGuesses={}
        self.userScores={}
        self.prize=100
        self.dice=[]
    def action(self, complete):
        msg=complete.message().split()
        nick=complete.user()
        if self.userScores=={}:
            userScores=settingsHandler.readSetting("chohan","nick, points")
            print userScores
            if len(userScores)!=2 and type(userScores[1])!=unicode:
                for user, score, in userScores:
                    self.userScores[user]=int(score)
            else:
                user, score=userScores
                self.userScores[user]=int(score)
        if msg[0].lower()=="guess":
            if self.total==0:
                return ["PRIVMSG $C$ :Nobody's rolled the dice, yet! Roll with roll!"]
            elif nick not in self.userGuesses.keys():
                self.userGuesses[nick]=msg[1]
            else:
                return ["PRIVMSG $C$ :You have already guessed!"]
            msg="Today could be your lucky day! Putting 1/5th of your points into the pot for a total prize of "
            if nick in self.userScores.keys():
                self.prize+=(self.userScores[nick]/5)+100
                self.userScores[nick]-=self.userScores[nick]/5
            msg+=str(self.prize)
        elif msg[0].lower()=="roll":
            if self.total==0:
                self.total=0
                self.dice=[]
                for i in range(2):
                    rtd=random.randint(1,6)
                    self.total+=rtd
                    self.dice.append(rtd)
                    print i,rtd
                self.prize=100
                msg="Dice rolled!"
            else:
                msg="Dice already rolled! Start guessing!"
        elif msg[0].lower()=="reveal":
            if self.total==0:
                return ["PRIVMSG $C$ :No game in progress!"]
            print "revealan"
            oddEven="odd!" if self.total % 2 !=0 else "even!"
            winners=[]
            msg=["PRIVMSG $C$ :The result is "+oddEven+" ("+str(self.dice[0])+"+"+str(self.dice[1])+")"]
            print "winnerappendan"
            for user in self.userGuesses.keys():
                if self.userGuesses[user]==oddEven[:-1]:
                    winners.append(user)
            if winners!=[]:
                prize=self.prize/len(winners)
            else:
                prize=0
            print "winnerpointdistributan",winners
            for winner in winners:
                print winner
                if winner in self.userScores.keys():
                    self.userScores[winner]+=prize
                    settingsHandler.updateSetting("chohan","points",self.userScores[winner],"nick='"+winner+"'")
                else:
                    self.userScores[winner]=prize
                    print "settanwritan"
                    settingsHandler.writeSetting("chohan", ["nick", "points"], [winner,str(prize)])
                    print "settanwrittan"
            print "dbhandlan"
            if len(winners)>1:
                winners=', '.join(winners[:-1])+" and "+winners[-1]
                winString=["winners are "," each"]
            elif len(winners)==1:
                winners=winners[0]
                winString=["winner is ",""]
            else:
                winners=""
                winString=["",""]
            if winners!="":
                msg+=["PRIVMSG $C$ :The "+winString[0]+winners+", and they"+winString[1]+" win "+str(prize)+" points"]
            else:
                msg+=["PRIVMSG $C$ :Nobody wins!"]
            self.total=0
            self.userGuesses={}
            return msg
        elif msg[0].lower()=="points":
            if len(msg)==1:
                return ["PRIVMSG $C$ :You have "+str(self.userScores[nick])+" points"]
            else:
                nick=msg[1]
                if nick in self.userScores.keys():
                    return ["PRIVMSG $C$ :"+nick+" has "+str(self.userScores[nick])+" points"]
                else:
                    return ["PRIVMSG $C$ :"+nick+" has 0 points"]
        elif msg[0].lower()=="e-penis":
            if len(msg)==1:
                return ["PRIVMSG $C$ :8="+('='*(self.userScores[nick]/100))+'D']
            else:
                nick=msg[1]
                if nick in self.userScores.keys():
                    return ["PRIVMSG $C$ :8="+('='*(self.userScores[nick]/100))+'D']
                else:
                    return ["PRIVMSG $C$ :"+nick+" has 0 points"]
        elif msg[0].lower()=="scoreboard":
            num=3 if len(msg)==1 else int(msg[1])
            scoreNames=[]
            for name in self.userScores.keys():
                if self.userScores[name]>0:
                    scoreNames.append((self.userScores[name],name))
            scoreNames.sort(key=lambda scoreName:scoreName[0])
            scoreNames.reverse()
            msg="The top "+str(num)+" users are: "
            for i in range(min(num,len(scoreNames))):
                msg+=scoreNames[i][1]+" with "+str(scoreNames[i][0])+" points"
                if i!=min(num,len(scoreNames))-1:
                    msg+=", "
                else:
                    msg+="!"
        elif msg[0].lower()=="donate":
            name=msg[1]
            amount=int(msg[2])
            if complete.user() not in self.userScores.keys() or name not in self.userScores.keys():
                msg="At least ONE of you don't have any points at all! Play a game of chohan first"
            elif self.userScores[complete.user()]>=amount and amount>0:
                self.userScores[name]+=amount
                self.userScores[complete.user()]-=amount
                settingsHandler.updateSetting("chohan","points",self.userScores[name],"nick='"+name+"'")
                settingsHandler.updateSetting("chohan","points",self.userScores[complete.user()],"nick='"+complete.user()+"'")
                msg="Donated points to "+name+", oh generous one!"
            elif amount<0:
                msg="Nice try!"
            elif self.userScores[complete.user()]<amount:
                msg="You don't have that much to give!"

        return ["PRIVMSG $C$ :"+msg]
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !cho-han module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!cho-han [roll|reveal|points|guess] [odd|even]"]
