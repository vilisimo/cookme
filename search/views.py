"""
Logic related to searching fridge & global recipes lives.
"""

from django.shortcuts import render


def search_results(request):
    # request.GET.get['q'] to get query string
    ingredients = request.GET.get('q').split()
    ingredients = [ingredient.strip() for ingredient in ingredients]
    content = {
        'ingredients': ingredients
    }
    return render(request, 'search/search_results.html', content)
