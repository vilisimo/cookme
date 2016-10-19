"""
Logic related to searching fridge & global recipes lives.
"""

from django.shortcuts import render


def search_results(request):
    # request.GET.get['q'] to get query string
    content = {}
    return render(request, 'search/search_results.html', content)
