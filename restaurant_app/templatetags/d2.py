from django import template

register = template.Library()

@register.filter
def get_dict_value(dictionary, key):
    if key in dictionary:
        return dictionary[key]
    return None
