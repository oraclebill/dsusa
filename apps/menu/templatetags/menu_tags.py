from django import template
from menu import menus

register = template.Library()


@register.inclusion_tag('menu/menu.html', takes_context=True)
def menu(context, menu_name):
    return {
        'current': context['request'].path,
        'menu': menus[menu_name](),
    }


@register.filter
def startswith(a, b):
    return a.startswith(b)


@register.filter
def iterable(l):
    return hasattr(l, '__iter__')
