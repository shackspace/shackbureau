from django.contrib import admin
from reversion.admin import VersionAdmin
from django.contrib import messages
from ajax_select import make_ajax_form

from .models import (
    AccountTransaction,
    BankTransactionLog,
    BankTransactionUpload,
    Member,
    Membership,
    MemberSpecials,
    MemberDocument,
    MemberDocumentTag,
    MemberTrackingCode,
    Balance,
    Memberlog
)
from .forms import MemberForm, MemberSpecialsForm, MembershipInlineFormset


class OrderMemberByNameMixin():
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "member":
            kwargs["queryset"] = Member.objects.order_by('surname', 'name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Membership)
class MembershipAdmin(OrderMemberByNameMixin, VersionAdmin):
    search_fields = ("member__member_id",
                     "member__name",
                     "member__surname",
                     "member__nickname")
    list_display = ("member",
                    "valid_from",
                    'membership_type',
                    "membership_fee")
    list_filter = ("member",
                   'member__is_active',
                   "membership_fee_monthly",
                   "membership_type")
    readonly_fields = ('modified',
                       'created',
                       'created_by',)
    form = make_ajax_form(Membership, {'member': 'member'})

    def membership_fee(self, obj):
        return "{} / {}".format(obj.membership_fee_monthly,
                                obj.membership_fee_interval,)

    def save_model(self, request, obj, form, change):
        if not getattr(obj, 'created_by', False):
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        return False


class MembershipInline(admin.TabularInline):
    model = Membership
    formset = MembershipInlineFormset
    extra = 0
    min_num = 1
    fields = ('valid_from', 'membership_type',
              'membership_fee_monthly', 'membership_fee_interval',)
    readonly_fields = ('modified',
                       'created',
                       'created_by',)


class MemberDocumentInline(admin.TabularInline):
    model = MemberDocument
    extra = 0
    fields = ('description',
              'data_file',
              'comment',
              'tag',
              )
    readonly_fields = ('modified',
                       'created',
                       'created_by',)


class MemberSpecialInline(admin.TabularInline):
    model = MemberSpecials
    extra = 0
    min_num = 1
    exclude = ('created_by', 'is_registration_to_key_mailinglist_sent')


class BalanceInline(admin.TabularInline):
    model = Balance
    extra = 0
    min_num = 1
    fields = ('balance',
              'accumulated_balance',
              'year')
    readonly_fields = ('balance',
                       'accumulated_balance',
                       'year')

    def get_queryset(self, request):
        from django.db.models import Max, F
        qs = super().get_queryset(request)
        year_max = qs.aggregate(Max('year')).get('year__max')
        return qs.filter(year=year_max)


@admin.register(Member)
class MemberAdmin(VersionAdmin):
    list_display = ("member_id", 'is_active', "name", "surname", 'nickname',
                    'is_underaged', 'join_date', 'leave_date')
    list_display_links = list_display
    search_fields = ("=member_id", "name", "surname", "nickname", "email")
    list_filter = ("payment_type", "is_underaged", 'is_active',
                   "membership__membership_fee_monthly",
                   "membership__membership_type", "memberdocument__tag")
    readonly_fields = ('member_id',
                       'copy_paste_information',
                       'modified',
                       'created',
                       'created_by',
                       'is_registration_to_mailinglists_sent',
                       'is_welcome_mail_sent',
                       'is_cancellation_mail_sent_to_cashmaster',
                       'is_revoke_memberspecials_mail_sent',
                       )
    fieldsets = [
        ('', {
            'fields': ['comment',
                       'join_date']}),
        ('Address', {
            'fields': ['form_of_address',
                       'name',
                       'nickname',
                       'surname',
                       'address1', 'address2',
                       'zip_code', 'city',
                       'country',
                       'is_underaged',
                       'email',
                       'date_of_birth', ]
        }),
        ('Payment', {
            'fields': ['payment_type',
                       'iban_issue_date',
                       'iban_fullname',
                       'iban_address',
                       'iban_zip_code',
                       'iban_city',
                       'iban_country',
                       'iban_institute',
                       'bic',
                       'iban', ]
        }),
        ('Memberstate', {
            'fields': ['is_active',
                       'leave_date',
                       'is_cancellation_confirmed', ]
        }),
        ('Additional information', {
            'fields': readonly_fields,
            'classes': ['collapse', ]}),
    ]

    inlines = [
        MembershipInline,
        MemberDocumentInline,
#        MemberSpecialInline,
#        BalanceInline,
    ]
    form = MemberForm
    actions = None
    history_latest_first = True
    save_on_top = True

    def copy_paste_information(self, obj):
        copy_paste = ["{} {}".format(obj.name, obj.surname),
                      obj.address1 or "",
                      obj.address2 or "",
                      "{} {}".format(obj.zip_code, obj.city),
                      "",
                      obj.email or "",
                      "",
                      obj.iban_fullname or "",
                      obj.iban_address or "",
                      "{} {}".format(obj.iban_zip_code, obj.iban_city),
                      obj.iban_country or "",
                      obj.bic or "",
                      obj.iban or ""]
        return "\n".join(copy_paste)

    def save_formset(self, request, form, formset, change):
        formset.save(commit=False)
        for f in formset.forms:
            obj = f.instance
            if isinstance(obj, Membership):
                if not getattr(obj, 'valid_from', False):
                    # don't save if valid_from is not set
                    continue
            if isinstance(obj, MemberDocument):
                if not getattr(obj, 'data_file', False):
                    # don't save without a file
                    continue
            if not getattr(obj, 'created_by', False):
                obj.created_by = request.user
            obj.save()
            formset.save_m2m()

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
    search_fields = ('member__name', 'member__surname', 'member__nickname', 'payment_reference', 'transaction_hash')
    actions = None
    readonly_fields = ('modified',
                       'created',
                       'created_by',)
    date_hierarchy = 'due_date'
    form = make_ajax_form(AccountTransaction, {'member': 'member'})

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        # claims are always negative. all others are positive
        original_amount = obj.amount
        obj.amount = abs(obj.amount)
        if obj.booking_type in ('claim', 'charge back'):
            obj.amount = obj.amount * -1
        if obj.amount != original_amount:
            messages.add_message(request, messages.WARNING,
                                 # FIXME: translate:
                                 'Vorzeichen des Betrages wurde geändert. Penner.')

        if not getattr(obj, 'created_by', False):
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)


