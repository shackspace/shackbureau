from os import path
from subprocess import call
from shutil import copyfile
from django.template.loader import get_template
from django.template import Context
from django.utils.text import slugify
from django.conf import settings


def generate_letter(letter, tempdirectory):
    base_filename = slugify(letter.description)
    tex_file = path.join(tempdirectory, "{}.tex".format(base_filename))

    context_dict = dict(letter.__dict__)
    context_dict['address'] = context_dict['address'].strip().replace('\r\n', '\\\\\r\n')

    context = Context(context_dict)

    with open(tex_file, 'w') as tex:
        tex.write(get_template('documentmanagement/letter.tex').render(context))

    copyfile(path.join(settings.BASE_DIR, 'static/img/logo_shack_brightbg.pdf'),
             path.join(tempdirectory, 'logo_shack_brightbg.pdf'))

    call(['pdflatex', '-interaction nonstopmode', tex_file], cwd=tempdirectory)
    pdf_file = path.join(tempdirectory, "{}.pdf".format(base_filename))

    if path.isfile(pdf_file):
        return pdf_file, "{}.pdf".format(base_filename)
    return None, None
