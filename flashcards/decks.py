import yaml

class parseConfig:
    "Handles parsing, exporting, importing of deck configs"

    def __init__(self):
        self.decks_location = "./decks/"
        self.deck = {}

    def importDeck(self, filename):
        "Import deck to file"
        with open(self.decks_location + filename, 'r') as f:
            self.deck = yaml.load(f)

    def getDeck(self):
        return self.deck

    def exportDeck(self, filename):
        "Export deck to file"
        with open(self.decks_location + filename, 'w') as f:
            f.write(yaml.dump(self.deck, default_flow_style=False))

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


#Testing below
if __name__ == "__main__":
    parser = parseConfig()
    parser.importDeck("testdeck.yml")
    decks = parser.getListOfDecks()
    cards = parser.getListOfCards(decks[0])
    print decks
    print cards
    print yaml.dump(parser.getDeck(), default_flow_style=False)