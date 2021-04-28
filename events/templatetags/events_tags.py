from django import template
from events.models import Event

register = template.Library()


@register.simple_tag()
def get_count(event):
    return (event.visitors.all()).count()

# @register.simple_tag()
# def get_user