"""
Test suite to ensure that views work correctly.
"""

import urllib.parse

from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, HttpResponseRedirect

from fridge.models import Fridge
from search.forms import SearchForm


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

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            url = reverse('search:search_results')
            q = form.cleaned_data['q']
            if q:
                # Is encoding needed? I think django does it by default? But
                # when testing, django complains that response does not
                # redirect to a string one would expect with full encoding.
                # url += '?q=' + "+".join(term.strip() for term in q.split())
                url += '?q=' + urllib.parse.quote_plus(q)
            return HttpResponseRedirect(url)
    else:
        form = SearchForm()

    content['form'] = form

    return render(request, 'base.html', content)


def register(request):
    """
    View allowing users to register.

    Extremely simple registration. Much better alternatives would be AllAuth
    or django-registration. However, this is mainly for practice purposes.
    Also, registration is only important to get the fridge. Email, social
    accounts, etc does not matter, as the app is not designed to scale or to
    be a serious competitor to proper websites.
    """

    # Don't want a registered user accessing the view.
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password1'])
            login(request, user)
            redirect = request.POST.get('next', '/')
            return HttpResponseRedirect(redirect)
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})
