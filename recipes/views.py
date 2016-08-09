from django.shortcuts import render
from django.http import HttpResponse  # DELETE LATER


def recipes(request):
    return HttpResponse("Recipes")


def test(request):
    return render(request, 'recipes/test.html', {})
