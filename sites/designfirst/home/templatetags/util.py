from django import template

register = template.Library()


class MediaNode(template.Node):
    def __init__(self, file_path):
        self.file_path = file_path
    def render(self, context):
	from settings import MEDIA_URL
	try:
		prefix = MEDIA_URL.rstrip('/')
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

