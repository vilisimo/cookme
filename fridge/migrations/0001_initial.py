# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-12 02:18
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ingredients', '0001_initial'),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fridge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visible', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='FridgeIngredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('fridge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fridge.Fridge')),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ingredients.Ingredient')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ingredients.Unit')),
            ],
        ),
        migrations.AddField(
            model_name='fridge',
            name='ingredients',
            field=models.ManyToManyField(through='fridge.FridgeIngredient', to='ingredients.Ingredient'),
        ),
        migrations.AddField(
            model_name='fridge',
            name='recipes',
            field=models.ManyToManyField(to='recipes.Recipe'),
        ),
        migrations.AddField(
            model_name='fridge',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='fridgeingredient',
            unique_together=set([('fridge', 'ingredient')]),
        ),
    ]
