from django.conf.urls.defaults import *

import views

urlpatterns = patterns('',
    # items
    url(r'^map$', views.items_map, name='items-map'),
    url(r'^items$', views.items_list, name='items-list'),
    url(r'^item/(?P<id>\d+)/detail$', views.item_detail, name='item-detail'),
    
    # places
    url(r'^places$', views.places_list, name='places-list'),
    url(r'^places/(?P<place_slug>[-\w]+)/detail$', views.place_detail, name='place-detail'),
    
    # people
    url(r'^people$', views.people_list, name='people-list'),
    url(r'^people/(?P<person_slug>[-\w]+)/detail$', views.person_detail, name='person-detail'),
    
    # domains
    url(r'^domains$', views.domains_list, name='domains-list'),
    url(r'^domains/(?P<id>\d+)/detail$', views.domain_detail, name='domain-detail'),
    
    # keywords
    url(r'^keyword/(?P<keyword_name>[-\w]+)/detail$', views.keyword_detail, name='keyword-detail'),
    
    # tags
    url(r'^tags$', views.tags_list, name='tags-list'),
    url(r'^tags/(?P<tag_slug>[-\w]+)/detail$', views.tag_detail, name='tag-detail'),
    
    # update methods
    url(r'^item/(?P<id>\d+)/archive$', views.item_archive, name='item-archive'),
    # json methods
    url(r'^feeds/class/(?P<feedclass>\w+)/list$', views.list_feeds_for_class, name='list-feeds-for-class'),
    # kml output
    url(r'^kml/places/$', views.get_kml_places, name='places-kml'),
    # filters
    url(r'^filters/$', views.filters, name='filters'),
    # test
    url(r'^test/$', views.test, name='test'),
)
