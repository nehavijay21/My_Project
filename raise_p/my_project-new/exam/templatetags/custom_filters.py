from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Returns the value from a dictionary for the given key."""
    return dictionary.get(key, 0)  # Default to 0 if key is not found
