from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import AssetCode, AssetModel, Manufacturer


class AssetCodeAdmin(admin.ModelAdmin):
    list_display = ["code", "code_type"]
    list_filter = ["code_type"]
    search_fields = ["code"]


class AssetModelAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "manufacturer", "is_container"]
    list_filter = ["is_container"]
    search_fields = ["name", "manufacturer__name", "notes"]


class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ["name"]


class PyInvAdminSite(admin.AdminSite):
    site_header = 'PyInv Administration'
    site_title = 'PyInv Administration'
    index_title = 'PyInv Admin Panel'


admin_site = PyInvAdminSite()
admin_site.register(AssetCode, AssetCodeAdmin)
admin_site.register(AssetModel, AssetModelAdmin)
admin_site.register(Manufacturer, ManufacturerAdmin)
admin_site.register(User, UserAdmin)
