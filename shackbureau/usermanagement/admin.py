from django.contrib import admin
from reversion import VersionAdmin

from .models import Member
from .forms import MemberForm


@admin.register(Member)
class MemberAdmin(VersionAdmin):
    list_display = ("member_id", 'is_active', "name", "surname",
                    'is_underaged')
    list_display_links = list_display
    search_fields = ("member_id", "name", "surname", "nickname")
    list_filter = ("payment_type", "is_underaged", 'is_active', )
    readonly_fields = ('member_id', 'modified', 'created', 'created_by')
    form = MemberForm
    actions = None
    history_latest_first = True

    def save_model(self, request, obj, form, change):
        if not getattr(obj, 'created_by', False):
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        return False
