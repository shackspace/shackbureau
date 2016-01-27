from django import forms
from .models import Member, MemberSpecials


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
            # readonly
            'created_by',
        ]
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
