#-- blackjack game
#-- simple blackjack on the command line
#-- Jason Banks - jasonb@progensys.co.uk

import random
from random import shuffle

#--------------------------------------
class Player:
    def __init__(self,name, cash):
        self.name = name
        self.cash = cash


#--------------------------------------
class Card:
    def __init__(self,name,suite,value):
        self.name = name
        self.suite = suite
        self.value = value

    def Name(self):
        return self.name

    def DisplayName(self):
        return (self.name + " of " + self.suite)

    def Suite(self):
        return self.suite

    def PrintName(self):
        print (self.name + " of " + self.suite)

    def Value(self):
        return self.value
    
#--------------------------------------    
class Hand:
    def __init__(self):
        self.hand = list()

    def Hand(self):
        return self.hand

    #-- calculate the value of the blackjack hand
    def Score(self):
        score = 0
        acecount = 0
        for card in self.hand:           
            score += card.Value()
            if card.Value()==1:
                score+=10
                acecount+=1

        while score>21 and acecount>0:
            score-=10
            acecount-=1

        return score

    #-- display the hand
    def ShowHand(self):
        for card in self.hand:
            print ("  " + card.DisplayName())
        print ()

    #-- add a card to the hand
    def AddCard(self, card):
        self.hand.append(card)

#--------------------------------------    
class Deck:
    def __init__(self):
        #-- create a list to hold the deck in
        self.deck = list()

        #-- create a tuple of the suites
        self.suites = ("Hearts", "Spades", "Clubs", "Diamonds")

        #-- create a tuple o  f the card names
        self.cardnames = ("Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King")

        #-- expand the two tuples to get the complete deck plus values
        for suite in self.suites:
            cardval=1
            for cardname in self.cardnames:
                card = Card(cardname,suite, cardval)
                if cardval<10:
                    cardval+=1
                self.deck.append(card)
    
    #-- shuffles the deck
    def Shuffle(self):
        decksize = len(self.deck)
        print ("Shuffling "+str(decksize)+" cards")
        random.shuffle(self.deck)

    #-- displays the entire deck (start to finish)
    def ShowDeck(self):
        for card in self.deck:
            print (card.name)

    #-- Gets the next card from the deck - this version cycles the cards back to the end of the deck in a complete loop similar to actual blackjack
    def NextCard(self):
        rv = self.deck[0]
        self.deck.append(self.deck.pop(0))
        return rv


#-- game modes
MODE_TAKE_BET = 0
MODE_PLAYER_TURN = 1
MODE_DEALER_TURN = 2
MODE_BUST = 3
MODE_DEALERBUST = 4
MODE_SHOWDOWN = 5

#--------------------------------------    
class Game:  
    def __init__(self):
        self.hasQuit = False        
        self.deck = Deck() #-- create a new deck and shuffle it ready for use
        self.deck.Shuffle()
        self.player = Player("Player 1", 100) #-- create a player and give them 100 '$'                
        self.playerhand = Hand() #-- create empty hands for both player and dealer
        self.dealerhand = Hand()
        self.wager = 0
        self.gamemode = MODE_TAKE_BET        

    #-- check if we can continue to play or not
    def canKeepPlaying(self):
        if self.player.cash>0 and self.hasQuit!=True:
            return True
        return False

    #-- load player and dealer hands with two cards each
    def Deal(self):        
        self.playerhand.hand.clear()
        self.dealerhand.hand.clear()
        self.playerhand.AddCard(self.deck.NextCard())
        self.playerhand.AddCard(self.deck.NextCard())
        self.dealerhand.AddCard(self.deck.NextCard())
        self.dealerhand.AddCard(self.deck.NextCard())

    #-- ask the player for their wager
    def TakeBet(self):
        print ("You have $" + str(self.player.cash))
        print ()
        bet=-1
        while bet<0:
            bet = int(input("How much shall you bet? (0 to quit game and cash out)  "))
            if bet > self.player.cash:
                bet=-1
        if bet==0:
            self.hasQuit=True
        else:
            self.gamemode = MODE_PLAYER_TURN
            self.Deal()
        self.wager = bet

    #-- show the player hand and ask for their move (twist or stick)
    def PlayerTurn(self):
        print()
        print("Your hand is:")
        self.playerhand.ShowHand()        
        playermove=0
        while (playermove<1 or playermove>2):
            playermove = int(input("1=Twist, 2=Stick  "))
        if playermove==2:
            self.gamemode = MODE_DEALER_TURN
        else:
            self.playerhand.AddCard(self.deck.NextCard())
            if (self.playerhand.Score()>21):
                self.gamemode = MODE_BUST

    #-- show the dealer hand and ask for their move
    #-- assuming casino rules - dealer must stick over 17
    #-- and must twist if less than
    def DealerTurn(self):
        print()     
        print("Dealer hand is:")
        self.dealerhand.ShowHand()
        if (self.dealerhand.Score()>16):
            print ("Dealer Sticks")
            self.gamemode = MODE_SHOWDOWN
        else:
            print ("Dealer Twists")
            self.dealerhand.AddCard(self.deck.NextCard())
            if (self.dealerhand.Score()>21):
                self.gamemode = MODE_DEALERBUST

    #-- Handle the game result!
    def Result(self, message, winnings):
        print()
        print(message)
        self.player.cash += winnings
        self.gamemode = MODE_TAKE_BET
        print()

    #-- Player wins a round
    def Win(self):
        self.Result("!!!You Win!!!", self.wager)        

    #-- Player loses a round
    def Lose(self):
        self.Result("***House Wins***", -self.wager)        
    
    #-- round is drawn
    def Draw(self):
        self.Result("---A Draw---",0)
        

    #-- player goes bust
    def Bust(self):
        print ()
        print ("Sorry - you have bust with a total of: " + str(self.playerhand.Score()))
        self.playerhand.ShowHand()
        self.Lose()
        print ()
        
    #-- dealer goes bust
    def DealerBust(self):
        print ()
        print("The dealer has gone bust with a total of:" + str(self.dealerhand.Score()))
        self.dealerhand.ShowHand()
        self.Win()
        print ()

    #-- showdown between player and dealer - highest score wins
    def ShowDown(self):
        if (self.playerhand.Score()>self.dealerhand.Score()):
            self.Win()
        elif (self.playerhand.Score()<self.dealerhand.Score()):
            self.Lose()
        else:
            self.Draw()

    #-- main game loop
    def Play(self):
        #-- loop until the player loses or quits
        while self.canKeepPlaying():
            if self.gamemode==MODE_TAKE_BET:
                self.TakeBet()
            elif self.gamemode==MODE_PLAYER_TURN:
                self.PlayerTurn()
            elif self.gamemode==MODE_DEALER_TURN:
                self.DealerTurn()
            elif self.gamemode==MODE_BUST:
                self.Bust()
            elif self.gamemode==MODE_DEALERBUST:
                self.DealerBust()
            elif self.gamemode==MODE_SHOWDOWN:
                self.ShowDown()
        print("")


#-- create a new game object!
game = Game()
game.Play()
print()
print()


#-- show the exit message
if (game.player.cash>0):
    print ("congratulations - you walk away with $" + str(game.player.cash))
else:
    print ("Sorry - you appear to be out of cash - come back another time...")

print()
print()
print("Thank you for playing - blackjack")
print()
print()