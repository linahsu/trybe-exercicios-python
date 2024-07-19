from django.urls import path
from menu.views import index, recipe_details, delete_recipe

urlpatterns = [
    path("", index, name='home-page'),
    path("recipe/<int:recipe_id>", recipe_details, name='details-page'),
    path("recipe/<int:recipe_id>/delete", delete_recipe, name='delete-page'),
]
