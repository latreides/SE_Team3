from db_interactions import *
from random import randint

def getNextCard(deckId):
    deckOfCards = getCardsForDeck(deckId)
    card = deckOfCards.order_by('?')[0]
    return card
