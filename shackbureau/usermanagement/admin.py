from django.contrib import admin
from .models import Member
from .forms import MemberForm


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("member_id", "name", "surname")
    list_filter = ("member_id", )
    readonly_fields = ('member_id', )
    form = MemberForm