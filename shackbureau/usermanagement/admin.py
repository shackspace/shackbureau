from django.contrib import admin
from reversion import VersionAdmin

from .models import (
    AccountTransaction,
    BankTransactionLog,
    BankTransactionUpload,
    Member,
    Membership,
)
from .forms import MemberForm
from django.contrib import messages


@admin.register(Membership)
class MembershipAdmin(VersionAdmin):
    search_fields = ("member__member_id",
                     "member__name",
                     "member__surname")
    list_display = ("member",
                    "valid_from",
                    'membership_type',
                    "membership_fee"
    )
    list_filter = ("member",
                   'member__is_active',
                   "membership_fee_monthly",
                   "membership_type")
    readonly_fields = ('modified',
                       'created',
                       'created_by',)

    def membership_fee(self, obj):
        return "{} / {}".format(obj.membership_fee_monthly,
                                obj.membership_fee_interval,)

    def save_model(self, request, obj, form, change):
        if not getattr(obj, 'created_by', False):
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 1
    fields = ('valid_from', 'membership_type',
              'membership_fee_monthly', 'membership_fee_interval',)
    readonly_fields = ('modified',
                       'created',
                       'created_by',)


@admin.register(Member)
class MemberAdmin(VersionAdmin):
    list_display = ("member_id", 'is_active', "name", "surname",
                    'is_underaged')
    list_display_links = list_display
    search_fields = ("member_id", "name", "surname", "nickname")
    list_filter = ("payment_type", "is_underaged", 'is_active',
                   "membership__membership_fee_monthly",
                   "membership__membership_type")
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

    def save_formset(self, request, form, formset, change):
        formset.save(commit=False)
        print("AAAAA")
        for f in formset.forms:
            obj = f.instance
            print("A")
            if not getattr(obj, 'valid_from', False):
                print("B")
                print(obj.valid_from)
                continue
            if not getattr(obj, 'created_by', False):
                obj.created_by = request.user
            obj.save()

    def has_delete_permission(self, request, obj=None):
        return False

    class Media:
        js = ("js/member_admin.js",)


@admin.register(AccountTransaction)
class AccountTransactionAdmin(VersionAdmin):
    # FIXME: add daterangefilter for booking_date, due_date
    list_display = ("member", 'booking_date', 'due_date', "booking_type",
                    "transaction_type", 'amount', 'payment_reference')
    list_filter = ("member", )
    actions = None
    readonly_fields = ('modified',
                       'created',
                       'created_by',)

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


@admin.register(BankTransactionUpload)
class BankTransactionUploadAdmin(admin.ModelAdmin):
    actions = None
    readonly_fields = ('modified',
                       'created',
                       'created_by',)

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if not getattr(obj, 'created_by', False):
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)


@admin.register(BankTransactionLog)
class BankTransactionLogAdmin(admin.ModelAdmin):
    def add_transaction(self):
        if self.is_matched and self.is_resolved:
            return u"<a target='_blank' href='/admin/usermanagement/accounttransaction/add/?" + \
                "amount={}&booking_date={}&payment_reference={}&booking_type=deposit'>Add Transaction</a>".format(
                    self.amount, self.booking_date, self.reference)
        else:
            return ''
    add_transaction.short_description = ''
    add_transaction.allow_tags = True

    list_display = ('is_matched', 'member', "reference", add_transaction, "upload")
    list_display_links = list_display
    list_filter = ("is_matched", "score")
    search_fields = ("member__name", "member__surname")
    actions = None
    readonly_fields = ('modified',
                       'created',
                       'created_by',)

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if not getattr(obj, 'created_by', False):
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)
