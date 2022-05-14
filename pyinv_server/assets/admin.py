from django.contrib import admin

from .models import AssetModel, Manufacturer


class AssetModelAdmin(admin.ModelAdmin):
    list_display = ["name", "manufacturer", "is_container"]
    list_filter = ["is_container"]
    search_fields = ["name", "manufacturer__name", "notes"]


class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ["name"]


admin.site.register(AssetModel, AssetModelAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
