from os import path, mkdir
from subprocess import call
from shutil import copyfile
from django.template.loader import get_template
from django.template import Context
from django.utils.text import slugify
from django.conf import settings


def pdflatex(base_filename, template, context, tempdirectory, additional_files=None):
    base_filename = slugify(base_filename)
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


def generate_letter(letter, tempdirectory):
    base_filename = slugify(letter.description)
    context_dict = dict(letter.__dict__)

    return pdflatex(base_filename=base_filename,
                    template='documentmanagement/letter.tex',
                    context=context_dict,
                    tempdirectory=tempdirectory,
                    additional_files=(('static/img/logo_shack_brightbg.pdf', 'img/logo_shack_brightbg.pdf'), )
                    )


def generate_donation_receipt(donationreceipt, tempdirectory):
    base_filename = slugify(donationreceipt.description)
    context_dict = dict(donationreceipt.__dict__)

    return pdflatex(base_filename=base_filename,
                    template='documentmanagement/donationreceipt.tex',
                    context=context_dict,
                    tempdirectory=tempdirectory,
                    additional_files=(('static/img/logo_shack_brightbg.pdf', 'img/logo_shack_brightbg.pdf'), )
                    )


def generate_data_protection_agreement(dataprotectionagreement, tempdirectory):
    base_filename = slugify(dataprotectionagreement.description)
    context_dict = dict(dataprotectionagreement.__dict__)

    return pdflatex(base_filename=base_filename,
                    template='documentmanagement/data_protection_agreement.tex',
                    context=context_dict,
                    tempdirectory=tempdirectory,
                    additional_files=(('static/img/logo_shack_brightbg.pdf', 'img/logo_shack_brightbg.pdf'), )
                    )
