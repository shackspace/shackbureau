from tempfile import TemporaryDirectory
from os import path
from datetime import datetime
from django.utils.text import slugify
from django.core.files import File
from django.db import models
from django.conf import settings
from .utils import pdflatex


class Document(models.Model):
    class Meta:
        ordering = ('-created', )
        abstract = True

    document_type = ""
    templat = None
    additional_files = None

    description = models.CharField(max_length=127, help_text="will be used for filename")

    def upload_to(self, filename):
        if self.document_type:
            return 'documentmanagement_{}/{}'.format(self.document_type, filename)
        else:
            return 'documentmanagement/{}'.format(filename)

    data_file = models.FileField(upload_to=upload_to)
    last_update_of_data_file = models.DateTimeField(blank=True, null=True)
    update_document = models.BooleanField(
        default=False,
        help_text="If you want to update the document after the first save you have to set this."
    )
    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,)

    def save_document(self):
        tempdirectory = TemporaryDirectory()
        document = self.generate_document(tempdirectory.name)
        if document:
            with open(document, 'rb') as f:
                self.data_file.save(path.basename(document), File(f))
                self.last_update_of_data_file = datetime.now()
        tempdirectory.cleanup()

    def generate_document(self, tempdirectory):
        return pdflatex(base_filename=slugify(self.description),
                        template=self.template,
                        context=self.__dict__,
                        tempdirectory=tempdirectory,
                        additional_files=self.additional_files
                        )

    def save(self, *args, **kwargs):
        if not self.data_file or self.update_document:
            self.update_document = False
            self.save_document()
        return super().save(*args, **kwargs)

    def __str__(self):
        if self.document_type:
            return "{} {}".format(self.document_type, self.description)
        return "Document {}".format(self.description)


class Letter(Document):
    class Meta:
        ordering = ('-date', )

    document_type = "letter"
    template = 'documentmanagement/letter.tex'
    additional_files = (('static/img/logo_shack_brightbg.pdf', 'img/logo_shack_brightbg.pdf'), )

    address = models.TextField()
    date = models.DateField()
    place = models.CharField(max_length=255, default="Stuttgart")
    subject = models.CharField(max_length=255)
    opening = models.CharField(max_length=255, default="Sehr geehrte Damen und Herren,")
    content = models.TextField(help_text="You can write LaTeX here!")
    closing = models.CharField(max_length=255, default="Mit freundlichen Grüßen")
    signature = models.CharField(max_length=255, default="Der Vorstand")


class DonationReceipt(Document):
    class Meta:
        ordering = ('-date', )

    document_type = "donationreceipt"
    template = 'documentmanagement/donationreceipt.tex'
    additional_files = (('static/img/logo_shack_brightbg.pdf', 'img/logo_shack_brightbg.pdf'), )

    address_of_donator = models.TextField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    day_of_donation = models.DateField()
    donation_type = models.CharField(
        choices=(('benefits', 'Sachzuwendungen'),
                 ('allowance in money', 'Geldzuwendungen')),
        default='allowance in money',
        max_length=25
    )
    is_waive_of_charge = models.BooleanField(
        default=False,
        help_text="Es handelt sich um den Verzicht auf Erstattung von Aufwendungen"
    )
    description_of_benefits = models.TextField(
        null=True, blank=True,
        help_text="Genaue Bezeichnung der Sachzuwendung mit Alter, Zustand, Kaufpreis usw"
    )
    is_from_business_assets = models.BooleanField(
        default=False,
        help_text="Die Sachzuwendung stammt nach den Angaben des Zuwendenden aus dem Betriebsvermögen. Die Zuwendung wurde nach dem Wert der Entnahme (ggf. mit dem niedrigeren gemeinen Wert) und nach der Umsatzsteuer, die auf die Entnahme entfällt, bewertet."
    )
    is_from_private_assets = models.BooleanField(
        default=False,
        help_text="Die Sachzuwendung stammt nach den Angaben des Zuwendenden aus dem Privatvermögen"
    )
    no_information_about_origin = models.BooleanField(
        default=False,
        help_text="Der Zuwendende hat trotz Aufforderung keine Angaben zur Herkunft der Sachzuwendung gemacht."
    )
    has_documents_of_value = models.BooleanField(
        default=False,
        help_text="Geeignete Unterlagen, die zur Wertermittlung gedient haben, z. B. Rechnung, Gutachten, liegen vor."
    )
    date = models.DateField()
    place = models.CharField(max_length=255, default="Stuttgart")
    no_signature = models.BooleanField(default=True)


class DataProtectionAgreement(Document):
    class Meta:
        ordering = ('-date', )
    document_type = "dataprotectionagreement"
    template = 'documentmanagement/data_protection_agreement.tex'
    additional_files = (('static/img/logo_shack_brightbg.pdf', 'img/logo_shack_brightbg.pdf'), )

    address = models.TextField()
    date = models.DateField()
    place = models.CharField(max_length=255, default="Stuttgart")
