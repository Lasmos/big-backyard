import os
import enum
import random
import copy
import sys
#import array

#initialize gamewide variables
#read the instructions!
game_instructions = "Type 'c' to try catching the bug that's here.\n Type 'l' to look for a different bug.\nType 'i' to check your inventory.\nType 's' to sell your bugs to the shopkeeper.\nType 'e' to quit the game."

money = 0





#bug-related initializations

#bugs ever caught
caught_bugs_ever = []#number of bugs ever caught arranged by bug type and in the same order

#bugs currently held
held_bugs_now = []#number of bugs currently held arranged by bug type and in the same order

#player stats
player_stats = [1,1,1]#jumping, aiming, and bargaining

#count each bug instance
every_bug = 0#not currently used - is it needed?
every_bug_type = 0#used in giverandombug to tell how many bug types there are

#hold onto each bug type
every_bug_list = []

#enum for bug sizes
class Sizes (enum.Enum):
    TINIER = 1
    TINY = 2
    SMALL = 3


#create bugs class
class Bug ():
    "All the buzzing beasties, from the tiny to the ... less tiny."
    
    #every bug has these
    def __init__(self, number, word, word2, stringwords, intarray, enumsize):
        global every_bug_type
        global every_bug_list
        
        self.id = number
        self.name = word
        self.nameplural = word2
        self.description = stringwords
        self.stats = intarray #height, swiftness, irregularity, value
        self.size = enumsize
        every_bug_type += 1
        every_bug_list.append(self)
        caught_bugs_ever.append(0)
        held_bugs_now.append(0)
        

#create bugs
morpho = Bug(0, "Blue Morpho", "Blue Morphos", "A high-flying bright blue butterfly flits here.", [5,4,5,5], Sizes.SMALL)
painted = Bug(1, "Painted Lady", "Painted Ladies", "An orange butterfly with large black splotches has settled on a branch.", [2,2,2,2], Sizes.TINY)
monarch = Bug(2, "Monarch", "Monarchs", "A bright orange-and black butterfly dashes about.", [2,1,1,1], Sizes.TINY)

#bug-related methods
def tradeidforbug(bugid):
    for element in every_bug_list:
        if(element.id == bugid):
            return element

def giverandombug():
    return tradeidforbug(random.randint(0,(every_bug_type - 1)))










#shopkeeper-related initializations
#every shopkeeper
every_shopkeeper_list = []

#enum for shopkeeper pronouns
class Pronoun (enum.Enum):
    FEMININE = 1
    MASCULINE = 2
    PLURAL = 3


#create Shopkeepers class
class Shopkeeper ():
    "These people are SUPER interested in your bugs."
    
    #every shopkeeper has these
    def __init__(self, number, word, word2, apronoun, stringwords, stringwords2, stringwords3, intarray2):
        global every_shopkeeper_list
        
        self.id = number
        self.name = word
        self.title = word2
        self.pronoun = apronoun
        self.shopkeeperdescription = stringwords
        self.behavior = stringwords2
        self.shopdescription = stringwords3
        #self.deals = intarray how do I handle making deals?
        self.wishes = intarray2
        every_shopkeeper_list.append(self)

#create shopkeepers
vanessa = Shopkeeper(0, "Vanessa", "The Picky", Pronoun.FEMININE, "willowy blonde wearing lipstick, heels, and a large assortment of jewelry", "raises a perfectly-manicured brow at you and rests her elbows on the stainless-steel counter", "gigantic, bejeweled boudoir with display cases of shiny things everywhere", [5, 1, 5])
valerie = Shopkeeper(1, "Valerie", "The Newbie", Pronoun.FEMININE, "dark-haired oversized teenage girl with acne", "dashes up to the rickety wooden counter wheezing", "tiny shack with a counter out front", [2, 2, 5])
virgil = Shopkeeper(2, "Virgil", "The Edgelord", Pronoun.MASCULINE, "tall figure in a black cloak that hides their face in shadow", "looms menacingly over the black marble counter", "fabric-draped and incense-scented building lit dimly with candles", [2, 2, 2])


#shopkeeper-related methods
def tradeidforshopkeeper(shopkeeperid):
    for shopkeeper in every_shopkeeper_list:
        if(shopkeeper.id == shopkeeperid):
            return shopkeeper
    
def giverandomshopkeeper():
    return tradeidforshopkeeper(random.randint(1,len(every_shopkeeper_list)))

def showtheshop(shopkeeper):
    theperson = "he asks. "
    if(shopkeeper.pronoun == Pronoun.FEMININE):
        theperson = "she asks. "
    elif(shopkeeper.pronoun == Pronoun.PLURAL):
        theperson = "they ask. "
    
    telluser("The shop is a " + shopkeeper.shopdescription + ". ")
    telluser("A " + shopkeeper.shopkeeperdescription + " " + shopkeeper.behavior + ". ")
    telluser("'Do you want to sell?' " + theperson)

