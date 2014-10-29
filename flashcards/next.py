from db_interactions import *
from models import *
from django.contrib.auth.models import User
from random import randint

def getNextCard():
    "Function to call next card."
    
    numOfDecks = Deck.objects.count()
    deckID = randint(1, numOfDecks)
    deck = Deck.objects.get(pk = deckID) #will need to modify, only for playing purposes
    deckOfCards = GetCardsForDeck(deck)
    numOfCards = 0
    
    for card in deckOfCards:
        numOfCards = numOfCards + 1
        
    cardID = randint(1, numOfCards)
    card =  Card.objects.get(pk = cardID)
    return card 