from django import template

register = template.Library()


@register.filter
def step_finished(wizard, step):
    return wizard.order.is_step_finished(step['slug'])
