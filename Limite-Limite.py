from tkinter import *
from tkinter.messagebox import *
from tkinter.simpledialog import *
import codecs
import random as rd
import time
import os 

##Start screen

class addingPlayer:
    def __init__(self,players_list):
        self.players_list = players_list
    def __call__(self):
        name = askstring("Adding player","Player name?")
        (self.players_list).insert(END,name)

class removingPlayer:
    def __init__(self,players_list):
        self.players_list = players_list
    def __call__(self):
        if(askokcancel("Removing player", "Would you really remove "+(self.players_list).get(ACTIVE)+" from the party?")):
            (self.players_list).delete(ACTIVE)

def getCardInDirectory(carddeck,panel):
    card_dir = os.listdir('Carddeck') 
    for i in card_dir:
        var = BooleanVar()
        checkbox = Checkbutton(panel,variable=var,text=i,onvalue=True, offvalue=False)
        checkbox.pack()
        carddeck.append((i,var))

def startScreen():
    #Deck choose
    available_deck_panel = LabelFrame(root, text="Choose your deck")
    available_deck_panel.pack(fill="both", expand="yes")
    
    carddeck = []
    getCardInDirectory(carddeck,available_deck_panel)
    
    #player management
    
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
    
    play=Button(root, text="Start", command=StartGame(carddeck,players_list))
    play.pack()
    

##GAME
class StartGame:
    def __init__(self,detectedDeck,players):
        self.players_list = players
        self.carddeck = detectedDeck
    def __call__(self):
        players = (self.players_list).get(0,END)
        if(len(players)<=1):
            showerror("","Not enought player!")
            return
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

        mainGameLoop(players,white_cards,black_cards)
        
class Player:
    class selectCard:
        def __init__(self,player):
            self.player = player
        def __call__(self):
            indexOfEmptyCard = -1
            for i in range(3):
                if(len((self.player).selectedCard[i].get()) == 0):
                    indexOfEmptyCard = i
                    break
            
            if(indexOfEmptyCard>(self.player).whiteCardNumber or indexOfEmptyCard==-1):
                showerror("","You should only pick "+str((self.player).whiteCardNumber)+" cards!")
                return
                
            ((self.player).selectedCard[indexOfEmptyCard]).set(((self.player).card).get(ACTIVE))
            ((self.player).card).delete(ACTIVE)

    class unselectCard:
        def __init__(self,player):
            self.player = player
        def __call__(self):
            indexOfLastCard = -1
            for i in range(3):
                if(len((self.player).selectedCard[i].get()) != 0):
                    indexOfLastCard = i
            
            if(indexOfLastCard==-1):
                showerror("","No card to unselect!")
                return
                
            print((self.player).selectedCard[indexOfLastCard].get())
            ((self.player).card).insert(END,(self.player).selectedCard[indexOfLastCard].get())
            ((self.player).selectedCard[indexOfLastCard]).set("")

    class finishTurn:
        def __init__(self,player):
            self.player = player
        def __call__(self):
            numberOfCard = 0
            for i in range(3):
                if(len((self.player).selectedCard[i].get()) != 0):
                    numberOfCard +=1
            if(numberOfCard!=(self.player).whiteCardNumber):
                showerror("","You should only select "+str((self.player).whiteCardNumber)+" card!")
                return
            (self.player).endTurn()
            
    def __init__(self,name,gameWindows):
        self.name = name
        self.playing = BooleanVar()
        self.whiteCardNumber = IntVar()
        self.point = IntVar()
        self.cards = None
        self.selectedCard = [StringVar(),StringVar(),StringVar()]
        
        self.playerFrame = Frame(gameWindows, borderwidth=2, relief=SUNKEN, padx=5, pady=5)
        Label(self.playerFrame,text="Turn of: "+str(name)).pack()
        
        #Card Selected
        selected_card_panel = LabelFrame(self.playerFrame, text="Your choice", padx=5, pady=5)
        selected_card_panel.pack(fill="both", expand="yes")
        
        Label(selected_card_panel,textvariable=self.selectedCard[0]).pack()
        Label(selected_card_panel,textvariable=self.selectedCard[1]).pack()
        Label(selected_card_panel,textvariable=self.selectedCard[2]).pack()
        
        #Card of the player
        card_panel = LabelFrame(self.playerFrame, text="Your cards")
        card_panel.pack(fill="both", expand="yes")
        
        self.card = Listbox(card_panel,width=150)
        (self.card).pack(fill="both", expand="yes")
        
        buttonframe = Frame(card_panel, borderwidth=2, relief=FLAT)
        buttonframe.pack(fill="both", expand="yes")
        
        Button(buttonframe, text="Select", command=self.selectCard(self)).pack()
        Button(buttonframe, text="Unselect", command=self.unselectCard(self)).pack()
        
        Button(self.playerFrame, text="Finish turn", command=self.finishTurn(self)).pack()

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
        
    def addWhiteCard(self,whitecard):
        (self.card).insert(END,whitecard)
    def setWhiteCardNumber(self,number):
        self.whiteCardNumber = number
    
    def getSelectedCard(self):
        return self.selectedCard
    def getName(self):
        return self.name

    def addPoint(self):
        (self.point).set((self.point).get()+1)
    def getPoint(self):
        return self.point
 
class Czar:
    class Choose:
        def __init__(self,czar,players):
            self.czar = czar
            self.players = players
        def __call__(self):
            self.players[(self.czar.cardToJudge)[(self.czar).czarChoose.get()].getPlayerID()].addPoint()
            (self.czar).endTurn()

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
    
def getBlackCard(black):
    card = black.pop(rd.randint(0,len(black)-1))
    return (card.count("__"),card)
    
def getWhiteCard(white,player,number):
    for i in range(number):
        player.addWhiteCard(white.pop(rd.randint(0,len(white)-1)))

def mainGameLoop(playersNameList,white_cards,black_cards):
    players = []
    game_white_cards = list(white_cards)
    game_black_cards = list(black_cards)
    
    czar_id = 0
    winner_id = -1
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
    #Player generation
    for i in range(len(playersNameList)):
        players.append(Player(playersNameList[i],gameWindows))
        getWhiteCard(game_white_cards,players[-1],5)
        Label(player_point,text=players[-1].getName()).grid(row=i, column=0)
        Label(player_point,textvariable=players[-1].getPoint()).grid(row=i, column=1)

    czar = Czar(players,gameWindows)
    while(winner_id == -1):
        showCzarText.set("Czar this turn: "+players[czar_id].getName())
        
        nb_white_to_withdraw,txt = getBlackCard(game_black_cards)
        showBlackText.set(txt)
        
        #Player card selection
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
        
        if(players[czar.getWinnerID()].getPoint().get()>5):
            winner_id = czar.getWinnerID()
            
        czar_id+=1
        if(czar_id>=len(players)):
            czar_id =0
        
    showInformation("","This game winner is "+players[winner_id]+"!")
        
## Global var / start function

root = Tk()
root.title("Cards Against Humanity, python v.0.1 by leaxs")
root.minsize(width=200, height=400)
startScreen()          

root.mainloop()