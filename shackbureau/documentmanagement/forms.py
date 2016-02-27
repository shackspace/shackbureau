from django import forms
from .models import DonationReceipt


class DonationReceiptForm(forms.ModelForm):
    class Meta(object):
        model = DonationReceipt
        fields = [
            'description',
            'donation_type',
            'description_of_benefits',
        ]

    def clean(self):
        cleaned_data = super(DonationReceiptForm, self).clean()
        donation_type = cleaned_data.get("donation_type")
        description_of_benefits = cleaned_data.get("description_of_benefits")
        if donation_type == 'benefits' and not description_of_benefits.strip():
            msg = "Description of benefits is required"
            self.add_error('description_of_benefits', msg)
        return cleaned_data
