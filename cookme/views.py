"""
Test suite to ensure that views work correctly.
"""

from django.shortcuts import render
from fridge.models import Fridge


def home(request):
    """
    Quick and dirty way of implementing a home view that has a fridge.

    :param request: default request object.
    :return:        default render object.
    """

    content = dict()

    user = request.user
    if user.is_authenticated:
        fridge = Fridge.objects.get_or_create(user=user)[0]

        content = {
            'user': user,
            'fridge': fridge,
        }

    return render(request, 'base.html', content)
