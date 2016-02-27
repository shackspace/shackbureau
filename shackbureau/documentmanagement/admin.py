from django.contrib import admin
from reversion import VersionAdmin

from .models import Letter, DonationReceipt, DataProtectionAgreement
from .forms import DonationReceiptForm


@admin.register(Letter)
class LetterAdmin(VersionAdmin):
    list_display = ('date', 'description', 'subject', 'address',)
    list_display_links = list_display
    search_fields = ('description', 'address', 'content', 'subject')
    readonly_fields = ('data_file',
                       'last_update_of_data_file',
                       'modified',
                       'created',
                       'created_by',)
    fieldsets = [
        (None, {
            'fields': ('description', )
        }),
        ('Document', {
            'fields': ('update_document', 'data_file', 'last_update_of_data_file')
        }),
        ('Content', {
            'fields': ('address', 'date', 'place', 'subject', 'opening', 'content', 'closing', 'signature')
        }),
        ('Meta information', {
            'fields': ('modified', 'created', 'created_by')
        })
    ]
    date_hierarchy = 'date'
    actions = None
    history_latest_first = True
    save_on_top = True

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if not getattr(obj, 'created_by', False):
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)


@admin.register(DonationReceipt)
class DonationReceiptAdmin(VersionAdmin):
    list_display = ('date', 'day_of_donation', 'description', 'donation_type',
                    'address_of_donator', 'amount', 'description_of_benefits')
    list_display_links = list_display
    search_fields = ('description', 'address_of_donator', 'description_of_benefits')
    list_filter = ('donation_type',
                   'is_waive_of_charge',
                   'is_from_business_assets',
                   'is_from_private_assets',
                   'no_information_about_origin',
                   'has_documents_of_value')
    readonly_fields = ('data_file',
                       'last_update_of_data_file',
                       'modified',
                       'created',
                       'created_by',)
    fieldsets = [
        (None, {
            'fields': ('description', )
        }),
        ('Document', {
            'fields': ('update_document', 'data_file', 'last_update_of_data_file')
        }),
        ('Donation information', {
            'fields': ('address_of_donator',
                       'amount',
                       'day_of_donation',
                       'donation_type',
                       'is_waive_of_charge',
                       'description_of_benefits',
                       'is_from_business_assets',
                       'is_from_private_assets',
                       'no_information_about_origin',
                       'has_documents_of_value',)
        }),
        ('Signature', {
            'fields': ('date',
                       'place',
                       'no_signature')
        }),
        ('Meta information', {
            'fields': ('modified', 'created', 'created_by')
        })
    ]
    date_hierarchy = 'date'
    form = DonationReceiptForm
    actions = None
    history_latest_first = True
    save_on_top = True

    def save_model(self, request, obj, form, change):
        if not getattr(obj, 'created_by', False):
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        return False

    class Media:
        js = ("js/donation_receipt_admin.js",)


@admin.register(DataProtectionAgreement)
class DataProtectionAgreementAdmin(VersionAdmin):
    list_display = ('date', 'description', 'address',)
    list_display_links = list_display
    search_fields = ('description', 'address')
    readonly_fields = ('data_file',
                       'last_update_of_data_file',
                       'modified',
                       'created',
                       'created_by',)
    fieldsets = [
        (None, {
            'fields': ('description', )
        }),
        ('Document', {
            'fields': ('update_document', 'data_file', 'last_update_of_data_file')
        }),
        ('Content', {
            'fields': ('address', 'place', 'date')
        }),
        ('Meta information', {
            'fields': ('modified', 'created', 'created_by')
        })
    ]
    date_hierarchy = 'date'
    actions = None
    history_latest_first = True
    save_on_top = True

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if not getattr(obj, 'created_by', False):
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)
