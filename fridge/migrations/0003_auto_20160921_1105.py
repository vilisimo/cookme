# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-21 11:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fridge', '0002_auto_20160921_0957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fridgeingredient',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ingredients.Ingredient'),
        ),
    ]
