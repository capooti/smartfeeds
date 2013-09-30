import os

# django batteries
from django.conf.urls.defaults import *
from django.conf import settings
from django.core.urlresolvers import reverse

# admin
from django.contrib import admin
admin.autodiscover()

from feeds.views import tweets_map

urlpatterns = patterns('',

    # home page
    url(r'^$', tweets_map, name='tweets-map'),
    
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
