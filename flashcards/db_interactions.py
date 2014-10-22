from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from flashcards.models import *
from datetime import datetime
from django.utils.timezone import utc

'''
Generic Helper Function for Time Zone aware now()
'''
def GetNow():
    return datetime.now().replace(tzinfo=utc)


'''
Creates a new deck object given a name for the deck and the userID for the user who is creating the deck
and returns the new deck as an object of type deck
'''
def CreateDeck(userID, deckName):
	try:
		userObj = User.objects.get(id = userID)
	except (ValueError, ObjectDoesNotExist):
		print "The given User ID does not exist in the database"

	newDeck = Deck(Name = deckName, User_ID = userObj, Create_Date=timezone.now())
	newDeck.save()
	return newDeck

'''
Creates a new card object given the deck the card belongs to, a boolean value indicating if either side of the
card can be considered the front, and optionally text or images that the card would display.
**** To link an image the image must already be in the database ****
Returns the card object that was created
'''
def CreateCard(deckID, twoSided, frontText = None, backText = None, frontImageID = None, backImageID = None):
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

'''
Creates a new image entry in the database given a path to the image on the server or web
Returns the object of type image created by the database
'''
def CreateImage(pathToImage):
	newImage = Image(Image_Path = pathToImage)
	newImage.save()
	return newImage

'''
Returns an object containing the most recent deck accessed by the user id passed into the function
'''
def GetMostRecentDeck(userID):
	return Deck.objects.order_by('-Accessed_Date')[0] if Deck.objects.filter(User_ID=userID).exclude(Accessed_Date__isnull=True).exists() else None

'''
Returns a list containing all the decks that the current user has as Deck objects
'''
def GetDecksForUser(userID):
	return Deck.objects.filter(User_ID=userID)

'''
Returns a single specific Deck
'''
def getDeck(deckID):
    return Deck.objects.get(id=deckID)

# Abstract Test Data Function, to be removed for final product.
def GetDecksForUser_test(userID):
    deckList = [\
            Deck(id=0, Name = "How to Use MemorizeMe", User_ID = userID, Create_Date = GetNow(), Accessed_Date = GetNow()), \
            Deck(id=1, Name = "My Deck", User_ID = userID, Create_Date = GetNow(), Accessed_Date = GetNow().replace(tzinfo=utc)), \
            Deck(id=2, Name = "How To Swahili with Dr. Shade", User_ID = userID, Create_Date = GetNow(), Accessed_Date = GetNow()), \
            Deck(id=3, Name = "What is Love? (Baby, Don't Hurt Me)", User_ID = userID, Create_Date = GetNow(), Accessed_Date = GetNow()), \
            Deck(id=4, Name = "Identifying Wood", User_ID = userID, Create_Date = GetNow(), Accessed_Date = GetNow()), \
            Deck(id=5, Name = "Meine Flashkarte", User_ID = userID, Create_Date = GetNow(), Accessed_Date = GetNow()), \
            Deck(id=6, Name = "Mitt Flashcard", User_ID = userID, Create_Date = GetNow(), Accessed_Date = GetNow()), \
            Deck(id=7, Name = "Mi Tarjeta de Memoria Flash", User_ID = userID, Create_Date = GetNow(), Accessed_Date = GetNow()), \
            ]
    deckList.extend(list(GetDecksForUser(userID)))
    return deckList

'''
Returns a list containing all the cards as objects belonging to the deck ID that was passed in
'''
def GetCardsForDeck(deckID):
	return Card.objects.filter(Deck_ID=deckID)

'''
Return the last time the user logged in as a string
'''
def GetLastTimeLoggedIn(userID):
        try:
		userObj = User.objects.get(id=userID)
	except (ValueError, ObjectDoesNotExist):
		print "The given User ID does not exist in the database"
	return userObj.last_login.strftime('%b-%d-%Y %I:%M:%S %p')

def GetCountCardsWithDifficulty(deckID, difficulty):
    return Card.objects.filter(Deck_ID=deckID, Difficulty=difficulty).count()

def GetCountCardsNotStudied(deckID):
    return Card.objects.filter(Deck_ID=deckID).exclude(Difficulty__isnull=False).count()
