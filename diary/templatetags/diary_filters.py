from django import template

register = template.Library()

@register.filter
def placeholder(value, arg):
    """Specify a placeholder in an HTML input widget"""
    value.field.widget.attrs['placeholder'] = arg
    return value