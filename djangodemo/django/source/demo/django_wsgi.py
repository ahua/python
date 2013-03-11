#!/usr/bin/env python

import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'demo.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()

