from django.dispatch import Signal

status_changed = Signal(providing_args=['old', 'new'])

