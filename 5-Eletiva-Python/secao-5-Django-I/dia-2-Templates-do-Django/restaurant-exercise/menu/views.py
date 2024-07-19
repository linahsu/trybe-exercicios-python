from django.shortcuts import render
from menu.models import Recipe


def index(request):
    contexto = {
        'recipes': Recipe.objects.all()
    }
    return render(request, 'home.html', contexto)
