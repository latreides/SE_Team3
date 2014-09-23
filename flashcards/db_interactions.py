from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from flashcards.models import *

'''
Creates a new deck object given a name for the deck and the userID for the user who is creating the deck
and returns the new deck as an object of type deck
'''
def CreateDeck(userID, deckName):
	try:
		userObj = User.objects.get(id=userID)
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
			backImageObj = Image.objects.get(Image_ID = backImageID)
		except (ValueError, ObjectDoesNotExist):
			print "The ID provided for the back image id does not exist in the image table."
	else: 
		backImageObj = None
		
	if frontImageID != None:
		try:
			frontImageObj = Image.objects.get(Image_ID = frontImageID)
		except (ValueError, ObjectDoesNotExist):
			print "The ID provided for the front image id does not exist in the image table."
	else:
		frontImageObj = None
	
	try:
		DeckObj = Deck.objects.get(Deck_ID = deckID)
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
	
