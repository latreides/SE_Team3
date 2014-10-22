from db_interactions import *
from models import *
from django.contrib.auth.models import User


def getNextCard():
    "Function to call next card."
    
    deck = Deck.objects(pk = 1) #will need to modify, only for playing purposes
    deckOfCards = GetCardsForDeck(deck)
    card = Card.objects.random(deckOfCards)
    return card 