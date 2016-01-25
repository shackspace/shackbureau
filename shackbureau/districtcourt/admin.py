from django.contrib import admin
from reversion import VersionAdmin

from .models import Debitor


@admin.register(Debitor)
class MemberAdmin(VersionAdmin):
    list_display = ("debitor_id", "districtcourt", "record_token", "record_token_line_2", "name", "is_done",)
    list_display_links = list_display
    search_fields = list_display
    list_filter = ("districtcourt", "is_done", "debitor_id")
    readonly_fields = ('debitor_id',
                       'modified',
                       'created',
                       'created_by',)

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if not getattr(obj, 'created_by', False):
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)
