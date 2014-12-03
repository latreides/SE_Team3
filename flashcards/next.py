from db_interactions import *
from random import randint

def getNextCard(deckId):
    """
        Selects and returns a random card.
    """
    deckOfCards = getCardsForDeck(deckId)
    card = deckOfCards.order_by('?')[0]
    return card
