from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^gwgzh/$', 'guwen.views.gwgzh'),

    url(r'^test/tinymce/$', 'study.views.tinymce')
)

urlpatterns += staticfiles_urlpatterns()
