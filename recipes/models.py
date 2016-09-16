from django.db import models
from django.utils import timezone
from django.urls import reverse

from django.template.defaultfilters import slugify
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

from ingredients.models import Ingredient, Unit


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.author.id, filename)


class Recipe(models.Model):
    """    Model that represents recipes.    """

    author = models.ForeignKey(User)
    title = models.CharField(max_length=250, null=False)
    description = models.TextField()
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    date = models.DateTimeField(editable=False)
    views = models.PositiveIntegerField(default=0)
    slug = models.SlugField()
    image = models.ImageField(upload_to='recipes/', blank=True,
                              default='recipes/no-image.jpg')

    def save(self, *args, **kwargs):
        """
        Date is updated only when model is saved.
        Unique (user-friendly, hence 2) slug is assigned upon creation.
        """

        if not self.id:
            self.date = timezone.now()

            i = 2  # user-friendly; if we find something, there are 2 instances
            slug = slugify(self.title)
            while Recipe.objects.filter(slug=slug):
                slug = "{0}-{1}".format(slug, i)
                i += 1
            self.slug = slug

        return super(Recipe, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('recipes:recipe_detail', kwargs={'slug': self.slug})

    def __str__(self):
        if len(Recipe.objects.filter(title=self.title)) > 1:
            return "{0}-{1}".format(self.title, self.pk)
        else:
            return self.title


# Note: there are rating packages for Django, but more fun to create it from 0.
class Rating(models.Model):
    """ Model representing ratings that can be made. """

    stars = models.IntegerField(validators=[MinValueValidator(1),
                                MaxValueValidator(5)])
    user = models.OneToOneField(User)
    recipe = models.ForeignKey(Recipe, blank=False, null=False)
    date = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        """ Date is updated only when model is saved """

        if not self.id:
            self.date = timezone.now()
        return super(Rating, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user) + \
               '\'s ' + str(self.recipe) + ' rating: {0}'.format(self.stars)


class RecipeIngredient(models.Model):
    """ Model representing ingredients in the recipe. Quantity is a must! """

    recipe = models.ForeignKey(Recipe)
    ingredient = models.ForeignKey(Ingredient)
    unit = models.ForeignKey(Unit, blank=False, null=False)
    quantity = models.FloatField(blank=False, null=False)

    class Meta:
        unique_together = ('recipe', 'ingredient')

    def __str__(self):
        return "{0} in {1}".format(self.ingredient, self.recipe)
