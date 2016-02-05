from django.contrib import admin
from reversion import VersionAdmin
from .models import CashTransaction


@admin.register(CashTransaction)
class CashTransactionAdmin(VersionAdmin):
    list_display = ("transaction_id", "transaction_date", "transaction_date_id", "is_stored_by_account",
                    "description", 'transaction_sum', 'account_sum',
                    "transaction_coin_001", "transaction_coin_002", "transaction_coin_005", "transaction_coin_010",
                    "transaction_coin_020", "transaction_coin_050",  "transaction_coin_100", "transaction_coin_200",
                    "transaction_bill_005", "transaction_bill_010", "transaction_bill_020", "transaction_bill_050",
                    "transaction_bill_100", "transaction_bill_200", "transaction_bill_500")
    list_display_links = list_display

    readonly_fields = ("transaction_sum", "account_sum", "transaction_id", "modified", "created_by", "created")

    def save_model(self, request, obj, form, change):
        if not getattr(obj, 'created_by', False):
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)

    class Media:
        js = ("js/cash_transaction_admin.js", )
