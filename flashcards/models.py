from django.db import models
from django.conf import settings
'''
Deck is a database table that stores information specific to a single deck
    Deck_ID- (Primary Key) Integer value assigned when deck is created
    User_ID- (Foreign Key) ID of the user who created the deck
    Name- User chosen name of the deck of flashcards
    Create_Date- Date which the deck was created
    Accessed_Date- Last time the deck was used
'''
class Deck(models.Model):
    User_ID = models.ForeignKey(settings.AUTH_USER_MODEL)
    Name = models.CharField(max_length = 100)
    Create_Date = models.DateTimeField()
    Accessed_Date = models.DateTimeField(blank=True, null=True)
    Public = models.BooleanField(default=False)

    #Return the Decks name as the text for the object
    def __unicode__(self):
        return self.Name

    class Meta:
        app_label = 'flashcards'

'''
Image is a database table that contains an ID for an image used for referencing in the card
table, and then the path to where the image is stored on the server
    Image_ID- (Primary Key) Integer assigned to card when it is stored
    Image_Path- The path to the image file on the server
'''
class Image(models.Model):
    Image_Path = models.CharField(max_length = 200)

    #Return the image records path as the text for the object
    def __unicode__(self):
        return self.Image_Path

    class Meta:
        app_label = 'flashcards'

'''
Card is a database table that stores information specific to a single flash card
    Card_ID- (Primary Key) Integer assigned value for a card when it is created
    Deck_ID- (Foreign Key) ID referencing the deck that the card is part of
    Front/Back_Text- Text to display on the the corresponding side of the card
    Front/Back_Img_ID- (Foreign Key) ID referencing the ID of the image to display
    Difficulty- User rated difficulty of the current card
    Last_Attempted- The most recent time the card was attempted by the user
    Two_Sided- A boolean value hloding whether the card can be displayed with either
    side forward
'''
class Card(models.Model):
    Deck_ID = models.ForeignKey(Deck)
    Front_Text = models.TextField(blank=True, null=True)
    Back_Text = models.TextField(blank=True, null=True)
    Front_Img_ID = models.ForeignKey('Image', related_name = 'Front_Image', blank=True, null=True)
    Back_Img_ID = models.ForeignKey('Image', related_name = 'Back_Image', blank=True, null=True)
    Difficulty = models.IntegerField(blank=True, null=True)
    Last_Attempted = models.DateTimeField(blank=True, null=True)
    Two_Sided = models.BooleanField(default=False)
    Categories = models.TextField(null=True)

    #Return the Cards front side text as the text for the object
    def __unicode__(self):
        return str(self.id)
    
    class Meta:
        app_label = 'flashcards'
