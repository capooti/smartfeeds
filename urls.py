import os

# django batteries
from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic import list_detail, create_update
from django.core.urlresolvers import reverse


# admin
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # admin url
    (r'^admin/', include(admin.site.urls)),

    # feeds url
    (r'^feeds/', include('feeds.urls')),
    
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': os.path.join(os.path.dirname(__file__), "media"),
             'show_indexes': True
            }),
    )
