#-*- coding: utf-8 -*-
import datetime 
strftime = datetime.datetime.strftime

from django.http import HttpResponse
from django.template import Context, loader

from models import Guwenguanzhi

def gwgzh(request):
    objs = Guwenguanzhi.objects.all()
    items = []
    for o in objs:
        items.append({
            "vol": o.vol,
            "pos": "第%s篇" % o.pos,
            "title": o.title,
            "author": o.author,
            "finished": "Y" if o.finished else "",
            "startdate": strftime(o.startdate, "%Y-%m-%d") if o.startdate else "",
            "enddate": strftime(o.startdate, "%Y-%m-%d") if o.startdate else "",
        })
    t = loader.get_template('guwenguanzhi.html')
    c = Context({
        'items': items
    })
    return HttpResponse(t.render(c))
