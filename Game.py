from tkinter import *
from tkinter.messagebox import *
import random as rd

class Game:
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
        class undoCard:
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
                    showerror("","No card to undo!")
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
                (self.player).endTurn(False)
        
        #Player constructor
        def __init__(self,name,gameWindows):
            self.name = name
            self.hasCard = True
            self.playing = BooleanVar()
            self.whiteCardNumber = IntVar()
            self.point = IntVar()
            self.cards = None
            self.selectedCard = [StringVar(),StringVar(),StringVar()]
            
            self.playerFrame = Frame(gameWindows, borderwidth=2, relief=SUNKEN, padx=5, pady=5)
            
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
            
            Button(buttonframe, text="Undo", command=self.undoCard(self)).pack(side=RIGHT)
            Button(buttonframe, text="Select", command=self.selectCard(self)).pack(side=RIGHT)
            
            #End of turn button
            Button(self.playerFrame, text="Finish turn", command=self.finishTurn(self)).pack()
        
        #To show and hide player deck on the main screen
        def pack(self):
            (self.playerFrame).pack(expand=True)
        def unpack(self):
            (self.playerFrame).pack_forget()
        
        def startTurn(self):
            (self.playing).set(True)
            for i in self.selectedCard:
                i.set('')
        def endTurn(self,forced):
            (self.playing).set(False)
            self.hasCard = forced
        def isPlaying(self):
            return self.playing
        def hasCard(self):
            return self.hasCard
        
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
                    (self.playerCard)[i].set(playerCard[i].get())
            def getPlayerCard(self):
                return self.playerCard  
        
        #Czar constructor: build czar GUI
        def __init__(self,players,frame_center):
            self.czarChoose = IntVar()
            self.playing = BooleanVar()
            self.cardToJudge=[self.cardSelection() for i in players]
            
            #Czar frame
            self.czarFrame = Frame(frame_center, borderwidth=2, relief=SUNKEN)
            
            self.czarCardToChooseFrame = Frame(self.czarFrame)
            self.czarCardToChooseFrame.pack(fill="both", expand="yes")
            Button(self.czarFrame, text="Choose", command=self.Choose(self,players)).pack()
        
        #Shuffle the card choose by the player to be anonymous
        def shuffle(self,czarID,players):
            for widget in (self.czarCardToChooseFrame).winfo_children():
                widget.destroy()
            
            #Re-attribut all cardToJudge to each player
            for i in range(len(players)):
                if(i!=czarID and players[i].hasCard):
                    (self.cardToJudge)[i].setPlayerID(i)
                    (self.cardToJudge)[i].setPlayerCard(players[i].getSelectedCard())
                else:
                    (self.cardToJudge)[i].setPlayerID(-1)
            rd.shuffle(self.cardToJudge)
            
            #Checking if players has played and show his submission
            choosableDeck = 0
            for cards in self.cardToJudge:
                if(cards.getPlayerID() == -1):
                    continue
                cardFrame = Frame(self.czarCardToChooseFrame, borderwidth=2, relief=SUNKEN)
                cardFrame.pack(fill="both", expand="yes")
                Radiobutton(cardFrame, variable=self.czarChoose, value=choosableDeck).pack(anchor=W)
                Label(cardFrame,textvariable=cards.getPlayerCard()[0]).pack()
                Label(cardFrame,textvariable=cards.getPlayerCard()[1]).pack()
                Label(cardFrame,textvariable=cards.getPlayerCard()[2]).pack()
                choosableDeck+=1
                self.czarChoose.set(cards.getPlayerID())
            
            #if no ones has played, a default value is set
            if(choosableDeck==0):
                self.czarChoose.set(-1)
            #Check if czar can play (if there is enought deck to have a choice)
            return choosableDeck>1
        
        def getWinnerID(self):
            return (self.cardToJudge)[self.czarChoose.get()].getPlayerID()
        
        def startTurn(self):
            (self.playing).set(True)
        def endTurn(self):
            (self.playing).set(False)
        def isPlaying(self):
            return self.playing
        
        def pack(self):
            (self.czarFrame).pack(fill="both", expand="yes")
        def unpack(self):
            (self.czarFrame).pack_forget()
    
    class Timer:
        def __init__(self,frame_side,time,timevar):
            self.time = time
            self.timevar = timevar
            self.frame_side = frame_side
        
        def launch(self,player):
            self.player = player
            self.remaining_time = self.time
            (self.timevar).set("Remaining time: "+str(self.remaining_time)+"s")
            (self.frame_side).after(1000, self.tick)
        
        def tick(self):
            self.remaining_time -=1
            self.timevar.set("Remaining time: "+str(self.remaining_time)+"s")
            if(self.remaining_time<=0):
                (self.player).endTurn(True)
            else:
                (self.frame_side).after(1000, self.tick)
    ##
    def __init__(self,root,playerslist,calls,reponses,gameParameters):
        #Class variable
        self.czarName = StringVar()
        self.showCall = StringVar()
        self.turnOf = StringVar()
        self.remaningTime = StringVar()
        
        self.players = []
        self.initialCall = list(calls)
        self.initialReponses = list(reponses)
        
        self.game_calls = list(calls)
        self.game_reponses = list(reponses)
        
        self.czar_id = 0
        
        self.time_limite = gameParameters[0]
        self.score_limit = gameParameters[1]
        self.same_card_several_occurence = gameParameters[2]
        
        #gameWindows
        self.gameWindows = Toplevel(root)
        self.gameWindows.minsize(width=400, height=600)
        self.gameWindows.resizable(0,0)
        self.gameWindows.title("Cards Against Humanity : Game")
        self.gameWindows.iconbitmap('icon.ico')
        
        #Side frame
        frame_side = Frame(self.gameWindows)
        Label(frame_side, textvariable = self.czarName).grid(row=0,column=0)
        frame_side.grid(row=0,column=0,rowspan=2)
        
        self.frame_points = LabelFrame(frame_side, text="Scoreboard")
        self.frame_points.grid(row=1,column=0)
        frame_information = LabelFrame(frame_side, text="Information")
        frame_information.grid(row=2,column=0)
        
        Label(frame_information, textvariable = self.turnOf).grid(row=0,columnspan=2)
        Label(frame_information, textvariable = self.remaningTime).grid(row=1,column=0)
        
        #Center frame
        frame_center = Frame(self.gameWindows)
        frame_center.grid(row=1,column = 1,rowspan = 2)
        Label(frame_center, textvariable = self.showCall).pack(side=TOP)
        
        #Check if the Timer is needed for the game
        if(self.time_limite != 0):
            self.timer = self.Timer(frame_side,self.time_limite,self.remaningTime)
            
        #Create a Player class for each player
        for pl in playerslist:
            (self.players).append(self.Player(pl,frame_center))
            self.getWhiteCard(self.players[-1],5)
        
        #Create the Czar class
        (self.czar) = self.Czar(self.players,frame_center)
        self.update_scoreboard()
        self.turn()

    #Get a random black card and remove it from the list of available black card
    def getBlackCard(self):
        card = (self.game_calls).pop(rd.randint(0,len((self.game_calls))-1))
        return (card.count("__"),card)

    #Get a random white card to give to a player and remove it from the list of available white card
    def getWhiteCard(self,player,number):
        for i in range(number):
            card = (self.game_reponses).pop(rd.randint(0,len((self.game_reponses))-1))
            player.addWhiteCard(card)
            if(self.same_card_several_occurence):
                (self.gameReponses).append(card)
    
    #Update the side scoreboard (czar and point)
    def update_scoreboard(self):
        for widget in (self.frame_points).winfo_children():
            widget.destroy()
        for i in range(len(self.players)):
            name = str(self.players[i].getName()+": "+str((self.players)[i].getPoint().get()))
            if(i == self.czar_id):
                Label(self.frame_points, text=name,bg="gray").grid()
            else:
                Label(self.frame_points, text=name).grid()
    
    def turn(self):
        (self.czarName).set("Czar this turn: "+self.players[self.czar_id].getName())
        
        nb_white_to_withdraw,txt = self.getBlackCard()
        (self.showCall).set(txt)
        
        #Player card choose loop
        for i in range(len((self.players))):
            if(i==self.czar_id):
                continue
            (self.turnOf).set("Turn of : "+(self.players)[i].getName())
            if(self.time_limite != 0):
                self.timer.launch((self.players)[i])
            (self.players)[i].pack()
            self.getWhiteCard((self.players)[i],nb_white_to_withdraw)
            (self.players)[i].setWhiteCardNumber(nb_white_to_withdraw)
            (self.players)[i].startTurn()
            (self.gameWindows).wait_variable((self.players)[i].isPlaying())
            (self.players)[i].unpack()
            
        #Czar selection
        (self.turnOf).set("Turn of : "+(self.players)[self.czar_id].getName())
        (self.czar).pack()
        (self.czar).startTurn()
        if((self.czar).shuffle(self.czar_id,self.players)):
            (self.gameWindows).wait_variable((self.czar).isPlaying())
        (self.czar).unpack()
        
        #Change the Czar
        (self.czar_id)+=1
        if((self.czar_id)>=len((self.players))):
            (self.czar_id) = 0
        
        #Check if the turn winner has win the game
        if(self.players[self.czar.getWinnerID()].getPoint().get()>=self.score_limit):
            showinfo("","This game winner is "+self.players[(self.czar).getWinnerID()].getName()+"!")
            self.gameWindows.destroy()
        else:
            self.update_scoreboard()
            self.turn()
        