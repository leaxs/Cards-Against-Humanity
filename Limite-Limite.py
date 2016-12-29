from tkinter import *
from tkinter.messagebox import *
from tkinter.simpledialog import *
import codecs
import random as rd
import os 

##Start screen
#Add player to the party
class addingPlayer:
    def __init__(self,players_list):
        self.players_list = players_list
    def __call__(self):
        name = askstring("Adding player","Player name?")
        (self.players_list).insert(END,name)
        
#Remove the selected player in listbox
class removingPlayer:
    def __init__(self,players_list):
        self.players_list = players_list
    def __call__(self):
        if(askokcancel("Removing player", "Would you really remove "+(self.players_list).get(ACTIVE)+" from the party?")):
            (self.players_list).delete(ACTIVE)
            
#Start button manager
class StartGame:
    def __init__(self,detectedDeck,players):
        self.players_list = players
        self.carddeck = detectedDeck
    def __call__(self):
        #Check if there is enought players (minimum is 3)
        players = (self.players_list).get(0,END)
        if(len(players)<=2):
            showerror("","Not enought player!")
            return
            
        #Getting black and white cards
        white_cards = []
        black_cards = []
        for i in self.carddeck:
            isBlackcard = True
            if(i[1].get()):
                f = codecs.open("Carddeck/"+i[0], encoding='utf-8')
                for line in f:
                    if("\end"in line):
                        isBlackcard = False
                        continue
                    if(isBlackcard):
                        black_cards.append(line[:-2])
                    else:
                        white_cards.append(line[:-2])
                f.close()
                
        #Check if there is at least one black and one white cards
        if(len(black_cards) == 0 or len(white_cards)==0):
            showerror("","You should select decks to have both blacks and whites cards!")
            return
        
        #Lauch the game
        mainGameLoop(players,white_cards,black_cards)
        
#Research all files in carddeck directory and return their name
def getCardInDirectory(carddeck,panel):
    card_dir = os.listdir('Carddeck') 
    for i in card_dir:
        var = BooleanVar()
        checkbox = Checkbutton(panel,variable=var,text=i,onvalue=True, offvalue=False)
        checkbox.pack()
        carddeck.append((i,var))

#Title screen that allows to choose used deck and add/remove player
def startScreen():
    #Deck management
    available_deck_panel = LabelFrame(root, text="Choose your deck")
    available_deck_panel.pack(fill="both", expand="yes")
    
    carddeck = []
    getCardInDirectory(carddeck,available_deck_panel)
    
    #Player management
    players_panel = LabelFrame(root, text="Players")
    players_panel.pack(fill="both", expand="yes")
    
    players_list = Listbox(players_panel)
    players_list.pack()
    
    buttonframe = Frame(players_panel, borderwidth=2, relief=FLAT)
    buttonframe.pack()
    addPlayer=Button(buttonframe, text="Add", command=addingPlayer(players_list))
    addPlayer.pack(side=LEFT)
    removePlayer=Button(buttonframe, text="Remove", command=removingPlayer(players_list))
    removePlayer.pack(side=RIGHT)
    
    #Start game button
    play=Button(root, text="Start", command=StartGame(carddeck,players_list))
    play.pack()
    
