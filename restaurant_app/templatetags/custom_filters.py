from django import template

register = template.Library()

@register.filter
def get_dict_value(key, dictionary):
    if str(key) in dictionary:
        return dictionary[str(key)]
    return None


@register.filter
def multiply(v1, v2):
    return round(v1*v2, 2)
