# coding=UTF-8

from django import template

register = template.Library()

@register.filter
def tagify(value):
    """Puts tags in an interview text to format it"""
    new_value = ''
    paragraphs = value.split("\n")
    for paragraph in paragraphs:
        if '<a class="part"' in paragraph:
            new_value += '<div align="center">' + paragraph + "</div><hr class=\"part\"/>\n"
        else:
            try:
                sep = paragraph.index(': ', 1)
                # Only colons close to the beginning
                if sep < 30:
                    paragraph = '<label>' + paragraph[:sep] + '</label>' + paragraph[sep:]
            except:
                pass
            new_value += '<p class="jp">' + paragraph + "</p>\n"
    return new_value
