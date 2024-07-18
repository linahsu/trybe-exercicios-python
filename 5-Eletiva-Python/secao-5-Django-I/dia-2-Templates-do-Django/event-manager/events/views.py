from django.shortcuts import render
from events.models import Event
from django.shortcuts import get_object_or_404


def index(request):
    context = {
        "company": "Trybe",
        "events": Event.objects.all(),
    }
    return render(request, 'home.html', context)


def about(request):
    return render(request, 'about.html')


def event_details(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'details.html', {'event': event})