from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from flashcards.models import Deck, Image, Card

# Register your models here.
admin.site.register(Deck)
admin.site.register(Image)
admin.site.register(Card)

