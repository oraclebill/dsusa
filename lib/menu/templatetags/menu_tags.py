from django import template
from menu import menus

register = template.Library()


@register.inclusion_tag('menu/menu.html', takes_context=True)
def menu(context, menu_name):
    menu_item = menus.get(menu_name, None)
    if menu_item and callable(menu_item):
        menu_item = menu_item()
    elif not menu_item:
        menu_item = '#'
    return {
        'current': context['request'].path,
        'menu': menu_item,
    }


@register.filter
def startswith(a, b):
    return a.startswith(b)


@register.filter
def iterable(l):
    return hasattr(l, '__iter__')
