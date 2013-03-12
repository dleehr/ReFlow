from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'reflow.views.home', name='home'),
    (r'^', include('authenticate.urls')),
    (r'^api/', include('rest_framework.urls', namespace='rest_framework')),
    (r'^rest-api/', include('rest_framework_docs.urls', namespace='rest_framework_docs')),
    (r'^', include('repository.urls')),
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)
