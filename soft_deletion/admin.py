from django.contrib import admin
from admin_confirm import AdminConfirmMixin
from admin_confirm.admin import confirm_action

from control.models import Control, Questionnaire
from logs.actions import add_log_entry
from utils.file import delete_control_folder


def find_parent_control(obj):
    if isinstance(obj, Control):
        return obj
    if isinstance(obj, Questionnaire):
        return obj.control
    return obj

def undelete(modeladmin, request, queryset):
    for item in queryset:
        item.undelete()
        add_log_entry(verb='admin undeleted', session_user=request.user, obj=item, target=item)

@confirm_action
def soft_delete(modeladmin, request, queryset):
    for item in queryset:
        item.soft_delete()
        parent = find_parent_control(item)
        if isinstance(parent, Control):
            delete_control_folder(parent.reference_code)
        add_log_entry(verb='admin soft deleted', session_user=request.user, obj=item, target=parent)


undelete.short_description = "Re-activate seleted items - undelete"
soft_delete.short_description = "Deactivate selected items - soft delete"
soft_delete.allowed_permissions = ['soft_delete']

class IsActiveFilter(admin.SimpleListFilter):
    title = 'active'
    parameter_name = 'active'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Yes'),
            ('no', 'No'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'yes':
            return queryset.filter(deleted_at__isnull=True)
        elif value == 'no':
            return queryset.filter(deleted_at__isnull=False)
        return queryset


class SoftDeletedAdmin(AdminConfirmMixin, object):
    actions = [soft_delete, undelete]

    def is_active(self, instance):
        return not instance.is_deleted()
    is_active.boolean = True
    is_active.short_description = "active"

    def get_list_display(self, request):
        return super().get_list_display(request) + ('deleted_at', 'is_active')

    def get_readonly_fields(self, request, obj=None):
        return super().get_readonly_fields(request, obj) + ('deleted_at',)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_soft_delete_permission(self, request, obj=None):
        return True
