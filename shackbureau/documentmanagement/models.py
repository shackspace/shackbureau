from django.db import models
from django.conf import settings


class Document(models.Model):
    class Meta:
        ordering = ('-created', )
        abstract = True

    document_type = ""

    description = models.CharField(max_length=255)

    data_file = models.FileField(upload_to='documentmanagement_{}'.format(document_type))

    update_document = models.BooleanField(default=False)

    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,)

    def generate_document(self, template=None, files=None):
        pass

    def save(self, *args, **kwargs):
        if not self.data_file or self.update_document:
            self.generate_ducument()
        return super().save(*args, **kwargs)


class Letter(Document):
    class Meta:
        ordering = ('-date', )

    address = models.TextField()
    date = models.DateField(max_length=255, auto_now_add=True)
    place = models.CharField(max_length=255, default="Stuttgart")
    subject = models.CharField(max_length=255)
    opening = models.CharField(max_length=255, default="Sehr geehrte Damen und Herren,")
    content = models.TextField()
    closing = models.CharField(max_length=255, default="Mit freundlichen Grüßen")
    signature = models.CharField(max_length=255, default="Der Vorstand")
