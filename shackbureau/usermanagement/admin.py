from django.contrib import admin
from reversion import VersionAdmin

from .models import Member, AccountTransaction, Membership
from .forms import MemberForm
from django.contrib import messages


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 1
#            'membership_type',
#            'membership_fee_monthly',
#            'membership_fee_interval',


@admin.register(Member)
class MemberAdmin(VersionAdmin):
    list_display = ("member_id", 'is_active', "name", "surname",
                    'is_underaged')
    list_display_links = list_display
    search_fields = ("member_id", "name", "surname", "nickname")
    list_filter = ("payment_type", "is_underaged", 'is_active', )
    readonly_fields = ('member_id',
                       'modified',
                       'created',
                       'created_by',
                       'is_registration_to_mailinglists_sent')
    inlines = [
        MembershipInline,
    ]
    form = MemberForm
    actions = None
    history_latest_first = True

    def save_model(self, request, obj, form, change):
        if not getattr(obj, 'created_by', False):
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        return False



@admin.register(AccountTransaction)
class AccountTransactionAdmin(VersionAdmin):
    # FIXME: add daterangefilter for booking_date, due_date
    list_display = ("member", 'booking_date', "booking_type",
                    "transaction_type", 'amount')
    list_filter = ("member", )
    actions = None

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        # claims are always negative. all others are positive
        original_amount = obj.amount
        obj.amount = abs(obj.amount)
        if obj.booking_type == 'claim':
            obj.amount = obj.amount * -1
        if obj.amount != original_amount:
            messages.add_message(request, messages.WARNING,
                                 # FIXME: translate:
                                 'Vorzeichen des Betrages wurde geändert. Penner.')

        if not getattr(obj, 'created_by', False):
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)
