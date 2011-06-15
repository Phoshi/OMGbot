# -*- coding: utf-8 -*-
from plugins import plugin
import settingsHandler
import globalv
import random
class crab(object):
    def __init__(self,user, name, XP, level, abilities,abilityList):
        print "This is even running"
        base=5
        self.user=user
        self.name=name
        self.XP=XP
        self.level=level
        self.abilities=abilities
        self.abilityList=abilityList
        self.attack=base+(base*0.02*self.level)
        self.defence=base+(base*0.015*self.level)
        self.agility=base+(base*0.01*self.level)
        self.enemyAttack=100 #% that gets to you, applied before defence
        self.enemyAgility=100
        self.XPModifier=100#% of XP you get
        self.hp=2*base+(base*level*0.05)
        self.maxhp=self.hp
        self.critMultiplier=1
        self.HPRegen=0
        self.numAbilities=0
        self.savevsdeath=0#chance to save vs death
        self.ondefend=[]
        self.onattack=[]
        self.ondeath=[]
        self.onsave=[]
        for ability in range(len(self.abilities)):
            if self.abilities[ability]=="1":
                self.numAbilities+=1
                self.addAbility(ability)
        if self.level>100:
            self.level=100
    def addAbility(self, ability):
        print "Adding ability",ability
        effects=self.abilityList[ability][2]
        effects=effects.split('|')
        for effect in effects:
            stat=effect.split()[1]
            amount=int(effect.split()[0])
            if stat=="attack":
                self.attack*=1+amount/100.0
            elif stat=="defence":
                self.defence*=1+amount/100.0
            elif stat=="agility":
                self.agility*=1+amount/100.0
            elif stat=="hp":
                self.hp*=1+amount/100.0
                self.maxhp=self.hp
            elif stat=="xp":
                self.XPModifier+=amount
            elif stat=="regen":
                self.HPRegen+=amount
            elif stat=="save":
                self.savevsdeath+=amount
            elif stat=="enemyattack":
                self.enemyAttack+=amount
            elif stat=="crit":
                self.critMultiplier*=1+amount/100.0
            elif stat=="enemyagility":
                self.enemyAgility+=amount
            elif stat=="deathchance":
                self.ondeath.append(ability)
            elif stat=="savechance":
                self.onsave.append(ability)
            elif stat=="chance":
                self.onattack.append(ability)
            elif stat=="defencechance":
                self.ondefend.append(ability)
    def getAttackString(self, crab):
        attacks=[]
        attacks.append("strikes")
        attacks.append("slices")
        attacks.append("cuts")
        attacks.append("stabs")
        if self.abilities[2]=="1":
            attacks.append("slices through %s"%crab.name)
        if self.abilities[3]=="1":
            attacks.append("smashes")
        if self.abilities[5]=="1":
            attacks.append("makes an FTL jump off of %s"%crab.name)
        if self.abilities[6]=="1":
            attacks.append("precisely strikes")
        if self.abilities[8]=="1":
            attacks.append("triple-cuts")
        if self.abilities[9]=="1":
            attacks.append("telekinetically throws %s into the ground"%crab.name)
        if self.abilities[11]=="1":
            attacks.append("uses the vulcan death claw")
        if self.abilities[12]=="1":
            attacks.append("jump kicks")
            attacks.append("flying kicks")
            attacks.append("spinning kicks")
        if self.abilities[13]=="1":
            attacks.append("blasts")
            attacks.append("counterattacks with defence lasers")
        if self.abilities[18]=="1":
            attacks.append("smites")
        if self.abilities[20]=="1":
            attacks.append("blasts %s with lasers"%crab.name)
            attacks.append("carves through %s with a high powered laser"%crab.name)
        if self.abilities[22]=="1":
            attacks.append("throws")
            attacks.append("smashes")
            attacks.append("kicks")
        if self.abilities[27]=="1":
            attacks.append("cuts")
            attacks.append("harnesses the power of an ancient god")
            attacks.append("calls upon eternity")
        if self.abilities[31]=="1":
            attacks.append("shoots a missile at %s because that is his weakness"%crab.name)
            attacks.append("launches a missile")
        if self.abilities[32]=="1":
            attacks.append("makes a damn good hit")
        if self.abilities[33]=="1":
            attacks.append("emits an aura of badassery")
        random.shuffle(attacks)
        return attacks[0]
    def attackCrab(self,crab):
        criticalString=""
        enemyDefence=crab.defence
        enemyAgility=crab.agility*(self.enemyAgility/100.0)
        attack=self.attack*(crab.enemyAttack/100.0)
        agility=self.agility*(crab.enemyAgility/100.0)
        miss=random.randint(1,int(enemyAgility*1.5))>agility
        if miss:
            return "%s %s, but misses!"%(self.name,self.getAttackString(crab))
        print self.onattack
        for ability in self.onattack:
            print "Checking onattack ability",ability
            if ability==21 and random.randint(0,100)<5:
                attack+=2
                attack*=3
                criticalString+="%s calls in an orbital strike! "%self.name
            elif ability==29 and random.randint(0,100)<5:
                attack*=5
                criticalString="%s uses hyper beam! "%self.name
            elif ability==19 and random.randint(0,int(self.maxhp))>self.hp:
                attack*=1.5
                self.HPRegen+=1
                criticalString+="%s activates their devil trigger! "%self.name
        damage=random.randint(1,int(attack*100))
        damage/=100
        critical=random.randint(-100,100)*self.critMultiplier
        if critical>=90:
            damage+=2
            damage*=2
            criticalString+="Critical Hit! "
        elif critical<=-90:
            damage/=4
            criticalString+="Critical Failure! "
        damage*=1-(enemyDefence/50.0)
        damage=int(damage)
        crab.hp-=damage
        self.hp+=self.HPRegen
        return "%s%s %s for %s damage!"%(criticalString, self.name, self.getAttackString(crab), damage)
    def isDead(self, crab):
        if self.hp>0:
            return (False,"")
        elif random.randint(0,100)<self.savevsdeath:
            for ability in self.onsave:
                if ability==23:
                    if random.randint(0,100)<=10:
                        crab.hp=0
                        return (False, "%s, in a last chance strike, kills %s in one clean hit!"%(self.name,crab.name))
            return (False, "%s should be dead, but just keeps on going!")
        else:
            return (True, "")
    def awardXP(self, XP):
        self.XP+=XP*(self.XPModifier/100.0)
        levelledup=0
        while self.XP>((self.level+1)*self.level*100) and self.level<100:
            self.level+=1
            levelledup=1
        if levelledup:
            return self.level
        else:
            return False
    def awardAbility(self, ability):
        self.abilities=self.abilities[:ability]+"1"+self.abilities[ability+1:]
    def removeAbility(self, ability):
        self.abilities=self.abilities[:ability]+"0"+self.abilities[ability+1:]
    def save(self,table):
        settingsHandler.executeQuery("UPDATE %s SET name='%s', XP=%s, level=%s, abilities='%s' WHERE user='%s'"%(table, self.name, self.XP, self.level, self.abilities,self.user))



