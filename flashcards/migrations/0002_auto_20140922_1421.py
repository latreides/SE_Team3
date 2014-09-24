# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='Card_ID',
        ),
        migrations.RemoveField(
            model_name='deck',
            name='Deck_ID',
        ),
        migrations.RemoveField(
            model_name='image',
            name='Image_ID',
        ),
        migrations.AddField(
            model_name='card',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, default=0, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deck',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, default=None, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='image',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, default=None, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='card',
            name='Back_Img_ID',
            field=models.ForeignKey(related_name=b'Back_Image', blank=True, to='flashcards.Image'),
        ),
        migrations.AlterField(
            model_name='card',
            name='Back_Text',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='Difficulty',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='Front_Img_ID',
            field=models.ForeignKey(related_name=b'Front_Image', blank=True, to='flashcards.Image'),
        ),
        migrations.AlterField(
            model_name='card',
            name='Front_Text',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='card',
            name='Last_Attempted',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='deck',
            name='Accessed_Date',
            field=models.DateTimeField(blank=True),
        ),
    ]
