from django import template

register = template.Library()

@register.filter
def is_selected(value, expected):
    return str(value) == str(expected)
