from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
import god
god.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'demo.views.home', name='home'),
    # url(r'^demo/', include('demo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^god/', include(god.site.urls)),
)
