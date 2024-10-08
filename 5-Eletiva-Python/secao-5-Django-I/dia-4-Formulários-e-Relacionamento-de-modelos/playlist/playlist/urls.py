from django.urls import path
from playlist.views import music, singer, index


urlpatterns = [
    path("", index, name="home-page"),
    path("musics", music, name="musics-page"),
    path("singers", singer, name="singers-page"),
]