##GAME
#Class to hold player information
class Player:
    #Select button manager
    class selectCard:
        def __init__(self,player):
            self.player = player
        def __call__(self):
            #Get the current number of choosed card
            indexOfEmptyCard = -1
            for i in range(3):
                if(len((self.player).selectedCard[i].get()) == 0):
                    indexOfEmptyCard = i
                    break
            
            #If the player try to choose more cards thatthe black card require, it shows an error message and stop the process
            if(indexOfEmptyCard>(self.player).whiteCardNumber or indexOfEmptyCard==-1):
                showerror("","You should only pick "+str((self.player).whiteCardNumber)+" cards!")
                return
            
            #Remove the card from players deck and put it in the selected card container
            ((self.player).selectedCard[indexOfEmptyCard]).set(((self.player).card).get(ACTIVE))
            ((self.player).card).delete(ACTIVE)

    #Unselect button manager
    class unselectCard:
        def __init__(self,player):
            self.player = player
        def __call__(self):
            #Get the index of the last selected card
            indexOfLastCard = -1
            for i in range(3):
                if(len((self.player).selectedCard[i].get()) != 0):
                    indexOfLastCard = i
            
            #If theres is no cards, it shows an error message and stop the process
            if(indexOfLastCard==-1):
                showerror("","No card to unselect!")
                return
            
            #Remove the card from selected card container and put it in the players deck
            ((self.player).card).insert(END,(self.player).selectedCard[indexOfLastCard].get())
            ((self.player).selectedCard[indexOfLastCard]).set("")

    #Finish turn button manager
    class finishTurn:
        def __init__(self,player):
            self.player = player
        def __call__(self):
            #Get the number of card choose
            numberOfCard = 0
            for i in range(3):
                if(len((self.player).selectedCard[i].get()) != 0):
                    numberOfCard +=1
            #If there isn't the right number , it shows an error message and stop the process
            if(numberOfCard!=(self.player).whiteCardNumber):
                showerror("","You should only select "+str((self.player).whiteCardNumber)+" card!")
                return
            #End the player turn
            (self.player).endTurn()
    
    #Player constructor
    def __init__(self,name,gameWindows):
        self.name = name
        self.playing = BooleanVar()
        self.whiteCardNumber = IntVar()
        self.point = IntVar()
        self.cards = None
        self.selectedCard = [StringVar(),StringVar(),StringVar()]
        
        self.playerFrame = Frame(gameWindows, borderwidth=2, relief=SUNKEN, padx=5, pady=5)
        Label(self.playerFrame,text="Turn of: "+str(name)).pack()
        
        #Choosed card frame
        selected_card_panel = LabelFrame(self.playerFrame, text="Your choice", padx=5, pady=5)
        selected_card_panel.pack(fill="both", expand="yes")
        
        Label(selected_card_panel,textvariable=self.selectedCard[0]).pack()
        Label(selected_card_panel,textvariable=self.selectedCard[1]).pack()
        Label(selected_card_panel,textvariable=self.selectedCard[2]).pack()
        
        #Player deck frame
        card_panel = LabelFrame(self.playerFrame, text="Your cards")
        card_panel.pack(fill="both", expand="yes")
        
        self.card = Listbox(card_panel,width=150)
        (self.card).pack(fill="both", expand="yes")
        
        buttonframe = Frame(card_panel, borderwidth=2, relief=FLAT)
        buttonframe.pack(fill="both", expand="yes")
        
        Button(buttonframe, text="Select", command=self.selectCard(self)).pack()
        Button(buttonframe, text="Unselect", command=self.unselectCard(self)).pack()
        
        #End of turn button
        Button(self.playerFrame, text="Finish turn", command=self.finishTurn(self)).pack()

    #To show and hide player deck on the main screen
    def pack(self):
        self.playerFrame.pack(expand=True)
    def unpack(self):
        self.playerFrame.pack_forget()

    def startTurn(self):
        self.playing.set(True)
        for i in self.selectedCard:
            i.set('')
    def endTurn(self):
        self.playing.set(False)
    def isPlaying(self):
        return self.playing
    
    def addWhiteCard(self,whitecard):       #Add whitecard to the player deck
        (self.card).insert(END,whitecard)
    def setWhiteCardNumber(self,number):    #Set the number of whitecard needed this turn
        self.whiteCardNumber = number
    
    def getSelectedCard(self):              #Return the card choosed by the player
        return self.selectedCard
    def getName(self):                      #Return the player name
        return self.name

    def addPoint(self):
        (self.point).set((self.point).get()+1)
    def getPoint(self):
        return self.point
 
