from django import template
from django.utils.safestring import mark_safe
from django.utils.html import escape
import re

register = template.Library()
rx=re.compile(r'(%\([^\s\)]*\)[sd])')

@register.filter
def format_message(message):
    return mark_safe(rx.sub('<code>\\1</code>', escape(message).replace(r'\n','<br />\n')))

@register.filter
def lines_count(message):
    return 1 + sum([len(line)/50 for line in message.split('\n')])

@register.filter
def mult(a,b):
    return int(a)*int(b)
