# imports python
import csv
import datetime
# imports django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.template.defaultfilters import slugify
from django.contrib.gis.geos import Point
# smartfeed
from pressevents.models import Event, EventCode

class Command(BaseCommand):
    """
    Load events from the GDELT database.
    This command must be scheduled in crontab, and should run every day.
    """ 
    help = 'Load events from the GDELT database.'

    def handle(self, *args, **options):
        #Event.objects.all().delete()
        keywords = ['earthquake', 'flood', 'rebel', 'refugee']
        with open('/home/capooti/git/github/capooti/smartfeeds/temp/20130925.export.CSV', 'rb') as csvfile:
            eventsreader = csv.reader(csvfile, delimiter='\t')
            for row in eventsreader:
                print row
                lon = row[54]
                lat = row[53]
                # we import it only if we have the coordinates
                if(len(lon)>0 and len(lat)>0):
                    globaleventid = row[0]
                    date = row[1]
                    url = row[57]
                    num_mentions = row[31]
                    num_sources = row[32]
                    num_articles = row[33]
                    action_geotype = row[49]
                    event_code = row[26]
                    print globaleventid, date, url, lon, lat
                    event = Event()
                    event.globaleventid = globaleventid
                    event.date = datetime.date(int(date[0:4]), int(date[4:6]), int(date[6:9]))
                    event.url = url
                    event.num_mentions = num_mentions
                    event.num_sources = num_sources
                    event.num_articles = num_articles
                    event.action_geotype = action_geotype
                    try:
                        ec = EventCode.objects.filter(code=event_code)[0]
                        event.eventcode = ec
                    except:
                        print 'Not such an event code!'
                    for i in range(0, len(Event.KEYWORD_CHOICES)-1):
                        #import ipdb;ipdb.set_trace()
                        if(Event.KEYWORD_CHOICES[i][1].lower() in url.lower()):
                            #import ipdb;ipdb.set_trace()
                            event.keyword = Event.KEYWORD_CHOICES[i][0]
                    #import ipdb;ipdb.set_trace()
                    event.geometry = Point(float(lon), float(lat))
                    event.save()
