# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-16 18:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='type',
            field=models.CharField(choices=[('Additives', 'Food additives'), ('Condiments', 'Condiments'), ('Dairy', 'Dairy'), ('Eggs', 'Eggs'), ('Flour', 'Flour'), ('Fruits', 'Fruits'), ('Grains', 'Grains'), ('Herbs', 'Herbs'), ('Meat', 'Meat'), ('Nuts', 'Nuts'), ('Oils', 'Cooking oils'), ('Pasta', 'Pasta'), ('Poultry', 'Poultry'), ('Salts', 'Salts'), ('Sauces', 'Sauces'), ('Seafood', 'Seafood'), ('Seeds', 'Seeds'), ('Spices', 'Spices'), ('Sugars', 'Sugars'), ('Vegetables', 'Vegetables')], max_length=250),
        ),
    ]
