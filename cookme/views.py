"""
Test suite to ensure that views work correctly.
"""

from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, HttpResponseRedirect

from fridge.models import Fridge


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
            return HttpResponseRedirect(reverse('home'))
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})
