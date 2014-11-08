from flashcards.models import *
from flashcards.db_interactions import *
from random import shuffle
from random import randint
from random import choice
from json import dumps

#This is the amount of difficulties available
NUMBOXES = 5

class engine:
    """
        Class for producing a spaced repetition algorithm
        - Based on Leitner system described at en.wikipedia.org/wiki/Spaced_repetition
        - Uses a box type system where boxes are difficulties of cards
    """

    def __init__(self):
        self.boxes = {k:[] for k in range(1,NUMBOXES+1)}
        self.deckId = None
    
    def sortCardsInBoxes(self, cardlist):
        """
            Puts cards in appropriate boxes, if card has no 
            difficulty it defaults to 5 as this is assumed
            to be a new card
        """
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
    
    def buildLotteryList(self):
        """ The lottery list will be percentage based on picking which
            box to draw a card from. The percentage to pick is based on how
            many difficulties there are.
            Ex: 2 difficulties will be a list of 1^2 and 2 ^ 2 or
                [1, 2, 2, 2, 2] which makes the percentage to pick an easy card 1/5
            As you add difficulty levels sequentially it continues to grow by n^2
        """
        lotteryList = []
        for i in range(1, NUMBOXES+1):
            n = i
            #This gives the bottom 3 difficulties more weight for balance
            if i < 4:
                n += 1
            if self.boxes[i] != []:
                lotteryList += [i] * i ** n
        return lotteryList
    
    def pickBox(self):
        """
            Picks a box(difficulty) to draw from
        """
        lotteryList = self.buildLotteryList()
        shuffle(lotteryList)
        cardChoice = choice(lotteryList)
        return (cardChoice)
        
    
    def getNextCard(self):
        boxNum = self.pickBox()
        cards = self.boxes[boxNum]
        return choice(cards)
    
    def getRandomCard(self):
        deckOfCards = getCardsForDeck(self.deckId)
        card = deckOfCards.order_by('?')[0]
        return card
        
    def toJson(self):
        return dumps(self)

        
    
