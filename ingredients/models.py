from string import capwords

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Ingredient(models.Model):
    """ Represents ingredients of recipes. """

    # Categories of ingredients
    INGREDIENTS = [
        ('Additive', 'Food additive'),
        ('Bread', 'Bread'),
        ('Bean', 'Bean'),
        ('Canned', 'Canned food'),
        ('Condiment', 'Condiment'),
        ('Oil', 'Cooking oil'),
        ('Eggs', 'Eggs'),
        ('Dairy', 'Dairy'),
        ('Flour', 'Flour'),
        ('Fruit', 'Fruit'),
        ('Grain', 'Grain'),
        ('Herb', 'Herb'),
        ('Meat', 'Meat'),
        ('Nut', 'Nut'),
        ('Pasta', 'Pasta'),
        ('Paste', 'Paste'),
        ('Poultry', 'Poultry'),
        ('Rice', 'Rice'),
        ('Salt', 'Salt'),
        ('Sauce', 'Sauce'),
        ('Seafood', 'Seafood'),
        ('Seed', 'Seed'),
        ('Spice', 'Spice'),
        ('Sugar', 'Sugar'),
        ('Vegetable', 'Vegetable'),
        ('Unspecified', 'Unspecified'),
    ]
    INGREDIENTS = sorted(INGREDIENTS, key=lambda x: x[1])

    name = models.CharField(max_length=250, null=False, unique=True)
    type = models.CharField(max_length=250, blank=True, null=False,
                            default='Unspecified', choices=INGREDIENTS)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        """
        Even though name is unique, slug may be not unique. For example,
        if model 1 has name ';a;' and model 2 has name ';a:'. In such a case,
        slug would be 'a' for both. Hence, slug needs to be processed before
        committing it to the database.
        """

        if not self.id:
            slug = slugify(self.name)
            i = 2
            while Ingredient.objects.filter(slug=slug):
                slug = '{slug}-{i}'
                i += 1
            self.slug = slug
            self.name = capwords(self.name)
        return super(Ingredient, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('ingredients:ingredient_detail', args=[self.slug])

    def __str__(self):
        return self.name


class Unit(models.Model):
    """ Represents quantities, such as oz, kg, ml, etc. """

    name = models.CharField(max_length=30, blank=False, null=False, unique=True)
    abbrev = models.CharField(max_length=10, blank=True, null=True)
    plural = models.CharField(max_length=20, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.abbrev