@admin.register(BankTransactionUpload)
class BankTransactionUploadAdmin(VersionAdmin):
    list_display = ("data_file", "data_type", "status", "created")
    list_display_links = list_display
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
class BankTransactionLogAdmin(OrderMemberByNameMixin, VersionAdmin):
    def add_transaction(self):
        if not self.is_matched and not self.is_resolved:
            return u"<a target='_blank' href='/admin/usermanagement/accounttransaction/add/?" + \
                "amount={}&booking_date={}&due_date={}&payment_reference={}%0A{}&booking_type=deposit'>Add Transaction</a>" \
                .format(self.amount, self.booking_date, self.booking_date, self.reference, self.transaction_owner)
        else:
            return ''
    add_transaction.short_description = ''
    add_transaction.allow_tags = True

    list_display = ('is_matched', 'is_resolved', 'booking_date', 'member',
                    "reference", "amount", add_transaction, "upload")
    list_display_links = list_display
    list_filter = ("is_matched", 'is_resolved', "score")
    search_fields = ("reference", "member__name", "member__surname")
    readonly_fields = ('modified',
                       'created',
                       'created_by',)
    actions = ['set_resolved_entry']
    date_hierarchy = 'booking_date'
    form = make_ajax_form(BankTransactionLog, {'member': 'member'})

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
class MemberSpecialsAdmin(OrderMemberByNameMixin, VersionAdmin):
    list_display = ('member', 'is_keyholder', 'has_matomat_key', 'has_snackomat_key', 'has_laser_key',
                    'has_metro_card', 'has_selgros_card', 'has_shack_iron_key', 'has_safe_key',
                    'has_loeffelhardt_account', 'signed_DSV',)
    list_display_links = list_display
    list_filter = ('member__is_active', 'is_keyholder', 'has_matomat_key', 'has_snackomat_key',
                   'has_laser_key', 'has_metro_card', 'has_selgros_card', 'has_shack_iron_key',
                   'has_safe_key', 'has_loeffelhardt_account', 'signed_DSV',
                   'is_registration_to_key_mailinglist_sent',)
    search_fields = ("member__name", "member__surname", "member__nickname", "member__member_id")
    actions = None
    readonly_fields = ('is_registration_to_key_mailinglist_sent',
                       'modified',
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
class MemberTrackingCodeAdmin(VersionAdmin):
    list_display = ('member', 'uuid', 'validated')
    list_display_links = list_display
    list_filter = ('validated', 'member__is_active')
    search_fields = ("member__name", "member__surname", "member__nickname", "member__email")
    form = make_ajax_form(MemberTrackingCode, {'member': 'member'})

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(MemberDocument)
class MemberDocumentAdmin(OrderMemberByNameMixin, VersionAdmin):
    list_display = ('data_file', 'member', 'description', 'tag_list')
    list_display_links = list_display
    list_filter = ('tag', 'member', )
    search_fields = ('member__name', 'member__surname', 'member__nickname', 'member__member_id',
                     'data_file', 'description', 'comment')
    readonly_fields = ('modified',
                       'created',
                       'created_by',)
    filter_horizontal = ('tag', )
    form = make_ajax_form(MemberDocument, {'member': 'member'})

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if not getattr(obj, 'created_by', False):
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)


@admin.register(MemberDocumentTag)
class MemberDocumentTagAdmin(VersionAdmin):
    list_display = ('tag', )
    list_display_links = list_display
    search_fields = ('tag', )
    readonly_fields = ('modified',
                       'created',
                       'created_by',)

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if not getattr(obj, 'created_by', False):
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)


@admin.register(Balance)
class BalanceAdmin(OrderMemberByNameMixin, VersionAdmin):
    list_display = ('year', 'member', 'balance', 'accumulated_balance')
    list_display_links = list_display
    search_fields = ('member__name', 'member__surname', 'member__nickname')
    readonly_fields = ('balance',
                       'accumulated_balance',
                       'modified',
                       'created',
                       'created_by',)
    list_filter = ('year', 'member')
    form = make_ajax_form(Balance, {'member': 'member'})

    def save_model(self, request, obj, form, change):
        if not getattr(obj, 'balance', False):
            obj.balance = 0
        if not getattr(obj, 'created_by', False):
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Memberlog)
class MemberlogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'member', 'action', 'detail')
    list_display_links = list_display
    search_fields = ('member__name', 'member__surname', 'member__nickname', 'action', 'detail')
    readonly_fields = ('modified',
                       'created',
                       'created_by',)
    list_filter = ('timestamp', 'action', 'member')
    date_hierarchy = 'timestamp'
    form = make_ajax_form(Memberlog, {'member': 'member'})

    def save_model(self, request, obj, form, change):
        if not getattr(obj, 'balance', False):
            obj.balance = 0
        if not getattr(obj, 'created_by', False):
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        return False
