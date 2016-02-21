from django.contrib import admin
from reversion import VersionAdmin

from documentmanagement.models import Letter


@admin.register(Letter)
class LetterAdmin(VersionAdmin):
    list_display = ('date', 'description', 'address',)
    list_display_links = list_display
    search_fields = ('decription', 'address', 'content', 'subject')
    readonly_fields = ('data_file',
                       'modified',
                       'created',
                       'created_by',)
    date_hierarchy = 'date'

    def save_model(self, request, obj, form, change):
        if not getattr(obj, 'created_by', False):
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)
