# tracker/templatetags/string_utils.py
from django import template

register = template.Library()

@register.filter
def split(value, delimiter=','):
    """Split string by comma (or any delimiter) and clean whitespace"""
    if not value:
        return []
    return [item.strip() for item in str(value).split(delimiter) if item.strip()]