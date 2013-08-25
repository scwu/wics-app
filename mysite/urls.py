from django.conf.urls.defaults import patterns, include, url
from app import views
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin #HP uncommented
admin.autodiscover() #HP uncommented

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),
    #HP Important general shit
    (r'^admin/jsi18n/$', 'django.views.i18n.javascript_catalog', {}, ""),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')), #HP uncommented
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)), #HP uncommented
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
    }),
    #HP this serves our media files the easy(ish) way.
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}), #HP

    #HP the real pages

    (r'^$', views.index, {}, "Home"),
    (r'^about/$', views.about, {}, "About"),
    (r'^contact/$', views.contact, {}, "Contact Us"),
    (r'^photos/$', views.photos, {}, "Photos"),
    (r'^career/$', views.career, {}, "Career"),
    (r'^events/$', views.calendar, {}, "Calendar"),
    (r'^photos/(.*)/$', views.photos_all, {}, ""),


    #HP add pages here
)
