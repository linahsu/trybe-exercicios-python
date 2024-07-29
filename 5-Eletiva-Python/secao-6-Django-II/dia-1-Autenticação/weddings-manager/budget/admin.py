from django.contrib import admin
from budget.models import Vendor, Marriage, Budget


admin.site.site_header = 'Weddings Manager Admin Panel'
admin.site.register(Vendor)
admin.site.register(Marriage)
admin.site.register(Budget)
