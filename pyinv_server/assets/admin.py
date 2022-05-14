from django.contrib import admin

from .models import Manufacturer


class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ["name"]


admin.site.register(Manufacturer, ManufacturerAdmin)