#Class that manage the czar
class Czar:
    """Choose button manager
    This class add a point to the deck choose by the czar
    """
    class Choose:
        def __init__(self,czar,players):
            self.czar = czar
            self.players = players
        def __call__(self):
            self.players[(self.czar.cardToJudge)[(self.czar).czarChoose.get()].getPlayerID()].addPoint()
            (self.czar).endTurn()

    """
    This class holds information about the players deck and enables to have anonymous deck for the czar choose
    """
    class cardSelection:
        def __init__(self):
            self.playerID=-1
            self.playerCard = [StringVar(),StringVar(),StringVar()]
        def setPlayerID(self,id):
            self.playerID = id
        def getPlayerID(self):
            return self.playerID
        def setPlayerCard(self,playerCard):
            for i in range(len(playerCard)):
                self.playerCard[i].set(playerCard[i].get())
        def getPlayerCard(self):
            return self.playerCard  

    #Czar constructor: build czar GUI
    def __init__(self,players,gameWindows):
        self.binding = []
        self.czarChoose = IntVar()
        self.playing = BooleanVar()
        self.cardToJudge=[]
        self.czarFrame = Frame(gameWindows, borderwidth=2, relief=SUNKEN)
        for i in range(len(players)-1):
            (self.cardToJudge).append(self.cardSelection())
            cardFrame = Frame(self.czarFrame, borderwidth=2, relief=SUNKEN)
            cardFrame.pack()
            Radiobutton(cardFrame, variable=self.czarChoose, value=i).pack(anchor=W)
            Label(cardFrame,textvariable=(self.cardToJudge)[i].getPlayerCard()[0]).pack()
            Label(cardFrame,textvariable=(self.cardToJudge)[i].getPlayerCard()[1]).pack()
            Label(cardFrame,textvariable=(self.cardToJudge)[i].getPlayerCard()[2]).pack()
        Button(self.czarFrame, text="Choose", command=self.Choose(self,players)).pack()
    
    #Shuffle the card choose by the player to be anonymous
    def shuffle(self,czarID,players):
        self.binding=[]
        for i in range(len(players)):
            if(i!=czarID):
                self.binding.append(i)
        rd.shuffle(self.binding)
        for i in range(len(self.binding)):
            self.cardToJudge[i].setPlayerID(self.binding[i])
            self.cardToJudge[i].setPlayerCard(players[self.binding[i]].getSelectedCard())
    
    def getWinnerID(self):
        return self.cardToJudge[self.czarChoose.get()].getPlayerID()

    def startTurn(self):
        self.playing.set(True)
    def endTurn(self):
        self.playing.set(False)
    def isPlaying(self):
        return self.playing
    
    def pack(self):
        self.czarFrame.pack()
    def unpack(self):
        self.czarFrame.pack_forget()
    
#Get a random black card and remove it from the list of available black card
def getBlackCard(black):
    card = black.pop(rd.randint(0,len(black)-1))
    return (card.count("__"),card)

#Get a random white card to give to a player and remove it from the list of available white card
def getWhiteCard(white,player,number):
    for i in range(number):
        player.addWhiteCard(white.pop(rd.randint(0,len(white)-1)))

def mainGameLoop(playersNameList,white_cards,black_cards):
    players = []
    game_white_cards = list(white_cards)
    game_black_cards = list(black_cards)
    
    czar_id = 0
    winner_id = -1
    #Windows and GUI management
    gameWindows = Toplevel(root)
    gameWindows.minsize(width=400, height=600)
    gameWindows.title("Cards Against Humanity : Game")
    
    showCzarText = StringVar()
    Label(gameWindows,textvariable=showCzarText,bg="gray").pack()
    
    Label(gameWindows,text="Black card: ",font=('bold')).pack()
    showBlackText = StringVar()
    Label(gameWindows,textvariable=showBlackText).pack()
    
    player_point = LabelFrame(gameWindows, text="Points:", padx=20, pady=20)
    player_point.pack(fill="both", expand="yes")
    #---
    
    #Create a Player class for each player
    for i in range(len(playersNameList)):
        players.append(Player(playersNameList[i],gameWindows))
        getWhiteCard(game_white_cards,players[-1],5)
        #Label to show players point
        Label(player_point,text=players[-1].getName()).grid(row=i, column=0)
        Label(player_point,textvariable=players[-1].getPoint()).grid(row=i, column=1)
    
    #Create the Czar class
    czar = Czar(players,gameWindows)
    while(winner_id == -1):
        showCzarText.set("Czar this turn: "+players[czar_id].getName())
        
        nb_white_to_withdraw,txt = getBlackCard(game_black_cards)
        showBlackText.set(txt)
        
        #Player card choose loop
        for i in range(len(players)):
            if(i==czar_id):
                continue
            players[i].pack()
            getWhiteCard(game_white_cards,players[i],nb_white_to_withdraw)
            players[i].setWhiteCardNumber(nb_white_to_withdraw)
            players[i].startTurn()
            gameWindows.wait_variable(players[i].isPlaying())
            players[i].unpack()
            
        #Czar selection
        czar.pack()
        czar.startTurn()
        czar.shuffle(czar_id,players)
        gameWindows.wait_variable(czar.isPlaying())
        czar.unpack()
        
        #Check if the turn winner has win the game
        if(players[czar.getWinnerID()].getPoint().get()>5):
            winner_id = czar.getWinnerID()
        
        #Change the Czar
        czar_id+=1
        if(czar_id>=len(players)):
            czar_id =0
        
    showInformation("","This game winner is "+players[winner_id]+"!")

## Start function
root = Tk()
root.title("Cards Against Humanity, python v.0.1 by leaxs")
root.minsize(width=200, height=400)
startScreen()          

root.mainloop()