from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .models import Asset, AssetCode, AssetModel, Location, Manufacturer


class AssetAdmin(admin.ModelAdmin):
    list_display = ["name", "asset_model", "state", "first_asset_code"]
    list_filter = ["asset_model", "state"]
    readonly_fields = ["created_at", "updated_at", "id"]
    search_fields = [
        "name",
        "asset_model__name",
        "asset_model__manufacturer__name",
    ]


class AssetCodeAdmin(admin.ModelAdmin):
    list_display = ["code", "code_type", "asset"]
    list_filter = ["code_type"]
    search_fields = ["code"]


class AssetModelAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "manufacturer", "is_container"]
    list_filter = ["is_container"]
    search_fields = ["name", "manufacturer__name", "notes"]


class LocationAdmin(TreeAdmin):
    form = movenodeform_factory(Location)


class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ["name"]


admin.site.register(Asset, AssetAdmin)
admin.site.register(AssetCode, AssetCodeAdmin)
admin.site.register(AssetModel, AssetModelAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
