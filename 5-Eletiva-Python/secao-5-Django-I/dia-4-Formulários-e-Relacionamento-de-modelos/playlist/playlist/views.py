from django.shortcuts import render
from playlist.forms import CreateMusicForm, CreateSingerForm


def music(request):
    form = CreateMusicForm()
    context = {"form": form}
    return render(request, 'music.html', context)


def singer(request):
    form = CreateSingerForm()
    context = {"form": form}
    return render(request, 'singer.html', context)
