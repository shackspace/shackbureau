from django.contrib import admin
from reversion import VersionAdmin

from .models import (
    AccountTransaction,
    BankTransactionLog,
    BankTransactionUpload,
    Member,
    Membership,
    MemberSpecials,
    MemberTrackingCode,
)
from .forms import MemberForm, MemberSpecialsForm, MembershipInlineFormset
from django.contrib import messages


class OrderMemberByNameMixin():
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "member":
            kwargs["queryset"] = Member.objects.order_by('surname', 'name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Membership)
class MembershipAdmin(OrderMemberByNameMixin, VersionAdmin):
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
    formset = MembershipInlineFormset
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
    search_fields = ("member_id", "name", "surname", "nickname", "email")
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
        for f in formset.forms:
            obj = f.instance
            if not getattr(obj, 'valid_from', False):
                # don't save if valid_from is not set
                continue
            if not getattr(obj, 'created_by', False):
                obj.created_by = request.user
            obj.save()

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if not getattr(obj, 'created_by', False):
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)

    class Media:
        js = ("js/member_admin.js",)


@admin.register(AccountTransaction)
class AccountTransactionAdmin(OrderMemberByNameMixin, VersionAdmin):
    # FIXME: add daterangefilter for booking_date, due_date
    list_display = ('member', 'booking_date', 'due_date', 'booking_type',
                    'transaction_type', 'amount', 'payment_reference')
    list_filter = ('transaction_type', 'booking_type', 'booking_date', 'due_date', 'member', )
    search_fields = ('member__name', 'member__surname', 'member__nickname', 'payment_reference', )
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
class BankTransactionLogAdmin(OrderMemberByNameMixin, admin.ModelAdmin):
    def add_transaction(self):
        if not self.is_matched and not self.is_resolved:
            return u"<a target='_blank' href='/admin/usermanagement/accounttransaction/add/?" + \
                "amount={}&booking_date={}&payment_reference={}%0A{}&booking_type=deposit'>Add Transaction</a>".format(
                    self.amount, self.booking_date, self.reference, self.transaction_owner)
        else:
            return ''
    add_transaction.short_description = ''
    add_transaction.allow_tags = True

    list_display = ('is_matched', 'is_resolved', 'member', "reference", add_transaction, "upload")
    list_display_links = list_display
    list_filter = ("is_matched", 'is_resolved', "score")
    search_fields = ("member__name", "member__surname")
    readonly_fields = ('modified',
                       'created',
                       'created_by',)
    actions = ['set_resolved_entry']

    def set_resolved_entry(self, request, queryset):
        rows_updated = queryset.update(is_resolved=True)
        if rows_updated == 1:
            message_bit = "1 entry was"
        else:
            message_bit = "%s entries were" % rows_updated
        self.message_user(request, "%s successfully marked as resolved." % message_bit)
    set_resolved_entry.short_description = "Set entries to resolved"

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if not getattr(obj, 'created_by', False):
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)


@admin.register(MemberSpecials)
class MemberSpecialsAdmin(admin.ModelAdmin):
    list_display = ('member', 'is_keyholder', 'has_matomat_key', 'has_snackomat_key', 'has_metro_card',
                    'has_selgros_card', 'has_shack_iron_key', 'has_safe_key', 'has_loeffelhardt_account',
                    'signed_DSV',)
    list_display_links = list_display
    list_filter = ('is_keyholder', 'has_matomat_key', 'has_snackomat_key', 'has_metro_card',
                   'has_selgros_card', 'has_shack_iron_key', 'has_safe_key', 'has_loeffelhardt_account',
                   'signed_DSV',)
    search_fields = ("member__name", "member__surname", "member__nickname")
    actions = None
    readonly_fields = ('modified',
                       'created',
                       'created_by',)
    form = MemberSpecialsForm

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if not getattr(obj, 'created_by', False):
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)

    class Media:
        js = ("js/memberspecials_admin.js",)


@admin.register(MemberTrackingCode)
class MemberTrackingCodeAdmin(admin.ModelAdmin):
    list_display = ('member', 'uuid', 'validated')
    list_filter = ('validated',)
    search_fields = ("member__name", "member__surname", "member__nickname")
