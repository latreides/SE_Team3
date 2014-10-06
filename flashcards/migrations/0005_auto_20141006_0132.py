# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0004_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_history',
            name='Deck_ID',
        ),
        migrations.RemoveField(
            model_name='user_history',
            name='User_ID',
        ),
        migrations.DeleteModel(
            name='User_History',
        ),
        migrations.AddField(
            model_name='card',
            name='Categories',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='deck',
            name='Accessed_Date',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='deck',
            name='Public',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='card',
            name='Back_Img_ID',
            field=models.ForeignKey(related_name=b'Back_Image', blank=True, to='flashcards.Image', null=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='Back_Text',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='Difficulty',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='Front_Img_ID',
            field=models.ForeignKey(related_name=b'Front_Image', blank=True, to='flashcards.Image', null=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='Front_Text',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='Last_Attempted',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
