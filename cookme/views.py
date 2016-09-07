from django.shortcuts import render

from fridge.models import Fridge


def home(request):
    """
    Quick and dirty way of implementing a view that has a user...

    :param request:
    :return:
    """

    content = dict()

    user = request.user
    if user.is_authenticated:
        fridge = Fridge.objects.get(user=user)

        content = {
            'user': user,
            'fridge': fridge,
        }

    return render(request, 'base.html', content)
