import yaml
from models import Deck, Card
from db_interactions import *
from django.contrib.auth.models import User
#from os import getcwd

class parseConfig:
    "Handles parsing, exporting, importing of deck configs"

    def __init__(self):
        self.decks_location = "/decks/"
        self.deck = {}

    def importDeck(self, request, filename):
        "Import deck to database from file"
            
        if request.user.is_authenticated():
            self.deck = yaml.load(filename)
            decks = self.getListOfDecks()
            cards = self.getListOfCards(decks[0])
            deck = createDeck(1, decks[0])
            if cards == []:
                return True, deck
            
            importedDeck = self.getDeck()
            for cards in importedDeck.values():
                for qNa in cards.values():
                    front = qNa[0].values()[0]
                    back = qNa[1].values()[0]
                    frontImgPath = qNa[2].values()[0]
                    backImgPath = qNa[3].values()[0]
                    frontImg = createImage(frontImgPath)
                    backImg = createImage(backImgPath)

                    createCard(deck.id, False, front, back, frontImg.id, backImg.id)
                        
            return True, deck
        else:
            return False, deck

    def getDeck(self):
        return self.deck

    def exportDeck(self, request, deckID):
        "Export deck to file"
        exportDeck = Deck.objects.get(pk = deckID)
        dictOfCards = {}
        cards = getCardsForDeck(exportDeck)
        for card in cards:
            #Prepping cards for export
            front = {'q': str(card.Front_Text)}                 
            back = {'a': str(card.Back_Text)}
            frontImgId = card.Front_Img_ID_id
            backImgId = card.Back_Img_ID_id
            frontImgPath = Image.objects.get(pk = frontImgId)
            backImgPath = Image.objects.get(pk = backImgId)
            frontImg = {'frontImg': str(frontImgPath)}
            backImg = {'backImg': str(backImgPath)}
            exportList = [front, back, frontImg, backImg]
            exportCard = {("card" + str(card.id)): exportList}
            
            dictOfCards.update(exportCard)
        
        self.deck = {str(exportDeck.Name): dictOfCards}
        formattedDeck = yaml.dump(self.deck, default_flow_style = False)
        return formattedDeck
            
        #with open(getcwd() + "/flashcards/decks/" + exportDeck.Name + ".yml", 'w') as f:
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