class pluginClass(plugin):
    def addAbility(self, name, effects):
        self.abilities.append((len(self.abilities), name, effects))
    def gettype(self):
        return "command"
    def __init_db_tables__(self, name):
        settingsHandler.newTable(name, "user","name","XP","level", "Abilities")
    def __init__(self):
        self.abilities=[]
        self.addAbility("Adamantium Shell","25 defence")
        self.addAbility("Accelerated Reflexes","5 agility")
        self.addAbility("Monomolecular Claw","15 attack")
        self.addAbility("Rocket Claw","5 attack|5 agilty")
        self.addAbility("Energy Shielding","25 defence")
        self.addAbility("Jump Drive","5 agility")
        self.addAbility("Assisted Aim","-10 enemyattack")
        self.addAbility("Cybernetic Enhancements","5 attack|5 defence|5 agility|5 hp")
        self.addAbility("Tri-Blade Claw","15 attack")
        self.addAbility("Telekenetic Flight","15 agility")
        self.addAbility("Slow-Motion Replay","10 xp")
        self.addAbility("Vulcan Death Claw","15 attack")
        self.addAbility("Kung-Fu", "5 attack|10 defence")
        self.addAbility("Secondary Lasers", "25 defence")
        self.addAbility("Temporal Replay","-20 enemyagility")
        self.addAbility("Omniprescence","-20 enemyagility")
        self.addAbility("Healing Touch","10 hp|1 regen")
        self.addAbility("Faith","5 save")
        self.addAbility("Smite","1 chance")
        self.addAbility("Devil Trigger","1 chance")
        self.addAbility("Primary Lasers","15 attack")
        self.addAbility("Orbital Strike","1 chance")
        self.addAbility("Micro Mecha", "15 attack | 10 defence")
        self.addAbility("Last Stand", "1 savechance")
        self.addAbility("Intense Training", "15 attack | 10 defence")
        self.addAbility("Punch Out Cthulhu", "5 save")
        self.addAbility("Nuclear Powered", "1 deathchance")
        self.addAbility("Infinity +1 Sword", "15 attack")
        self.addAbility("Cat-Like Reflexes", "15 agility")
        self.addAbility("Hyper Beam", "1 chance")
        self.addAbility("Lucky Shot", "25 crit")
        self.addAbility("Missile Launcher", "10 attack|10 crit")
        self.addAbility("Improbable Aim", "25 crit")
        self.addAbility("Badass Longcoat", "25 defence")

    def getCrabFromDatabase(self, table, user):
        try:
            data=settingsHandler.executeQuery("SELECT name, XP, level, abilities FROM %s WHERE user='%s'"%(table,user))
            data=data[0]
            newCrab=crab(user, data[0][:50], data[1], data[2], data[3].rjust(len(self.abilities),"0"), self.abilities)
            return newCrab
        except Exception as detail:
            print detail
            return False

    def action(self, complete):
        msg=complete.message()
        global crab
        if msg.split()[0]=="battle" or msg.split()[0]=="blowbyblow":
            events=[]
            if len(msg.split())==1:
                oneCrab=self.getCrabFromDatabase(complete.cmd()[0],complete.user())
                newLevel=oneCrab.level+int(random.gauss(0,4))
                if newLevel<=0:
                    newLevel=1
                if newLevel>100:
                    newLevel=100
                nameList=["Giant Enemy Crab", "Enemy Crab", "The Lord Of The Moon Seas", "God", "Hyper Crab", "Devil Crab", "Generic Enemy Crab", "Generic Angsty Teenage Crab","Hitler"]
                random.shuffle(nameList)
                newName=nameList[0]
                abilityString="1"*(1+int(newLevel/5))
                abilityString=abilityString.rjust(len(self.abilities), "0")
                abilityString=list(abilityString)
                random.shuffle(abilityString)
                abilityString=''.join(abilityString)
                twoCrab=crab("-WorldSpace-", newName, oneCrab.XP, newLevel, abilityString, self.abilities)
                events.append("PRIVMSG $C$ :%s has come across the level %s %s!"%(oneCrab.name, twoCrab.level, twoCrab.name))
            else:
                oneCrab=self.getCrabFromDatabase(complete.cmd()[0],complete.user())
                twoCrab=self.getCrabFromDatabase(complete.cmd()[0],msg.split()[1])
            if oneCrab==False:
                return ["PRIVMSG $C$ :You don't have a crab! Run !crab init [crab name] to get one!"]
            elif twoCrab==False:
                print "it's this"
                return ["PRIVMSG $C$ :%s doesn't have a crab! They can run !crab init [crab name] to get one!"%msg.split()[1]]
            turn=0
            battleWon=False
            if oneCrab.level < twoCrab.level-5:
                events.append("PRIVMSG $C$ :%s gets an underdog bonus! Attack and Defence improved 20%%!"%oneCrab.name)
                oneCrab.attack*=1.2
                oneCrab.defence*=1.2
            if twoCrab.level < oneCrab.level-5:
                events.append("PRIVMSG $C$ :%s gets a jerk penalty! Attack and Defence drop 25%%!"%oneCrab.name)
                oneCrab.attack*=0.75
                oneCrab.defence*=0.75
            for i in range(30):
                if turn==0:
                    events.append("PRIVMSG $C$ :"+oneCrab.attackCrab(twoCrab))
                else:
                    events[-1]+="; "+twoCrab.attackCrab(oneCrab)
                oneIsDead=oneCrab.isDead(twoCrab)
                twoIsDead=twoCrab.isDead(oneCrab)
                if oneIsDead[0]:
                    winner=twoCrab
                    loser=oneCrab
                    battleWon=True
                    if oneIsDead[1]!="":
                        events.append("PRIVMSG $C$ :%s"%oneIsDead[1])
                elif twoIsDead[0]:
                    winner=oneCrab
                    loser=twoCrab
                    battleWon=True
                    if twoIsDead[1]!="":
                        events.append("PRIVMSG $C$ :%s"%twoIsDead[1])
                if battleWon:
                    break
                else:
                    turn=(1 if turn==0 else 0)
            if msg.split()[0]=="battle":
                events=[]
            if battleWon:
                winnerXP=((loser.level+1)*(loser.level)*10)/((winner.level/5)+1)
                if loser.user!=winner.user:
                    if winner.user!="-WorldSpace-":
                        levelUp=winner.awardXP(winnerXP)
                    else:
                        levelUp=False
                    events.append("PRIVMSG $C$ :%s won the battle, and is awarded %s XP!"%(winner.name, winnerXP))
                else:
                    levelUp=False
                    events.append("PRIVMSG $C$ :%s won the battle, but gets no XP from fighting themself!"%(winner.name,))
                if levelUp!=False:
                    events.append("PRIVMSG $C$ :%s levelled up! %s is now level %s!"%(winner.name, winner.name, levelUp))
                if int(levelUp/5)>winner.numAbilities-1:
                    events.append("PRIVMSG $C$ :%s can now choose %s more abilities!"%(winner.name,1+int(levelUp/5)-winner.numAbilities))
                if winner.user!="-WorldSpace-":
                    winner.save(complete.cmd()[0])
            else:
                events.append("PRIVMSG $C$ :Both crabs retreat to recover. There is no winner!")
            return events
        elif msg.split()[0]=="init":
            if len(msg.split())==1:
                return ["PRIVMSG $C$ :You need to give your new crab a name!"]
            name=' '.join(msg.split()[1:])
            settingsHandler.executeQuery("INSERT INTO %s VALUES ('%s','%s',0,1,'%s')"%(complete.cmd()[0],complete.user(), name, "0"*len(self.abilities)))
            return ["PRIVMSG $C$ :%s successfully initialised! Type !crab list abilities to see all abilities, and !crab choose ability [name] to choose one!"%name]
        elif msg.split()[0]=="rename":
            newCrab=self.getCrabFromDatabase(complete.cmd()[0], complete.user())
            newCrab.name=' '.join(msg.split()[1:])
            newCrab.save(complete.cmd()[0])
        elif msg.split()[0]=="stats" or msg.split()[0]=="info":
            returnString=[]
            if len(msg.split())==1:
                user=complete.user()
            else:
                user=msg.split()[1]
            newCrab=self.getCrabFromDatabase(complete.cmd()[0], user)
            if newCrab==False:
                return ["PRIVMSG $C$ :%s doesn't have a crab! Run !crab init [crab name] to get one"%user]
            returnString.append("PRIVMSG $C$ :%s's stats: %s HP, %s XP, Level %s, %s attack, %s defence, %s agility, %s%% crit rate. %s has %s free ability slot(s)."%(newCrab.name, newCrab.hp, newCrab.XP, newCrab.level, newCrab.attack, newCrab.defence, newCrab.agility,newCrab.critMultiplier*10,newCrab.name,1+int(newCrab.level/5)-newCrab.numAbilities))
            ret=[]
            for ability in range(len(newCrab.abilities)):
                if newCrab.abilities[ability]=="1":
                    for abilitylist in self.abilities:
                        if abilitylist[0]==ability:
                            ret.append(abilitylist[1])
            returnString.append("PRIVMSG $C$ :Abilities are: "+', '.join(ret))
            return returnString
        elif msg.split()[0]=="list":
            if msg.split()[1]=="abilities":
                returnString=", ".join([ability[1] for ability in self.abilities])
                return ["PRIVMSG $C$ :"+returnString]
        elif msg.split()[0:2]==["choose","ability"]:
            targetAbility=' '.join(msg.split()[2:])
            newCrab=self.getCrabFromDatabase(complete.cmd()[0], complete.user())
            if int(newCrab.level/5)<=newCrab.numAbilities-1:
                return ["PRIVMSG $C$ :%s has no free ability slots!"%newCrab.name]
            ID=-1
            for ability in self.abilities:
                if ability[1].lower()==targetAbility.lower():
                    abilityName=ability[1]
                    ID=ability[0]
            if ID!=-1:
                newCrab.awardAbility(ID)
                newCrab.save(complete.cmd()[0])
                return ["PRIVMSG $C$ :Awarded %s the ability '%s'"%(newCrab.name, abilityName)]
            else:
                return ["PRIVMSG $C$ :There is no ability by that name!"]
        elif msg.split()[0:2]==["remove","ability"]:
            targetAbility=' '.join(msg.split()[2:])
            newCrab=self.getCrabFromDatabase(complete.cmd()[0], complete.user())
            for ability in self.abilities:
                if ability[1].lower()==targetAbility.lower():
                    abilityName=ability[1]
                    ID=ability[0]
            if newCrab.abilities[ID]=="0":
                return ["PRIVMSG $C$ :%s does not have that ability!"%newCrab.name]
            else:
                newCrab.removeAbility(ID)
                newCrab.save(complete.cmd()[0])
                return ["PRIVMSG $C$ :Removed that ability"]
        elif msg.split()[0]=="resetAbilities":
            newCrab=self.getCrabFromDatabase(complete.cmd()[0], complete.user())
            newCrab.abilities="0"*len(self.abilities)
            newCrab.save(complete.cmd()[0])
    def describe(self, complete):
        return ["PRIVMSG $C$ :I am the !say module","PRIVMSG $C$ :Usage:","PRIVMSG $C$ :!say [input]"]
