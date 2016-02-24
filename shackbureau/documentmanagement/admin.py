from django.contrib import admin
from reversion import VersionAdmin

from .models import Letter, DonationReceipt


@admin.register(Letter)
class LetterAdmin(VersionAdmin):
    list_display = ('date', 'description', 'subject', 'address',)
    list_display_links = list_display
    search_fields = ('decription', 'address', 'content', 'subject')
    readonly_fields = ('data_file',
                       'last_update_of_data_file',
                       'modified',
                       'created',
                       'created_by',)
    date_hierarchy = 'date'

    def save_model(self, request, obj, form, change):
        if not getattr(obj, 'created_by', False):
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)


@admin.register(DonationReceipt)
class DonationReceiptAdmin(VersionAdmin):
    list_display = ('date', 'day_of_donation', 'description', 'donation_type',
                    'address_of_donator', 'description_of_benefits', 'data_file')
    list_display_links = list_display
    search_fields = ('decription', 'address_of_donation', 'description_of_benefits')
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
    date_hierarchy = 'date'

    def save_model(self, request, obj, form, change):
        if not getattr(obj, 'created_by', False):
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)

    class Media:
        js = ("js/donation_receipt_admin.js",)
