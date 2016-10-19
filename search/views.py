"""
Logic related to searching fridge Ų global recipes lives.
"""

from django.shortcuts import render


def results(request):
    content = {}
    return render(request, 'search/results.html', content)
