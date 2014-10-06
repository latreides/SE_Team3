# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('flashcards', '0002_auto_20140925_2013'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_History',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Accessed_Date', models.DateTimeField()),
                ('Deck_ID', models.ForeignKey(to='flashcards.Deck')),
                ('User_ID', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='userhistory',
            name='Deck_ID',
        ),
        migrations.RemoveField(
            model_name='userhistory',
            name='User_ID',
        ),
        migrations.DeleteModel(
            name='UserHistory',
        ),
    ]
