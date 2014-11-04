# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0006_auto_20141022_0508'),
    ]

    operations = [
        migrations.AddField(
            model_name='deck',
            name='Times_Cloned',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='deck',
            name='Theme',
            field=models.CharField(default=b'BlankWhite.png', max_length=32, choices=[(b'Blank White', b'BlankWhite.png'), (b'Index Card', b'IndexCard.png'), (b'Film Strip', b'FilmStrip.png'), (b'Scroll', b'Scroll.png'), (b'Parchment', b'Parchment.png'), (b'White Scroll', b'WhiteScroll.png')]),
        ),
    ]
