# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0012_auto_20160818_2308'),
    ]

    operations = [
        migrations.AddField(
            model_name='fridge',
            name='visible',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
