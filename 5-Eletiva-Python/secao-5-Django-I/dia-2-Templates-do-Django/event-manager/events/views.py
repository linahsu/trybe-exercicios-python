from django.shortcuts import render


def index(request):
    context = {"company": "Trybe"}
    return render(request, 'home.html', context)


def about(request):
    return render(request, 'about.html')