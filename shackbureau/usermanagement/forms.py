from django import forms
from .models import Member, MemberSpecials
from django.utils.safestring import mark_safe


class TextInputWithActionWidget(forms.TextInput):
    # Special form element that can copy addres information from member to sepa
    def __init__(self, *args, **kwargs):
        self.action = kwargs.pop('action', '')
        self.description = kwargs.pop('description')
        super(TextInputWithActionWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        attrs['size'] = 31
        html = super(TextInputWithActionWidget, self).render(name, value, attrs=attrs)
        html += u"&nbsp;<a onclick='{action}'>{description}</a>".format(action=self.action, description=self.description)
        return mark_safe(html)


class MemberForm(forms.ModelForm):
    class Meta(object):
        model = Member
        fields = [
            'comment',
            'join_date',
            'form_of_address',
            'name',
            'nickname',
            'surname',
            'address1', 'address2',
            'zip_code', 'city',
            'country',
            'is_underaged',
            'email',
            'date_of_birth',
            'payment_type',
            'iban_issue_date',
            'iban_fullname',
            'iban_address',
            'iban_zip_code',
            'iban_city',
            'iban_country',
            'bic',
            'iban',
            'is_active',
            'leave_date',
            'is_cancellation_confirmed',
            'show_additional_information',
            # readonly
            'created_by',
        ]

    iban_fullname = forms.CharField(widget=TextInputWithActionWidget(description="copy member address",
                                                                     action="copyMemberAddressInSepa()"),
                                    required=False)
    show_additional_information = forms.BooleanField(required=False)

    def clean(self):
        cleaned_data = super(MemberForm, self).clean()
        payment_type = cleaned_data.get("payment_type")

        if payment_type == "SEPA":
            sepa_fields = ('iban_issue_date',
                           'iban_fullname',
                           'iban_address',
                           'iban_zip_code',
                           'iban_city',
                           'iban_country',
                           'bic',
                           'iban',)
            sepa_msg = "must be set if payment type is SEPA"
            for field in sepa_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, sepa_msg)

        is_active = cleaned_data.get("is_active")
        leave_date = cleaned_data.get("leave_date")
        is_cancellation_confirmed = cleaned_data.get("is_cancellation_confirmed")

        if is_active is True:
            if leave_date:
                self.add_error("leave_date", "an active member can not have a leave date")
            if is_cancellation_confirmed:
                self.add_error("is_cancellation_confirmed", "an active member can not have a confirmed cancelation")
        if is_active is False:
            if not leave_date:
                self.add_error("leave_date", "an inactive member must have a leave date")

        return cleaned_data


class MemberSpecialsForm(forms.ModelForm):
    class Meta(object):
        model = MemberSpecials
        fields = [
            'member',
            'has_matomat_key',
            'has_snackomat_key',
            'has_shack_iron_key',
            'has_safe_key',
            'has_metro_card',
            'has_selgros_card',
            'has_loeffelhardt_account',
            'signed_DSV',
            'is_keyholder',
            'ssh_public_key',
            # readonly
            'created_by',
        ]

    def clean(self):
        cleaned_data = super(MemberSpecialsForm, self).clean()
        is_keyholder = cleaned_data.get("is_keyholder")
        ssh_public_key = cleaned_data.get("ssh_public_key")

        if is_keyholder and not ssh_public_key:
            msg = "A keyholder must have a ssh public key"
            self.add_error('ssh_public_key', msg)

        return cleaned_data


class MembershipInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        # get forms that actually have valid data
        valid_from = set()
        muliple_valid_from = set()
        for form in self.forms:
            try:
                if form.cleaned_data:
                    membership_valid_from = form.cleaned_data.get("valid_from").replace(day=1)
                    if membership_valid_from in valid_from:
                        muliple_valid_from.add(membership_valid_from)
                    else:
                        valid_from.add(membership_valid_from)
            except AttributeError:
                # annoyingly, if a subform is invalid Django explicity raises
                # an AttributeError for cleaned_data
                pass
        if len(valid_from) == 0:
            raise forms.ValidationError('A member must have at least one membership')
        if muliple_valid_from:
            msg = "Multiple membeships for the same month are not allowed: " +\
                ", ".join([x.isoformat() for x in muliple_valid_from])
            raise forms.ValidationError(msg)
