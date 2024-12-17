#!/bin/bash
source /var/www/sharp/Sharpologican-django/myenv/bin/activate
exec /var/www/sharp/Sharpologican-django/myenv/bin/gunicorn --bind unix:/var/www/sharp/Sharpologican-django/myproject.sock --workers 3 myproject.wsgi:application
