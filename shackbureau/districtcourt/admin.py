from django.contrib import admin
from reversion import VersionAdmin

from .models import Debitor, DistrictcourtAccountTransaction, DistrictcourtBalance


@admin.register(Debitor)
class DebitorAdmin(VersionAdmin):
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


@admin.register(DistrictcourtAccountTransaction)
class DistrictcourtAccountTransactionAdmin(VersionAdmin):
    list_display = ("debitor", 'due_date', 'booking_date', 'amount', 'payment_reference')
    list_display_links = list_display
    search_fields = (
        # "debitor__record_token",
        # "debitor__record_token_line2",
        "debitor__name",
        'payment_reference',
    )

    list_filter = ("debitor__districtcourt", 'debitor__is_done', "debitor",)

    readonly_fields = ('modified',
                       'created',
                       'created_by',)

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if not getattr(obj, 'created_by', False):
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)


@admin.register(DistrictcourtBalance)
class DistrictcourtBalanceAdmin(VersionAdmin):
    list_display = ("debitor", 'balance')
    list_display_links = list_display
    search_fields = (
        # "debitor__record_token",
        # "debitor__record_token_line2",
        "debitor__name",
    )

    list_filter = ("debitor__districtcourt", 'debitor__is_done', "debitor",)

    readonly_fields = ('balance',
                       'modified',
                       'created',
                       'created_by',)

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if not getattr(obj, 'created_by', False):
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)
