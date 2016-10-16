"""
Logic related to searching fridge Ų global recipes lives.
"""

from django.shortcuts import render


def search_results(request):
    content = {}
    return render(request, 'search/search_results.html', content)
