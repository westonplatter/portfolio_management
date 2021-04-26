import json

from django import template

register = template.Library()


@register.filter
def loadjson(data):
    return json.loads(data)