def givemoney(shopkeeper, currentbugs, allbugs):
    global money 
    
    moneycounter = 0
    for bugtype in allbugs:
        if(currentbugs[bugtype.id] > 0):
            moneycounter += (shopkeeper.wishes[bugtype.id - 1] * bugtype.stats[3])
    money += moneycounter
    return moneycounter





bug_directions = {
    "right": ["x", 1],
    "left": ["x", -1],
    "up": ["y", 1],
    "down": ["y", -1],
    "away": ["z", 1],
    "toward": ["z", -1],
}
world_directions = {
    "east": ["x", 1],
    "west": ["x", -1],
    "north": ["y", 1],
    "south": ["y", -1],
    "outside": ["z", 1],
    "inside": ["z", -1],
}


#general methods
def trytocatch(theBug):
    #if the player's aim is that good, 
    if(player_stats[1] > theBug.stats[0] * theBug.stats[1]):
        #they can probably catch the bug
        if(playerluck(75)):
            return iscaught(theBug)
        else:
            return notcaught()
    #if the player's jump is that good
    elif(player_stats[0] > theBug.stats[0]):
        #they can catch the bug if they're somewhat lucky
        if(playerluck(50)):
            return iscaught(theBug)
        else:
            return notcaught()
    elif(player_stats[1] > theBug.stats[1]):
        #they can catch the bug if they're pretty lucky
        if(playerluck(25)):
            return iscaught(theBug)
        else:
            return notcaught()
    else:
        #they might still be able to catch the bug
        if(playerluck(1 + (10 - theBug.stats[1]))):
            return iscaught(theBug)
        else:
            return notcaught()

    

#increment currently held and ever caught bugs of the current type
def iscaught(theBug):
    global held_bugs_now
    global caught_bugs_ever
    
    print("bug's ID# is " + str(theBug.id) + ".\n")
    
    telluser("You got it!")
    
    held_bugs_now[theBug.id] += 1
    caught_bugs_ever[theBug.id] += 1
    return True

def notcaught():
    lossmessage = "Better luck next time!"
    pickone = random.randint(1, 5)
    if(pickone == 1):
        lossmessage = "It's not over yet!"
    elif(pickone == 2):
        lossmessage = "Ah! I missed..."
    elif(pickone == 3):
        lossmessage = "Whoops, there it goes!"
    elif(pickone == 4):
        lossmessage = "Time to try again."
    telluser(lossmessage)
    return False


def playerluck(tobeat):
    #tobeat 75 = 3/4 chance to win
    #tobeat 50 = 1/2 chance to win
    #tobeat 25 = 1/4 chance to win
    #tobeat 10 = 1/10 chance to win
    #tobeat 1 = 1/100 chance to win
    if(random.randint(1,100) > tobeat):
        return True
    else:
        return False

def telluser(astring):
    print(astring)






#inventory methods
def addinventory(currentbugs):
    addingup = 0
    for eachbugtype in currentbugs:
        addingup += eachbugtype
    return addingup


def inventory(current, potential):#array of ints, array of bugs
    #what needs to be shown?
    #for now just tell the player what bugs they have
    checkingfornone = 0
    
    #for each bug type the player COULD have,
    for bugtype in potential:
        #if they DO have any
        if(current[bugtype.id] > 0):
            #tell them so
            telluser(bugtype.nameplural + ": " + str(current[bugtype.id]))
            #and add to checkingfornone so it won't be 0
            checkingfornone += 1
        #otherwise they don't have any so don't tell them about it
    
    #then check checkingfornone to see if it's empty
    if(checkingfornone == 0):
        telluser("You don't have any bugs. Such a sad empty inventory. Go catch some!")
    
    telluser("You have " + str(addinventory(current)) + " total bugs.")



    


#main gameplay

#tell user how to play
telluser(game_instructions)
#randomize the first bug to show
current_bug = giverandombug()

#randomize the game's shopkeeper
shopkeep = giverandomshopkeeper()

