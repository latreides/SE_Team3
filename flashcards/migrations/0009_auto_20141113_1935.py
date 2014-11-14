# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0008_card_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='Weight',
            field=models.IntegerField(default=1),
        ),
    ]
