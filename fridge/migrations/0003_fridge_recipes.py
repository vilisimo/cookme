# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-08 19:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_recipe_ingredients'),
        ('fridge', '0002_fridge_ingredients'),
    ]

    operations = [
        migrations.AddField(
            model_name='fridge',
            name='recipes',
            field=models.ManyToManyField(to='recipes.Recipe'),
        ),
    ]
