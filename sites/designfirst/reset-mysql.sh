./manage.py sqlclear designer home product auth django paypal | ./manage.py dbshell
./manage.py syncdb --noinput
#./manage.py loaddata default
./manage.py createsuperuser --username=admin --email=admin@admin.admin

