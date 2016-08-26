from django.shortcuts import render

from fridge.models import Fridge


def home(request):
    """
    Quick and dirty way of implementing a view that has a user...

    :param request:
    :return:
    """

    user = request.user
    fridge = Fridge.objects.get(user=user)

    content = {
        'user': user,
        'fridge': fridge,
    }

    return render(request, 'base.html', content)