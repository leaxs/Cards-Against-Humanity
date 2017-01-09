"""
@author leaxs
"""
from tkinter import *
from tkinter.messagebox import *
from tkinter.simpledialog import *

import codecs
import os 
import Game 

class MainScreen: 
    ##Button manager
    #Add player to the party
    class addingPlayer:
        def __init__(self,mainscreen):
            self.mainscreen = mainscreen
        def __call__(self):
            name = askstring("Adding player","Player name?")
            (self.mainscreen).players_list.insert(END,name)

    #Remove the selected player in listbox
    class removingPlayer:
        def __init__(self,mainscreen):
            self.mainscreen = mainscreen
        def __call__(self):
            if(askokcancel("Removing player", "Would you really remove "+((self.mainscreen).players_list).get(ACTIVE)+" from the party?")):
                (self.mainscreen).players_list.delete(ACTIVE)
    
    #Resfresh decklist
    class refresh:
        def __init__(self,mainscreen):
            self.mainscreen = mainscreen
        def __call__(self):
            self.mainscreen.decks = []
            for widget in (self.mainscreen).frame_decklist.winfo_children():
                widget.destroy()
                
            (self.mainscreen).getCardInDirectory((self.mainscreen).decks,(self.mainscreen).frame_decklist)
    
    #Hold information of a deck
    class Carddeck:
        def __init__(self,name,var):
            self.name = name.split('.')[0]
            self.reponses = []
            self.calls = []
            self.enable = var
            
            isCall = True
            f = codecs.open("Carddeck/"+name, encoding='utf-8')
            for line in f:
                if("\end"in line):
                    isCall = False
                    continue
                if(isCall):
                    (self.calls).append(line[:-2])      #-2 to remove \r
                else:
                    (self.reponses).append(line[:-2])
            f.close()
        
        def getReponses(self):
            return self.reponses
        def getCalls(self):
            return self.calls
        
        def getDeckName(self):
            return self.name
        
        def isEnable(self):
            return (self.enable).get()
        
        #Information for main screen display (name, calls numbers, reponses numbers)
        def getDeckNameinfo(self):
            return (self.name+" (c:"+str(len(self.calls))+" /r:"+str(len(self.reponses))+")")
    
    #Start button manager
    class StartGame:
        def __init__(self,mainscreen):
            self.mainscreen = mainscreen
        def __call__(self):
            #Check if there is enought players (minimum is 3)
            players = ((self.mainscreen).players_list).get(0,END)
            if(len(players)<=2):
                showerror("","Not enought player!")
                return
                
            #Getting calls and reponses cards
            reponses = []
            calls = []
            for deck in (self.mainscreen).decks:
                if(deck.isEnable()):
                    reponses.extend(deck.getReponses())
                    calls.extend(deck.getCalls())
            #Check if there is at least one call and one reponse cards
            if(len(calls) == 0 and len(reponses)==0):
                showerror("","Selected decks doesn't contains any card!")
                return
            elif(len(calls) == 0):
                showerror("","Selected decks doesn't contains any call card!")
                return
            elif(len(reponses)==0):
                showerror("","Selected decks doesn't contains any reponse card!")
                return
                
            #Launch the game
            Game.Game((self.mainscreen).root,players,calls,reponses,(self.mainscreen).getGameParameters())
    
    ##
    def __init__(self,root):
        #Class variable
        self.decks = []  #Contains the deck that can be played
        self.players_list = None
        self.time_limite = None
        self.score_limite = None
        self.same_card_several_occurence = BooleanVar()
        self.root = root
        
        #Frame 
        frame_deck = LabelFrame(root, text="Game deck(s)")
        frame_parameters = LabelFrame(root, text="Game parameters")
        frame_players = LabelFrame(root, text="Players")
        
        frame_deck.grid(row=0,column=0,sticky ="w")
        frame_parameters.grid(row=0,column=1,sticky ="NW")
        frame_players.grid(row=1,columnspan=2,sticky ="EW")
        
        #Frame_deck
        self.frame_decklist = Frame(frame_deck)
        self.getCardInDirectory(self.decks,self.frame_decklist)
        
        (self.frame_decklist).pack(fill="both", expand="yes")
        Button(frame_deck, text="Refresh", command=self.refresh(self)).pack(fill="both", expand="yes", side=BOTTOM)
        
        #Frame_parameters
        self.score_limite = Spinbox(frame_parameters, from_=1, to_=100)
        self.time_limite = Spinbox(frame_parameters, from_=0, to_=120)
        
        Label(frame_parameters,text="Time limit (0 = no limit)").grid(row=0,column=0,sticky ="w")
        (self.time_limite).grid(row=0,column=1,sticky ="w")
        Label(frame_parameters,text="Score to win").grid(row=1,column=0,sticky ="w")
        (self.score_limite).grid(row=1,column=1,sticky ="w")
        
        Checkbutton(frame_parameters,variable=self.same_card_several_occurence,text="Allow several occurence of cards",onvalue=True, offvalue=False).grid(columnspan=2)
        
        #Frame_players
        self.players_list = Listbox(frame_players)
        buttonframe = Frame(frame_players, borderwidth=2, relief=FLAT)
        Button(buttonframe, text="Remove", command=self.removingPlayer(self)).pack(side=RIGHT)
        Button(buttonframe, text="Add", command=self.addingPlayer(self)).pack(side=RIGHT)
       
        (self.players_list).pack(fill="both", expand="yes")
        buttonframe.pack(fill="both", expand="yes", side=BOTTOM)
        
        #PlayButton
        Button(root, text="Start", command=self.StartGame(self)).grid(row=3,columnspan=2,sticky='EW')
        
    #Research all files in carddeck directory and return their name
    def getCardInDirectory(self,decks,frame):
        card_dir = os.listdir('Carddeck') 
        for i in card_dir:
            var = BooleanVar()
            deck=self.Carddeck(i,var)
            Checkbutton(frame,variable=var,text=deck.getDeckNameinfo(),onvalue=True, offvalue=False).grid(sticky="W")
            decks.append(deck)
            
    def getGameParameters(self):
        return [int((self.time_limite).get()),int((self.score_limite).get()),(self.same_card_several_occurence).get()]
##
root = Tk()
root.title("Cards Against Humanity, v.0.2")
root.iconbitmap('icon.ico')
root.resizable(0,0)
MainScreen(root)      
root.mainloop()