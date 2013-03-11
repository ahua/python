#!/usr/bin/env python

import os
# nginx configuration 
nginx_dns = "10.2.25.12"
uwsgi_dns = "10.2.25.12"

# uwsgi configuration
pythonpath = "/var/djangodemo/enabled/django/source" 
chdir = os.path.join(pythonpath, "demo")
wsgi_file = os.path.join(chdir, "django_wsgi.py")
mysite = "demo"


