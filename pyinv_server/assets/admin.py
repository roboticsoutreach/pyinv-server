from django.contrib import admin

from .models import AssetCode, AssetModel, Manufacturer


class AssetCodeAdmin(admin.ModelAdmin):
    list_display = ["code", "code_type"]
    list_filter = ["code_type"]
    search_fields = ["code"]


class AssetModelAdmin(admin.ModelAdmin):
    list_display = ["name", "manufacturer", "is_container"]
    list_filter = ["is_container"]
    search_fields = ["name", "manufacturer__name", "notes"]


class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ["name"]


admin.site.register(AssetCode, AssetCodeAdmin)
admin.site.register(AssetModel, AssetModelAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