#main game loop
user_uses = True
while(user_uses):
    
    #tell user what they have right now
    if(addinventory(held_bugs_now) > 20):
        telluser("You have quite a few bugs right now!")
    elif(addinventory(held_bugs_now) > 50):
        telluser("Wow, you have SO MANY bugs!")
    
    #tell user what's here right now
    if(current_bug is None):
        telluser("\nThere is no bug here right now. Look for one!")
    else:
        telluser("\n" + current_bug.description)
    
    #ask for user action
    state = input("What will you do? ")
    
    #respond to user action
    #if user wants to try to catch the bug,
    if(state == 'c' or state == 'C'):
        #if there is a bug present,
        if(current_bug):
            #try to catch the bug; 
            if(trytocatch(current_bug)):
                #if you succeeded, no bug is currently present
                current_bug = None
                #otherwise the bug that was already here is still here
        #otherwise tell the user to look for another bug
        else:
            telluser("No bugs here; press 'l' to look for another.")
    
    #if the user wants to look for a new bug,
    elif(state == 'l' or state == 'L'):
        #look for a new bug
        current_bug = giverandombug()
    
    #if the user wants to leave the game,
    elif(state == 'e' or state == 'E'):
        #shut down while loop
        user_uses = False
    
    #if the user wants to check their inventory,
    elif(state == 'i' or state == 'I'):
        #list the bugs they currently have
        inventory(held_bugs_now, every_bug_list)
    
    #if the user wants to sell their stock,
    elif(state == 's' or state == 'S'):
        #describe the shop and shopkeeper
        showtheshop(shopkeep)
        #ask for user's decision
        innerstate = input("\nType 'y' for yes or 'n' for no.")
        #wait for user's decision
        willusersell = True
        while(willusersell):
            #if the user decides to sell,
            if(innerstate == 'y' or innerstate == 'Y'):
                #check if user actually has any bugs
                if(addinventory(held_bugs_now) == 0):
                    telluser("'What, you don't have any? Shoo. Come back when you have bugs to sell.'")
                    willusersell = False
                else:
                    #acknowledge the decision,
                    telluser("'Great! Here's your money.'")
                    #give them money for their bugs,
                    newmoney = givemoney(shopkeep, held_bugs_now, every_bug_list)
                    #tell them how much they got,
                    telluser("\nYou got " + str(newmoney) + " pennies!")
                    telluser("You now have " + str(money) + " pennies.")
                    #erase all bugs from the user's inventory,
                    for eachbug in every_bug_list:
                        held_bugs_now[eachbug.id] = 0
                    print("You now have these bugs: " + str(held_bugs_now))
                    #then end selling loop.
                    willusersell = False
            #if the user doesn't want to sell,
            elif(innerstate == 'n' or innerstate == 'N'):
                #acknowledge the decision,
                telluser("'Too bad. Another time, then.'")
                #then end selling loop.
                willusersell = False
            #if the user wants to exit the game,
            elif(innerstate == 'e' or innerstate == 'E'):
                #give exit message,
                telluser("Okay. Goodbye, then.")
                #then close the program.
                sys.exit()
            else:
                telluser("'Do you want to sell or not? I don't have time for this.'")
                #don't end selling loop until they make a decision.
    
    #if the user inputs anything else,
    else:
        #tell them to pay attention this time
        telluser("I don't understand what you want.\n")
        telluser(game_instructions)








"""
plans and stuff:
-make bugs dodging you more interesting - /why/ did it escape?
-give a you-caught-the-bug message
-what does your inventory look like? it's a pouch of some sort. maybe make it upgradeable so you can only put a few bugs in it at first. that limits your exploration time by your caught bugs at first or you have to leave bugs behind.
-player stats: jumping, aiming, and bargaining
    jumping makes you able to catch bugs that fly too high
    aiming makes the chance of missing lower
    bargaining gives you a better chance of good deals from shopkeepers
   add a stealth stat?
-bug stats: height, swiftness, irregularity, value
    height makes them able to avoid you by going up
    swiftness makes them generally harder to catch
    irregularity makes them more difficult to predict
    value makes them worth more

-a boolean array for key items, you have it or you don't; the encyclopedia, types and levels of equipment?
-make a bug encyclopedia - what bugs have you caught before? how do you identify what bugs you have?
-make bug size matter - different nets are required to catch the smallest bugs and the larger bugs, and the largest ones need a different item entirely
-how to place the shopkeepers? for now just randomize which one you're working with for the whole game
-make bug catching directional?
-make selling bugs more choosy - what if you don't want to sell them all?
-make different spaces with different bugs
-make a 'home base'?
-make a training space, or just train stats with use? both?
-what types of items would make things easier to do? net types for bug sizes
-make a save system and ability to have different games going at one time
-make lots more bugs
-make bugs run away at some point? after a certain number of attempts?
-WHERE IS GRANDPA
-what is the central struggle for this game? the main thing is to collect them all and get lots of money... but why? maybe your complete bug collection can get some money for Grandpa to help with his money problems. no, not the complete collection but one specific bug - diamond bug, or something. it's in a far away place that we have to figure out how to get to and specialized equipment to catch.
-give shopkeepers their own yes/no/thank-you-come-again responses
-maybe the shopkeepers can reference how odd it is that they're here paying so much money for bugs? lampshade
-make later areas' bugs move but first area bugs stay still to get you used to catching them

"""
