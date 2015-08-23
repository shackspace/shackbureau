from django import forms
from .models import Member


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
