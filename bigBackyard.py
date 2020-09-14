import os
import enum
import random

#initialize gamewide variables
#read the instructions!
game_instructions = "Type 'c' to try catching the bug that's here.\n Type 'l' to look for a different bug.\nType 'e' to quit the game."

#bugs ever caught
caught_bugs_ever = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]#11

#bugs currently held
held_bugs_now = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]#11

#player stats
player_stats = [1,1,1]#jumping, aiming, and bargaining - add spotting?

#count each bug instance
every_bug = 0
every_bug_type = 0

#hold onto each bug type
every_bug_list = []




#initialize game classes
#create an enum for bug sizes
class Sizes (enum.Enum):
    TINIER = 1
    TINY = 2
    SMALL = 3




#create bugs class
class Bug ():
    "All the buzzing beasties, from the tiny to the ... less tiny."
    
    #every bug has these
    def __init__(self, number, word, stringwords, intarray, enumsize):
        global every_bug_type
        global every_bug_list
        
        self.id = number
        self.name = word
        self.description = stringwords
        self.stats = intarray #height, swiftness, value
        self.size = enumsize
        every_bug_type += 1
        every_bug_list.append(self)
        

#create bugs
morpho = Bug(1, "Blue Morpho", "A high-flying bright blue butterfly flits here.", [5,4,5], Sizes.SMALL)
painted = Bug(2, "Painted Lady", "An orange butterfly with large black splotches has settled on a branch.", [2,2,2], Sizes.TINY)
monarch = Bug(3, "Monarch", "A bright orange-and black butterfly dashes about.", [2,1,1], Sizes.TINY)

#bug-related methods
def tradeidforbug(bugid):
    for element in every_bug_list:
        if(element.id == bugid):
            return element
    return monarch

def giverandombug():
    return tradeidforbug(random.randint(1,every_bug_type))







#general methods
def trytocatch(theBug):
    #if the player's aim is that good, 
    if(player_stats[1] > theBug.stats[0] * theBug.stats[1]):
        #they can probably catch the bug
        if(playerluck(75)):
            iscaught(theBug)
        else:
            notcaught()
    #if the player's jump is that good
    elif(player_stats[0] > theBug.stats[0]):
        #they can catch the bug if they're somewhat lucky
        if(playerluck(50)):
            iscaught(theBug)
        else:
            notcaught()
    elif(player_stats[1] > theBug.stats[1]):
        #they can catch the bug if they're pretty lucky
        if(playerluck(25)):
            iscaught(theBug)
        else:
            notcaught()
    else:
        #they might still be able to catch the bug
        if(playerluck(1 + (10 - theBug.stats[1]))):
            iscaught(theBug)
        else:
            notcaught()

    

#increment currently held and ever caught bugs of the current type
def iscaught(theBug):
    global held_bugs_now
    global caught_bugs_ever
    
    held_bugs_now[theBug.id] += 1
    caught_bugs_ever[theBug.id] += 1

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


def addinventory():
    addingup = 0
    for eachbugtype in held_bugs_now:
        addingup += eachbugtype
    return addingup



#main gameplay

#tell user how to play
telluser(game_instructions)

#main game loop
user_uses = True
while(user_uses): 
    #randomize and store the bug currently 'on-screen'
    current_bug = giverandombug()
    
    #tell user what they have right now
    telluser("You currently have " + str(addinventory()) + " bugs with you.")
    
    #tell user what's here right now
    telluser("\n" + current_bug.description)
    
    #ask for user action
    state = input("What will you do? ")
    
    #respond to user action
    #if user wants to try to catch the bug,
    if(state == 'c' or state == 'C'):
        #try to catch the bug
        trytocatch(current_bug)
    #if the user wants to look for a new bug,
    elif(state == 'l' or state == 'L'):
        #look for a new bug
        current_bug = giverandombug()
    #if the user wants to leave the game,
    elif(state == 'e' or state == 'E'):
        #shut down while loop
        user_uses = False
    #if the user inputs anything else,
    else:
        #tell them to pay attention this time
        telluser("What is it you're trying to do? ")
        telluser(game_instructions)










"""
plans and stuff:
-make bugs dodging you more interesting - /why/ did it escape?
-give a you-caught-the-bug message
-what does your inventory look like?

-make a bug encyclopedia - what bugs have you caught before? how do you identify what bugs you have?
-make bug size matter
-make shopkeepers to sell bugs to
-make different spaces with different bugs
-make a 'home base'?
-make a training space, or just train stats with use? both?
-what types of items would make things easier to do?
-make a save system and ability to have different games going at one time
-make lots more bugs
-WHERE IS GRANDPA
-what is the central struggle for this game? the main thing is to collect them all and get lots of money... but why?

"""