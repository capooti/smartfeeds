from django.contrib import admin
from models import *
from django.contrib.gis.admin import GeoModelAdmin

class FeedAdmin(admin.ModelAdmin):

    model = Feed
    list_per_page = 20
    list_display = ['name', 'description', 'the_tags', 'enabled']
    search_fields = ['name', 'description']
    
    def the_tags(self, obj):
        return "%s" % (obj.tags.all(), )
    the_tags.short_description = 'Tags'

class ItemAdmin(admin.ModelAdmin):

    model = Item
    list_per_page = 20
    list_display = ['title', 'feed', 'feed_class', 'updated', 'filtered', 'archived', 'the_tags']
    search_fields = ['title', 'summary']
    list_filter = ['filtered', 'archived', 'feed']
    date_hierarchy = 'updated'

    def feed_class(self, obj):
        return "%s" % obj.feed.feed_class
      
    def the_tags(self, obj):
        return "%s" % (obj.tags.all(), )
    the_tags.short_description = 'Tags'

class PlaceAdmin(GeoModelAdmin):

    model = Place
    list_per_page = 20
    list_display = ['name', 'country']
    search_fields = ['name', 'item__title']
    list_filter = ['country']
    
    # Openlayers settings
    map_width = 500
    map_height = 500
    #openlayers_url = '/static/openlayers/lib/OpenLayers.js'
    default_zoom = 18

class PersonAdmin(admin.ModelAdmin):

    model = Person
    list_per_page = 20
    
class KeywordAdmin(admin.ModelAdmin):

    model = Keyword
    list_per_page = 20
    
class ImageAdmin(admin.ModelAdmin):

    model = Image
    list_per_page = 20
    list_display = ['src', 'alt']
    
class DomainAdmin(admin.ModelAdmin):

    model = Domain
    list_per_page = 20
    list_display = ['name', 'country']
    list_filter = ['country']
    
class FilterAdmin(admin.ModelAdmin):

    model = Filter
    list_per_page = 20
    
# register for admin
admin.site.register(Feed, FeedAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Filter, FilterAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Domain, DomainAdmin)


