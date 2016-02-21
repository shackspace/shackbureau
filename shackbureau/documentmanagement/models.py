from os import path
from tempfile import TemporaryDirectory
from subprocess import call
from shutil import copyfile
from django.template.loader import get_template
from django.template import Context
from django.utils.text import slugify
from django.core.files import File
from django.db import models
from django.conf import settings


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

    def generate_document(self, template=None, files=None, context=None):
        if template is None:
            template = self.template
        if context is None:
            context = Context(self.__dict__)

        tempdirectory = TemporaryDirectory()

        base_filename = slugify(self.description)
        tex_file = path.join(tempdirectory.name, "{}.tex".format(base_filename))

        with open(tex_file, 'w') as tex:
            tex.write(get_template(template).render(context))

        for template_file in self.template_files:
            src = path.join(settings.BASE_DIR, template_file)
            dest = path.join(tempdirectory.name, path.basename(src))
            copyfile(src, dest)

        call(['pdflatex', '-interaction nonstopmode', tex_file], cwd=tempdirectory.name)
        pdf_file = path.join(tempdirectory.name, "{}.pdf".format(base_filename))

        if path.isfile(pdf_file):
            with open(pdf_file, 'rb') as pdf:
                self.data_file.save("{}.pdf".format(base_filename), File(pdf))

        tempdirectory.cleanup()

    def save(self, *args, **kwargs):
        if not self.data_file or self.update_document:
            self.update_document = False
            self.generate_document()
        return super().save(*args, **kwargs)


class Letter(Document):
    class Meta:
        ordering = ('-created', )

    document_type = "letter"
    template = "documentmanagement/letter.tex"
    template_files = ('static/img/logo_shack_brightbg.pdf', )

    address = models.TextField()
    date = models.DateField(max_length=255)
    place = models.CharField(max_length=255, default="Stuttgart")
    subject = models.CharField(max_length=255)
    opening = models.CharField(max_length=255, default="Sehr geehrte Damen und Herren,")
    content = models.TextField()
    closing = models.CharField(max_length=255, default="Mit freundlichen Grüßen")
    signature = models.CharField(max_length=255, default="Der Vorstand")

    def save(self, *args, **kwargs):
        if not self.data_file or self.update_document:
            context_dict = dict(self.__dict__)
            context_dict['address'] = context_dict['address'].strip().replace('\r\n', '\\\\\r\n')
            self.update_document = False
            self.generate_document(context=Context(context_dict))
        return super().save(*args, **kwargs)
