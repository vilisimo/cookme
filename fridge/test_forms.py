"""
Test suite for custom form functionality.
"""


from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.test import TestCase

from ingredients.models import Ingredient
from .forms import AddRecipeFridgeForm


class AddRecipeFormTests(TestCase):
    """ Test suite to test the AddRecipeForm """

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.potato = Ingredient.objects.create(name='Potato', type='Vegetable')
        self.tomato = Ingredient.objects.create(name='Tomato', type='Fruit')

    def test_fields_not_empty(self):
        """ Ensure that information is passed to the fields """

        data = {'author': self.user, 'title': 'test', 'description': 'test'}
        form = AddRecipeFridgeForm(data=data)

        self.assertTrue(form.is_valid())

    def test_fields_empty(self):
        """ Ensure that empty data cannot be passed """

        data = {'title': '   ', 'description': 'test'}
        form = AddRecipeFridgeForm(data=data)

        self.assertFalse(form.is_valid())

        data = {'title': 'test', 'description': ' '}
        form = AddRecipeFridgeForm(data=data)

        self.assertFalse(form.is_valid())

    def test_image_field(self):
        """ Ensure that the form can take image field """

        with open('static/test/test.png', 'rb') as image:
            data = {'title': 'test', 'description': 'testing'}
            image_data = {'image': SimpleUploadedFile(image.name, image.read())}
            form = AddRecipeFridgeForm(data=data, files=image_data)

            self.assertTrue(form.is_valid())
