import yaml
from models import Deck, Card
from db_interactions import *
from django.contrib.auth.models import User

class parseConfig:
    "Handles parsing, exporting, importing of deck configs"

    def __init__(self):
        self.decks_location = "./decks/"
        self.deck = {}

    def importDeck(self, request, filename):
        "Import deck to file"
            
        if request.user.is_authenticated():
            self.deck = yaml.load(filename)
            decks = self.getListOfDecks()
            cards = self.getListOfCards(decks[0])
            deck = createDeck(1, decks[0])
            
            importedDeck = self.getDeck()
            for cards in importedDeck.values():
                for qNa in cards.values():
                    question = qNa[0].values()[0]
                    answer = qNa[1].values()[0]
                    createCard(deck.id, False, question, answer)
            return True
        else:
            return False

    def getDeck(self):
        return self.deck

    #def exportDeck(self, filename):
        #"Export deck to file"
        #with open(self.decks_location + filename, 'w') as f:
            #f.write(yaml.dump(self.deck, default_flow_style=False))

    def getListOfDecks(self):
        """Get list of decks in file
            Returns a list"""
        retVal = []
        if self.deck:
            retVal = [deckName for deckName in self.deck]
        return retVal

    def getListOfCards(self, deckName):
        """Get list of cards for deck in file
            Expects a string for deckname
            Returns a list"""
        retVal = []
        if self.deck and self.deck[deckName]:
            retVal = [card for card in self.deck[deckName]]
        return retVal
