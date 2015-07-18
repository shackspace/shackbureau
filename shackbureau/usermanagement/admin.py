from django.contrib import admin
from .models import Member
from .forms import MemberForm


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("member_id", 'is_active', "name", "surname", 'is_underaged')
    list_display_links = list_display
    search_fields = ("member_id", "name", "surname", "nickname")
    list_filter = ("payment_type", "is_underaged", 'is_active', )
    readonly_fields = ('member_id', 'modified', 'created', 'created_by')
    form = MemberForm
    actions = None

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)
