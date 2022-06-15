from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .models import Asset, AssetCode, AssetModel, Manufacturer, Node


class AssetCodeAdmin(admin.ModelAdmin):
    list_display = ["code", "code_type"]
    list_filter = ["code_type"]
    search_fields = ["code"]


class AssetAdmin(admin.ModelAdmin):
    list_display = ["__str__", "asset_model", "state", "node"]
    list_filter = ["asset_model", "state"]


class AssetModelAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "manufacturer", "is_container"]
    list_filter = ["is_container"]
    search_fields = ["name", "manufacturer__name", "notes"]


class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ["name"]


class NodeAdmin(TreeAdmin):
    form = movenodeform_factory(Node)

    list_display = ["display_name", "node_type", "asset"]
    list_filter = ["node_type"]


class PyInvAdminSite(admin.AdminSite):
    site_header = 'PyInv Administration'
    site_title = 'PyInv Administration'
    index_title = 'PyInv Admin Panel'


admin_site = PyInvAdminSite()
admin_site.register(AssetCode, AssetCodeAdmin)
admin_site.register(Asset, AssetAdmin)
admin_site.register(AssetModel, AssetModelAdmin)
admin_site.register(Manufacturer, ManufacturerAdmin)
admin_site.register(Node, NodeAdmin)
admin_site.register(User, UserAdmin)
