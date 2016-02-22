from tempfile import TemporaryDirectory
from django.core.files import File
from django.db import models
from django.conf import settings
from .views import generate_letter


class Document(models.Model):
    class Meta:
        ordering = ('-created', )
        abstract = True

    document_type = ""
    template = ""
    template_files = []

    description = models.CharField(max_length=255)

    def upload_to(self, filename):
        if self.document_type:
            return 'documentmanagement_{}/{}'.format(self.document_type, filename)
        else:
            return 'documentmanagement/{}'.format(filename)

    data_file = models.FileField(upload_to=upload_to)

    update_document = models.BooleanField(default=False)

    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,)

    def save_document(self):
        tempdirectory = TemporaryDirectory()
        document, filename = self.generate_document(tempdirectory.name)
        print(document, filename)
        if document:
            with open(document, 'rb') as f:
                self.data_file.save(filename, File(f))
        tempdirectory.cleanup()

    def generate_document(self):
        return None, None

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

    address = models.TextField()
    date = models.DateField(max_length=255)
    place = models.CharField(max_length=255, default="Stuttgart")
    subject = models.CharField(max_length=255)
    opening = models.CharField(max_length=255, default="Sehr geehrte Damen und Herren,")
    content = models.TextField(help_text="You can write latex here")
    closing = models.CharField(max_length=255, default="Mit freundlichen Grüßen")
    signature = models.CharField(max_length=255, default="Der Vorstand")

    generate_document = generate_letter
