from django.urls import path
from menu.views import index, recipe_details

urlpatterns = [
    path("", index, name='home-page'),
    path("recipes/<int:recipe_id>", recipe_details, name='details-page')
]
