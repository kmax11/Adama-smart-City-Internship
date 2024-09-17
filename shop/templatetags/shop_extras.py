from django import template

register = template.Library()

@register.filter
def times(number):
    return range(number)
@register.filter(name='subtract')
def subtract(value, arg):
    return int(value) - int(arg)