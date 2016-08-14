from django.shortcuts import render
from django.http import HttpResponse  # DELETE LATER


def recipes(request):
    """
    Should show the list of recipes.
    :param request:
    :return:
    """
    return render(request, 'recipes/test.html', {})
