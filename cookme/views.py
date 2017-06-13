"""
Test suite to ensure that views work correctly.
"""

import urllib.parse

import mistune
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse
from django.shortcuts import render, HttpResponseRedirect

from fridge.models import Fridge
from recipes.models import Recipe
from search.forms import SearchForm
from utilities.search_helpers import encode


def home(request):
    """
    Quick and dirty way of implementing a home view that has a fridge.
    """

    content = dict()
    user = request.user
    if user.is_authenticated:
        fridge = Fridge.objects.get_or_create(user=user)[0]
        user_additions = (Recipe.objects.filter(author=user)
                          .order_by('-date')[:4])

        content = {
            'user': user,
            'fridge': fridge,
            'user_additions': user_additions,
        }

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            url = reverse('search:search_results')
            q = form.cleaned_data['q']
            if q:
                query = encode(q)
                # Is encoding needed? I think django does it by default? But
                # when testing, django complains that response does not
                # redirect to a string one would expect with full encoding.
                # url += '?q=' + "+".join(term.strip() for term in q.split())
                url += '?q=' + urllib.parse.quote_plus(query)
            return HttpResponseRedirect(url)
    else:
        form = SearchForm()

    # Most popular, oldest ones at the top (if two recipes have equal views)
    most_popular = Recipe.objects.all().order_by('-views', 'date')[:4]
    # Most recent is shown first (though same date unlikely)
    most_recent = Recipe.objects.all().order_by('-date', '-views')[:4]

    content['form'] = form
    content['most_popular'] = most_popular
    content['most_recent'] = most_recent

    return render(request, 'home/home.html', content)


def register(request):
    """
    Extremely simple registration. Much better alternatives:
        - AllAuth
        - django-registration.
    However, this is mainly for practice project. Also, registration is only
    important to get the fridge. Email, social accounts, etc do not matter, as
    the app is not designed to scale or to be a serious competitor to proper
    websites.
    """

    # Don't want a registered user accessing the view.
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            redirect = request.POST.get('next', '/')
            return HttpResponseRedirect(redirect)
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


def about(request):
    """
    A view of About page. The page contains information about the website, 
    which is taken from a README.md file on GitHub. 
    
    At the moment, local version is used, but preferably a remote resource 
    should be used, as it is doubtful that README file will be on the server. 
    If it will, local one would be more reliable/faster.
    """

    with open("README.md", "r") as f:
        data = f.read()
        text = mistune.markdown(data)
        text = text.replace('../../', 'https://github.com/vilisimo/cookme/')
        text = f'<div class="about">{text}</div>'

    context = {
        'text': text,
    }

    return render(request, 'home/about.html', context)
