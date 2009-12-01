from django import template
from django.conf import settings
from customer.models import Dealer

register = template.Library()

class MediaNode(template.Node):
    def __init__(self, file_path):
        self.file_path = file_path
    def render(self, context):
        try:
            prefix = settings.MEDIA_URL.rstrip('/')
        except:
            prefix = ''
        return "%s%s" % (prefix, self.file_path)

def do_add_media_url_prefix(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, file_path = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]
    return MediaNode(file_path)
register.tag('media', do_add_media_url_prefix)


@register.filter
def menu_type(user):
    if user.get_profile().account.status\
            in (Dealer.Const.SUSPENDED, Dealer.Const.CANCELLED):
        return 'limited'
    return 'dealer'
