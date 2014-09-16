from django.db import models

'''
User is a database Table that will store information specific to a user
'''
class User(models.Model):
    User_ID = models.AutoField(primary_key=True)
    Email = models.CharField(max_length = 50)
    Password = models.CharField(max_length = 32)
    Login_ID = models.CharField(max_length = 50)

    #Return the users login ID as the text for the object
    def __unicode__(self):
        return self.Login_ID

    class Meta:
        app_label = 'flashcards'

'''
Deck is a database table that stores information specific to a single deck
'''
class Deck(models.Model):
    Deck_ID = models.AutoField(primary_key=True)
    User_ID = models.ForeignKey(User)
    Name = models.CharField(max_length = 100)
    Create_Date = models.DateTimeField()
    Accessed_Date = models.DateTimeField()

    #Return the Decks name as the text for the object
    def __unicode__(self):
        return self.Name

    class Meta:
        app_label = 'flashcards'

'''
Image is a database table that contains an ID for an image used for referencing in the card
table, and then the path to where the image is stored on the server
'''
class Image(models.Model):
    Image_ID = models.AutoField(primary_key=True)
    Image_Path = models.CharField(max_length = 200)

    #Return the image records path as the text for the object
    def __unicode__(self):
        return self.Image_Path

    class Meta:
        app_label = 'flashcards'

'''
Card is a database table that stores information specific to a single flash card
'''
class Card(models.Model):
    Card_ID = models.AutoField(primary_key=True)
    Deck_ID = models.ForeignKey(Deck)
    Front_Text = models.TextField()
    Back_Text = models.TextField()
    Front_Img_ID = models.ForeignKey('Image', related_name = 'Front_Image')
    Back_Img_ID = models.ForeignKey('Image', related_name = 'Back_Image')
    Difficulty = models.IntegerField()
    Last_Attempted = models.DateTimeField()
    Two_Sided = models.BooleanField()

    #Return the Cards front side text as the text for the object
    def __unicode__(self):
        return self.Front_Text

    class Meta:
        app_label = 'flashcards'
