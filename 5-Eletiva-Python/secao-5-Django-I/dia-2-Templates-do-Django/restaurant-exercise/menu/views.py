from django.shortcuts import render, get_object_or_404
from menu.models import Recipe
from django.http import Http404


def index(request):
    contexto = {
        'recipes': Recipe.objects.all()
    }
    return render(request, 'home.html', contexto)


def recipe_details(request, recipe_id):
    try:
        recipe = get_object_or_404(Recipe, id=recipe_id)
        return render(request, 'recipe_details.html', {'recipe': recipe})
    except Http404:
        return render(request, '404.html')


def delete_recipe(request, recipe_id):
    try:
        recipe = get_object_or_404(Recipe, id=recipe_id)
        recipe_name = recipe.name
        recipe.delete()
        return render(
            request, 'delete_recipe.html', {'recipe_name': recipe_name}
        )
    except Http404:
        return render(request, '404.html')
