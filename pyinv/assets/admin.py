from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .models import (
    Asset,
    AssetCode,
    AssetEvent,
    AssetModel,
    ChangeSet,
    Manufacturer,
    Node,
)


class AssetCodeAdmin(admin.ModelAdmin):
    list_display = ["code", "code_type"]
    list_filter = ["code_type"]
    search_fields = ["code"]


class AssetEventAdmin(admin.ModelAdmin):
    list_display = ["asset", "changeset"]
    list_filter = ["changeset__user"]


class ChangeSetAdmin(admin.ModelAdmin):
    list_display = ["timestamp", "user", "comment"]
    list_filter = ["timestamp", "user"]
    search_fields = ["comment"]


class AssetAdmin(admin.ModelAdmin):
    list_display = ["__str__", "asset_model", "node"]
    list_filter = ["asset_model"]


class AssetModelAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "manufacturer", "is_container"]
    list_filter = ["is_container"]
    search_fields = ["name", "manufacturer__name"]


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
admin_site.register(AssetEvent, AssetEventAdmin)
admin_site.register(Asset, AssetAdmin)
admin_site.register(AssetModel, AssetModelAdmin)
admin_site.register(ChangeSet, ChangeSetAdmin)
admin_site.register(Manufacturer, ManufacturerAdmin)
admin_site.register(Node, NodeAdmin)
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)
