import yaml
import sqlite3
from decks import parseConfig


class dbInterface:
    "The interface that will handle importing/exporting to the database"

    def __init__(self):
        self.db_location = "../flashcards.sqlite3"
        self.decks_location = "./decks/"


#For Testing Purposes
if __name__ == "__main__":
    db = dbInterface()
    parser = parseConfig()
    deck = "testdeck.yml"
    parser.importDeck(deck1)
    decks = parser.getListOfDecks()
    cards = parser.getListOfCards(decks[0])

#Will be added to Jason's Import function when working correctly
#----------------IMPORTING----------------#

    #Establish db connection
    conn = sqlite3.connect(db.db_location)
    conn.text_factory = str
    c = conn.cursor()

    #Create a table to hold deck's cards
    c.execute("CREATE TABLE IF NOT EXISTS deck (question, answer)")
    conn.commit()

    #Create rows for the cards
    deck = parser.getDeck()
    for cards in deck.values():
        for qNa in cards.values():
            c.execute("INSERT INTO deck VALUES (?, ?)", (qNa[0].values()[0], qNa[1].values()[0]))
            conn.commit()

    #Testing if cards are in database
    #for row in c.execute("SELECT * FROM deck"):
        #print row

    #For testing purposes
    #c.execute("DELETE FROM deck")
    #conn.commit()

    #Close db connection
    conn.close()

#Will be added to Jason's Export function when working correctly
#----------------EXPORTING----------------#

    #Establish db connection
    conn = sqlite3.connect(db.db_location)
    conn.text_factory = str
    c = conn.cursor()
    i = 1
    dictOfCards = {}

    #Test
    #c.execute("INSERT INTO deck VALUES ('What is 1 + 1?', '2')")
    #conn.commit()

    #Prepping data for export into yaml file
    for row in c.execute("SELECT * FROM deck"):
        q = row[0]
        a = row[1]

        cardQuestion = {'q': q}
        cardAnswer = {'a': a}

        myList = [cardQuestion, cardAnswer]

        cardNum = {("card" + str(i)): myList}
        i += 1

        dictOfCards.update(cardNum)

    yourDeck = {'YourDeck': dictOfCards}

    #Exports data into yaml file
    with open(db.decks_location + "YourDeck.yml", 'w') as f:
        f.write(yaml.dump(yourDeck, default_flow_style = False))

    #For testing purposes
    c.execute("DELETE FROM deck")
    conn.commit()

    #Close db connection
    conn.close()








        
