from django import template

register = template.Library()

@register.filter
def get_dict_value(key, dictionary):
    if str(key) in dictionary:
        return dictionary[str(key)]
    return None
