from django.contrib import admin
from reversion import VersionAdmin
from .models import CashTransaction


@admin.register(CashTransaction)
class CashTransactionAdmin(VersionAdmin):
    list_display = ("transaction_id", "transaction_date", "description", 'transaction_sum', 'account_sum',
                    "coin_001", "coin_002", "coin_005", "coin_010", "coin_020", "coin_050",  "coin_100", "coin_200",
                    "bill_005", "bill_010", "bill_020", "bill_050", "bill_100", "bill_200", "bill_500")
    list_display_links = list_display

    readonly_fields = ("transaction_sum", "account_sum", "transaction_id", "modified", "created_by", "created")

    def save_model(self, request, obj, form, change):
        if not getattr(obj, 'created_by', False):
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)
