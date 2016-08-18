# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-18 21:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_recipe_ingredients'),
    ]

    operations = [
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit', models.CharField(max_length=30)),
                ('abbrev', models.CharField(blank=True, max_length=5, null=True)),
                ('description', models.CharField(blank=True, max_length=1000, null=True)),
            ],
        ),
    ]
