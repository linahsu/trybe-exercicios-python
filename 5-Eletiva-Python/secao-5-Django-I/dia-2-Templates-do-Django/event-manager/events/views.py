from django.shortcuts import render
from events.models import Event


def index(request):
    context = {
        "company": "Trybe",
        "events": Event.objects.all(),
    }
    return render(request, 'home.html', context)


def about(request):
    return render(request, 'about.html')