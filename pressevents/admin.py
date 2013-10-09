from django.contrib import admin
from models import Event, EventCode
from django.contrib.gis.admin import GeoModelAdmin
#from django.contrib.gis.admin import OSMGeoAdmin

class EventCodeAdmin(admin.ModelAdmin):

    model = EventCode
    list_per_page = 20
    list_display = ['code', 'description']
    search_fields = ['description']
    
class EventAdmin(admin.ModelAdmin):

    model = Event
    list_per_page = 20
    list_display = ['globaleventid', 'date', 'num_mentions', 'num_sources', 
        'num_articles', 'action_geotype', 'eventcode', 'keyword']
    list_filter = ['keyword',]
    search_fields = ['url', 'eventcode__description']
    date_hierarchy = 'date'
    
# register for admin
admin.site.register(Event, EventAdmin)
admin.site.register(EventCode, EventCodeAdmin)
