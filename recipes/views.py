from django.shortcuts import render
from django.http import HttpResponse  # DELETE LATER


# Maybe the very main page should be moved somewhere else.

def recipes(request):
    return HttpResponse("Recipes")


def test(request):
    return render(request, 'recipes/test.html', {})
