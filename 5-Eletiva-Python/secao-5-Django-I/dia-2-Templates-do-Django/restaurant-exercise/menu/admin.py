from django.contrib import admin
from menu.models import Recipe

admin.site.site_header = 'Restaurant admin panel'
admin.site.register(Recipe)
