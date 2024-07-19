from django.urls import path
from menu.views import index

urlpatterns = [
    path("", index, name='home-page'),
]
