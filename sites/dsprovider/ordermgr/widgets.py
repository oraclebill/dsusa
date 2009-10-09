from django.forms import widgets
from django.utils.safestring import mark_safe


class JQueryDatepicker(widgets.DateInput):

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.7.2/jquery-ui.min.js',
        )

    def render(self, name, value, attrs=None):
        base_input = super(JQueryDatepicker, self).render(name, value, attrs)
        id = attrs['id']
        return mark_safe(''.join([
            base_input,
            '<script type="text/javascript">$(function() {',
            '    $(\'#%s\').datepicker({' % id,
            '    changeMonth: true,',
            '       changeYear: true,',
            '       dateFormat: "%s"' % self.jquery_format(),
            '});});</script>',
        ]))

    def jquery_format(self):
        """
        Return self.format in format for jquery.
        Now only makes few simple modifications.
        """
        return self.format.replace('%Y', 'yy').replace('%m', 'mm').replace('%d', 'dd')

