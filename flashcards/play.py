from flashcards.models import *
from flashcards.db_interactions import *
from random import shuffle
from random import randint
from json import dumps

class engine:

    def __init__(self):
        self.boxes = {k:[] for k in range(1,6)}
        self.deckId = None
    
    def sortCardsInBoxes(self, cardlist):
        for card in cardlist:
            if card.Difficulty:
                self.boxes[card.Difficulty].append(card)
            else:
                self.boxes[5].append(card)
        map(shuffle, self.boxes.values())   
    
    def play(self, deckId):
        #deck = getDeck(deckId)
        self.deckId = int(deckId)
        cardlist = getCardsForDeck(deckId)
        self.sortCardsInBoxes(cardlist)
        
    #Temp function
    def getNextCard(self):
        deckOfCards = getCardsForDeck(self.deckId)
        card = deckOfCards.order_by('?')[0]
        return card
        
    def toJson(self):
        return dumps(self)

        
    
