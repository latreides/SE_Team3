# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('Card_ID', models.AutoField(serialize=False, primary_key=True)),
                ('Front_Text', models.TextField()),
                ('Back_Text', models.TextField()),
                ('Difficulty', models.IntegerField()),
                ('Last_Attempted', models.DateTimeField()),
                ('Two_Sided', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('Deck_ID', models.AutoField(serialize=False, primary_key=True)),
                ('Name', models.CharField(max_length=100)),
                ('Create_Date', models.DateTimeField()),
                ('Accessed_Date', models.DateTimeField()),
                ('User_ID', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('Image_ID', models.AutoField(serialize=False, primary_key=True)),
                ('Image_Path', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='card',
            name='Back_Img_ID',
            field=models.ForeignKey(related_name=b'Back_Image', to='flashcards.Image'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='Deck_ID',
            field=models.ForeignKey(to='flashcards.Deck'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='card',
            name='Front_Img_ID',
            field=models.ForeignKey(related_name=b'Front_Image', to='flashcards.Image'),
            preserve_default=True,
        ),
    ]
