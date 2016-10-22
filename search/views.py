"""
Logic related to searching fridge & global recipes lives.
"""

from django.shortcuts import render


def search_results(request):
    # Temporary: to pass response 200 and resolving of url tests
    ingredients = request.GET.get('q')
    if ingredients:
        ingredients = request.GET.get('q').split()
        ingredients = [ingredient.strip() for ingredient in ingredients]

    content = {
        'ingredients': ingredients
    }
    
    return render(request, 'search/search_results.html', content)
