
from plugins import plugin
import globalv
import random
class pluginClass(plugin):
    def __init__(self):
        self.battleOver = False;
        self.battleTurn = 0;
        self.battleP1 = "Player1";
        self.battleP2 = "Player2";
        self.battleP1HP = random.randrange(60,100);
        self.battleP2HP = random.randrange(60,100);
        self.battleP1MP = random.randrange(10,40);
        self.battleP2MP = random.randrange(10,40);
        self.battleP1ATK = random.randrange(10,20);
        self.battleP2ATK = random.randrange(10,20);
        self.battleP1DEF = random.randrange(5,10);
        self.battleP2DEF = random.randrange(5,10);
        self.battleP1SPD = random.randrange(10,30);
        self.battleP2SPD = random.randrange(10,30);

        self.battleSpell1Name = "Cure";
        self.battleSpell1MP = 5;
        self.battleSpell1Effect = 1;
        # 0 = attack, 1 = heal, 2 = buff attack, 3 = buff defense
        self.battleSpell1Value = 25;

        self.battleSpell2Name = "Fire";
        self.battleSpell2MP = 5;
        self.battleSpell2Effect = 0;
        self.battleSpell2Value = random.randrange(30,40);

        if self.battleP1SPD >= self.battleP2SPD:
            self.battleTurn = 0;
        else :
            self.battleTurn = 1;

        self.lastCommand = "nothing";
        
    def gettype(self):
        return "command"
    def action(self, complete):
        msg=complete.message()

        if msg == "reset":
            self.__init__();
            return ["PRIVMSG $C$ :"+"!battle reset by $U$"]
        
        if msg == "name1":
            self.lastCommand = "name1";
            return ["PRIVMSG $C$ :"+"Name Player 1:"]
        
        if self.lastCommand == "name1":
            self.battleP1 = msg;
            self.lastCommand = "nothing";
            return ["PRIVMSG $C$ :"+"Player 1 is now known as "+self.battleP1]
        
        if msg == "name2":
            self.lastCommand = "name2";
            return ["PRIVMSG $C$ :"+"Name Player 2:"]

        if self.lastCommand == "name2":
            self.battleP2 = msg;
            self.lastCommand = "nothing";
            return ["PRIVMSG $C$ :"+"Player 2 is now known as "+self.battleP2]

        if msg == "stats1":
            return ["PRIVMSG $U$ : Player 1 stats:","PRIVMSG $U$ : HP: "+str(self.battleP1HP),"PRIVMSG $U$ : MP: "+str(self.battleP1MP),"PRIVMSG $U$ : ATK: "+str(self.battleP1ATK), "PRIVMSG $U$ : DEF: "+str(self.battleP1DEF),"PRIVMSG $U$ : SPD: "+str(self.battleP1SPD)] 

        if msg == "stats2":
            return ["PRIVMSG $U$ : Player 2 stats:","PRIVMSG $U$ : HP: "+str(self.battleP2HP),"PRIVMSG $U$ : MP: "+str(self.battleP2MP),"PRIVMSG $U$ : ATK: "+str(self.battleP2ATK), "PRIVMSG $U$ : DEF: "+str(self.battleP2DEF),"PRIVMSG $U$ : SPD: "+str(self.battleP2SPD)] 

        if msg == "turn":
            if self.battleTurn == 0:
                return ["PRIVMSG $C$ : It is "+self.battleP1+"'s turn..."]
            else :
                return ["PRIVMSG $C$ : It is "+self.battleP2+"'s turn..."]

        if msg == "fight":
            self.finalMsg = "";
            self.damageDone = 0;

            if self.battleP1HP <= 0 :
                self.battleTurn = 2;
                self.XP = self.battleP1DEF*self.battleP1ATK;
                self.GP = self.battleP1DEF+self.battleP1ATK;
                return ["PRIVMSG $C$ : "+self.battleP2+" won the battle!", "PRIVMSG $C$ : "+self.battleP2+" gets "+str(self.XP)+" XP and "+str(self.GP)+" GP!"]

            if self.battleP2HP <= 0 :
                self.battleTurn = 2;
                self.XP = self.battleP2DEF*self.battleP2ATK;
                self.GP = self.battleP2DEF+self.battleP2ATK;
                return ["PRIVMSG $C$ : "+self.battleP1+" won the battle!", "PRIVMSG $C$ : "+self.battleP1+" gets "+str(self.XP)+" XP and "+str(self.GP)+" GP!"]

            if self.battleTurn == 2:
                return ["PRIVMSG $C$: The battle has ended. Please reset the battle by using !battle reset"]
            
            if self.battleTurn == 0  and self.battleP2HP > 0:
                self.damageDone = self.battleP1ATK - self.battleP2DEF + random.randrange(0,self.battleP1ATK);
                self.battleP2HP -= self.damageDone;
                if self.battleP2HP <= 0: self.battleP2HP = 0;
                self.battleTurn = 1;
                return ["PRIVMSG $C$ : "+self.battleP1+" "+random.choice(["whacks","slices","smashes","slices","jabs","attacks"])+" "+self.battleP2+" with his weapon!","PRIVMSG $C$ : "+self.battleP2+" loses "+str(self.damageDone)+"HP!", "PRIVMSG $C$ : "+self.battleP1+" has "+str(self.battleP1HP)+" HP left.","PRIVMSG $C$ : "+self.battleP2+" has "+str(self.battleP2HP)+" HP left."];
            
            if self.battleTurn == 1 and self.battleP2HP > 0:
                self.damageDone = self.battleP2ATK - self.battleP1DEF + random.randrange(0,self.battleP2ATK);
                self.battleP1HP -= self.damageDone;
                if self.battleP1HP <= 0: self.battleP1HP = 0;
                self.battleTurn = 0;
                return ["PRIVMSG $C$ : "+self.battleP2+" "+random.choice(["whacks","slices","smashes","slices","jabs","attacks"])+" "+self.battleP1+" with his weapon!","PRIVMSG $C$ : "+self.battleP1+" loses "+str(self.damageDone)+"HP!", "PRIVMSG $C$ : "+self.battleP1+" has "+str(self.battleP1HP)+" HP left.","PRIVMSG $C$ : "+self.battleP2+" has "+str(self.battleP2HP)+" HP left."];

            
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !battle module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!battle reset|name1|name2|stats1|stats2|fight|spell1|spell2|status|spellList"]
