rm designfirst.db 
./manage.py syncdb --noinput
#./manage.py loaddata default
./manage.py createsuperuser --username=admin --email=admin@admin.admin

