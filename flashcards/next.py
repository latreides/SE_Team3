from db_interactions import *
from random import randint

def getNextCard(deckId):
    deckOfCards = GetCardsForDeck(deckId)
    card =  deckOfCards.objects.order_by('?')[0]
    return card
