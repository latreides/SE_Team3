import yaml
from models import Deck, Card
from decks import parseConfig
from db_interactions import *


def importDeck(fileName):
    """
        Imports a deck from Yaml file.
    """
    
    parser = parseConfig()
    parser.importDeck(fileName)
    decks = parser.getListOfDecks()
    cards = parser.getListOfCards(decks[0])
    deck = createDeck(1, decks[0])

    importedDeck = parser.getDeck()
    for cards in importedDeck.values():
        for qNa in cards.values():
            question = qNa[0].values()[0]
            answer = qNa[1].values()[0]
            createCard(deck.id, False, question, answer, 1, 1)
