from django.contrib import admin

from ordered_model.admin import OrderedModelAdmin

from soft_deletion.admin import SoftDeletedAdmin, IsActiveFilter

from .models import CGUItem


@admin.register(CGUItem)
class CGUItemAdmin(SoftDeletedAdmin, OrderedModelAdmin):
    list_display = ("id", "title", "slug", "order", "move_up_down_links")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("order",)
    list_filter = (IsActiveFilter,)
    search_fields = ("title", "description")
    ordering = ("order",)
