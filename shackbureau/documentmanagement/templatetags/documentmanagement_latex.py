from num2words import num2words as lib_num2words
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def latex_newlines(value):
    return '\\\\'.join(value.strip().splitlines())


@register.filter
@stringfilter
def striped_splitlines(value):
    return [line.strip() for line in value.splitlines() if line.strip()]


@register.filter
def num2words(value, arg='en'):
    try:
        return lib_num2words(value, lang=arg)
    except TypeError:
        return value
    except NotImplementedError:
        return ""
