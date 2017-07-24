import re
from string import capwords

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from ingredients.models import Ingredient, Unit


DEFAULT_IMAGE_LOCATION = 'recipes/no-image.jpg'


def user_directory_path(instance, filename):
    return f'user_{instance.author.id}/{filename}'


class Recipe(models.Model):
    """    Model that represents recipes.    """

    CUISINES = (
        ('us', 'American'),
        ('au', 'Australian'),
        ('br', 'Brazilian'),
        ('cr', 'Caribbean'),
        ('cn', 'Chinese'),
        ('ph', 'Filipino'),
        ('fr', 'French'),
        ('de', 'German'),
        ('gr', 'Greek'),
        ('in', 'Indian'),
        ('id', 'Indonesian'),
        ('it', 'Italian'),
        ('jp', 'Japanese'),
        ('kr', 'Korean'),
        ('lb', 'Lebanese'),
        ('mx', 'Mexican'),
        ('th', 'Thai'),
        ('sc', 'Scottish'),
        ('za', 'South African'),
        ('es', 'Spanish'),
        ('ot', 'Other'),
    )

    author = models.ForeignKey(User)
    title = models.CharField(max_length=100, null=False)
    description = models.TextField(max_length=250, null=False, blank=False)
    steps = models.TextField(max_length=3000, null=False, blank=False)
    cuisine = models.CharField(max_length=2, choices=CUISINES, default='ot', blank=False, null=False)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    date = models.DateTimeField(editable=False)
    views = models.PositiveIntegerField(default=0)
    slug = models.SlugField()
    image = models.ImageField(upload_to='recipes/', blank=True, default=DEFAULT_IMAGE_LOCATION)

    def save(self, *args, **kwargs):
        """
        Date is updated only when model is saved.

        Unique (user-friendly, hence 2) slug is assigned upon creation.

        Steps/description is populated if no values are provided.
        """

        if not self.id:
            self.date = timezone.now()

            # Could be done in templates. However, perhaps better to save
            # once, rather than evaluating it over and over again upon
            # accessing the template?
            if not self.steps:
                self.steps = 'No steps provided. Time to get creative!'
            if not self.description:
                self.description = 'No description provided.'

            i = 2  # user-friendly; if we find something, there are 2 instances
            slug = slugify(self.title)
            while Recipe.objects.filter(slug=slug):
                slug = f'{slug}-{i}'
                i += 1
            self.slug = slug
            self.title = capwords(self.title)

        return super(Recipe, self).save(*args, **kwargs)

    def step_list(self):
        return re.split(r'[\n\r]+', self.steps)

    def get_absolute_url(self):
        return reverse('recipes:recipe_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


# Note: there are rating packages for Django, but more fun to create it from 0.
class Rating(models.Model):
    """ Model representing ratings that can be made. """

    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.OneToOneField(User)
    recipe = models.ForeignKey(Recipe, blank=False, null=False)
    date = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        """ Date is updated only when model is saved """

        if not self.id:
            self.date = timezone.now()
        return super(Rating, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.user}\'s {str(self.recipe)} rating: {self.stars}'


class RecipeIngredient(models.Model):
    """ Model representing ingredients in the recipe. Quantity is a must! """

    recipe = models.ForeignKey(Recipe)
    ingredient = models.ForeignKey(Ingredient)
    unit = models.ForeignKey(Unit, blank=False, null=False)
    quantity = models.FloatField(validators=[MinValueValidator(0)], blank=False, null=False)

    class Meta:
        unique_together = ('recipe', 'ingredient')

    def __str__(self):
        return f'{self.ingredient} in {self.recipe}'
