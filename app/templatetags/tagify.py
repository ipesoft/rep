# coding=UTF-8

from django import template

register = template.Library()

@register.filter
def tagify(value):
    """Puts tags in an interview text"""
    new_value = ''
    paragraphs = value.split("\n")
    for paragraph in paragraphs:
        try:
            sep = paragraph.index(': ', 1)
            paragraph = '<label>' + paragraph[:sep] + '</label>' + paragraph[sep:]
        except:
            pass
        new_value += '<p class="jp">' + paragraph + "</p>\n"
    return new_value
