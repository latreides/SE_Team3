# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flashcards', '0007_auto_20141103_1821'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='Weight',
            field=models.DecimalField(default=1, max_digits=1, decimal_places=0),
            preserve_default=True,
        ),
    ]
