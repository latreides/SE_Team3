from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from flashcards.models import *
from datetime import datetime
from django.utils.timezone import utc
from re import escape

def getNow():
    '''
    Generic Helper Function for Time Zone aware now()
    '''
    return datetime.now().replace(tzinfo=utc)


def createDeck(userID, deckName):
    '''
    Creates a new deck object given a name for the deck and the userID for the user who is creating the deck
    and returns the new deck as an object of type deck
    '''
    try:
        userObj = User.objects.get(id = userID)
    except (ValueError, ObjectDoesNotExist):
        print "The given User ID does not exist in the database"

    newDeck = Deck(Name = deckName, User_ID = userObj, Create_Date=timezone.now())
    newDeck.save()
    return newDeck

def deleteDeck(deckId):
    '''
    Deletes an entire Deck
    '''
    foundDeck = Deck.objects.get(id=deckId)
    if foundDeck:
        foundDeck.delete()

def resetDeck(deckId):
    '''
    Resets scores in an entire Deck
    '''
    foundDeck = Deck.objects.get(id=deckId)
    if foundDeck:
        cards = getCardsForDeck(deckId)
        for card in cards:
            card.Difficulty = None
            card.save()

def createCard(deckID, twoSided, frontText = None, backText = None, frontImageID = None, backImageID = None):
    '''
    Creates a new card object given the deck the card belongs to, a boolean value indicating if either side of the
    card can be considered the front, and optionally text or images that the card would display.
    **** To link an image the image must already be in the database ****
    Returns the card object that was created
    '''
    if backImageID != None:
        try:
            backImageObj = Image.objects.get(id = backImageID)
        except (ValueError, ObjectDoesNotExist):
            print "The ID provided for the back image id does not exist in the image table."
    else:
        backImageObj = None

    if frontImageID != None:
        try:
            frontImageObj = Image.objects.get(id = frontImageID)
        except (ValueError, ObjectDoesNotExist):
            print "The ID provided for the front image id does not exist in the image table."
    else:
        frontImageObj = None

    try:
        DeckObj = Deck.objects.get(id = deckID)
    except (ValueError, ObjectDoesNotExist):
            print "The User ID provided does not exist in the database"
    newCard = Card(Deck_ID = DeckObj, Front_Text = frontText, Back_Text = backText, Front_Img_ID = frontImageObj, Back_Img_ID = backImageObj, Two_Sided = twoSided)
    newCard.save()
    return newCard

def deleteCard(cardId):
    '''
    Deletes a card from the Deck
    '''
    foundCard = Card.objects.get(id=cardId)
    if foundCard:
        foundCard.delete()


def createImage(pathToImage):
    '''
    Creates a new image entry in the database given a path to the image on the server or web
    Returns the object of type image created by the database
    '''
    newImage = Image(Image_Path = pathToImage)
    newImage.save()
    return newImage


def getMostRecentDeck(userID):
    '''
    Returns an object containing the most recent deck accessed by the user id passed into the function
    '''
    return Deck.objects.order_by('-Accessed_Date')[0] if Deck.objects.filter(User_ID=userID).exclude(Accessed_Date__isnull=True).exists() else None


def getDecksForUser(userID):
    '''
    Returns a list containing all the decks that the current user has as Deck objects
    '''
    return Deck.objects.filter(User_ID=userID)


def getDeck(deckID):
    '''
    Returns a single specific Deck
    '''
    return Deck.objects.filter(id=deckID).first()


def getCard(cardID):
    '''
    Returns a single specific Card
    '''
    return Card.objects.get(id=cardID)


def getCardsForDeck(deckID):
    '''
    Returns a list containing all the cards as objects belonging to the deck ID that was passed in
    '''
    return Card.objects.filter(Deck_ID=deckID)


def getLastTimeLoggedIn(userID):
    '''
    Return the last time the user logged in as a string
    '''
    try:
        userObj = User.objects.get(id=userID)
    except (ValueError, ObjectDoesNotExist):
        print "The given User ID does not exist in the database"
    return userObj.last_login.strftime('%b-%d-%Y %I:%M:%S %p')

def getCountCardsWithDifficulty(deckID, difficulty):
    '''
    Returns the number of cards in the given deck with the given difficulty
    '''
    return Card.objects.filter(Deck_ID=deckID, Difficulty=difficulty).count()

def getCountCardsNotStudied(deckID):
    '''
    Returns the number of cards in the given deck that have not been studied (do not have a dificulty set)
    '''
    return Card.objects.filter(Deck_ID=deckID).exclude(Difficulty__isnull=False).count()

def getCountCardsInDeck(deckID):
    '''
    Returns the number of cards in a given deck
    '''
    return Card.objects.filter(Deck_ID=deckID).count()

def getListOfDecksWithKeyword(keyword, userId):
    return Deck.objects.exclude(Public=False).filter(Tags__iregex=r'.*{0}.*'.format(escape(keyword))).exclude(User_ID=userId)

def getSetOfPublicDecksMatching(keywords, userId):
    '''
    Takes a list of keywords and returns a set of deck objects that match one or more of the keyword arguments
    '''
    matchingDecks = set()
    for keyword in keywords:
        matchingDecks = matchingDecks.union(getPublicDecksMatching(keyword, userId))
    return matchingDecks

def getPublicDecksMatching(keyword, userId):
    '''
    Takes a single keyword and finds all the decks that match it and returns the results in a set
    '''
    matchingDecks = getListOfDecksWithKeyword(keyword, userId)
    setOfDecks = set()
    for deck in matchingDecks:
        setOfDecks.add(deck)
    return setOfDecks
