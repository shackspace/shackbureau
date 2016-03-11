from os import path, mkdir
from subprocess import call
from shutil import copyfile
from django.template.loader import get_template
from django.template import Context
from django.utils.text import get_valid_filename
from django.conf import settings


def pdflatex(base_filename, template, context, tempdirectory, additional_files=None):
    base_filename = get_valid_filename(base_filename)
    tex_file = path.join(tempdirectory, "{}.tex".format(base_filename))
    with open(tex_file, 'w') as tex:
        tex.write(get_template(template).render(Context(context)))

    if additional_files:
        for additional_file in additional_files:
            needed_dir = path.join(tempdirectory, path.dirname(additional_file[1]))
            if not path.isdir(needed_dir):
                mkdir(needed_dir)
            copyfile(path.join(settings.BASE_DIR, additional_file[0]),
                     path.join(tempdirectory, additional_file[1]))

    call(['pdflatex', '-interaction', 'nonstopmode', tex_file], cwd=tempdirectory)

    # return path.join(tempdirectory, "{}.tex".format(base_filename))

    pdf_file = path.join(tempdirectory, "{}.pdf".format(base_filename))
    if path.isfile(pdf_file):
        return pdf_file

    log_file = path.join(tempdirectory, "{}.log".format(base_filename))
    if path.isfile(log_file):
        return log_file
    return None
