# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0005_auto_20141006_0132'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='Categories',
        ),
        migrations.AddField(
            model_name='deck',
            name='Tags',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='deck',
            name='Theme',
            field=models.CharField(default=b'Blank', max_length=32, choices=[(b'Blank White', b'BlankWhite.png'), (b'Index Card', b'IndexCard.png'), (b'Film Strip', b'FilmStrip.png'), (b'Scroll', b'Scroll.png'), (b'Parchment', b'Parchment.png'), (b'White Scroll', b'WhiteScroll.png')]),
            preserve_default=True,
        ),
    ]
