# -*- coding: utf-8 -*-
#******************************************************************************
#  $Id$
# 
#  Project:  Sm@rtFeeds
#  Purpose:  Utility commands for the feeds application
#  Author:   Paolo Corti, paolo.corti@jrc.ec.europa.eu
# 
#******************************************************************************

# imports django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from taggit.models import Tag
from django.template.defaultfilters import slugify
from django.contrib.gis.geos import Point
# other
import sys
import tweepy
import re
import psycopg2
import feedparser
import urllib
import datetime
from time import mktime
# smartfeed
from feeds.models import Item, Place, Filter, Keyword, Search

class Command(BaseCommand):
    """
    Load rss items from google news in the database.
    This command must be scheduled in crontab, and should run every hour or so.
    """ 
    help = 'Load rss items from google news in the database.'

    def handle(self, *args, **options):
        #Item.objects.all().delete()
        for search in Search.objects.all():
            if search.is_enabled:
                for keyword in search.keywords.all():
                    feed_url = 'https://news.google.com/news/feeds?hl=en&gl=en&authuser=0&q=%s&um=1&ie=UTF-8&output=rss' % keyword
                    self.load_feed(search, feed_url)

    def load_feed(self, search, feed_url):
        feed_parsed = feedparser.parse(feed_url)
        for item_parsed in feed_parsed.entries:
            link = item_parsed.link
            # then we unquote the url (ex http://voria.gr/index.php?module%3Dnews%26func%3Ddisplay%26sid%3D56406 becomes
            # http://voria.gr/index.php?module=news&func=display&sid=56406
            link = urllib.unquote(link)
            if len(link)>255:
                self.stdout.write('\nItem link is more than 255 chars!\n%s\n' % link)
                link = link[:255]
            # must import only items not already in the database (check URL of item)
            items = Item.objects.filter(link=link)
            if len(items)==0: # new item, must import it!
                if True:
                    self.stdout.write('Parsing item %s' % item_parsed.title.encode('utf-8'))
                    # store item
                    item = Item()
                    item.title = item_parsed.title[:255].encode('utf-8')
                    item.summary = item_parsed.summary.encode('utf-8')
                    item.link = link
                    item.updated = datetime.datetime.fromtimestamp(mktime(item_parsed.updated_parsed))
                    # save item
                    item.save()
                    item.search_set.add(search)
                    
                    # define text to be parsed
                    text2parse = item.title + item.summary
                        
                    # 5. places
                    for p_key in text2parse.split():
                        p_key = p_key.translate(None, "?,#:'\"") # remove certain characters
                        if len(p_key) > 4:
                            place = None
                            if Place.objects.filter(name__iexact=p_key).exists():
                                place = Place.objects.filter(name__iexact=p_key)[0]
                            else:
                                placename = self.get_placename(p_key)
                                if placename:
                                    place = Place()
                                    place.name = p_key #placename[0]
                                    place.slug = slugify(placename[0])
                                    place.geometry = Point(placename[1], placename[2])
                            if place:
                                # if we have a place, check if the place is on the search geometry
                                #qs = SpatialFilter.objects.filter(geometry__contains=place.geometry)
                                if search.geometry.contains(place.geometry):
                                    place.save()
                                    item.places.add(place)
                    # remove the tweet if it if has no places
                    if item.places.count()==0:
                        item.delete()
                    else:
                        self.stdout.write('Item imported!')
                    
        # finally let's remove old items
        self.stdout.write('\n***Removing old items')
        firstday = datetime.date.today()-datetime.timedelta(days=int(settings.DAYS_TO_KEEP))
        Tweet.objects.filter(updated__lte=firstday).delete()
                        
    def get_placename(self, name):
        conn = psycopg2.connect("dbname=%s user=%s password=%s" % 
            (settings.DATABASES['default']['NAME'],
            settings.DATABASES['default']['USER'],
            settings.DATABASES['default']['PASSWORD']))
        cur = conn.cursor()
        cur.execute("SELECT name, longitude, latitude FROM geonames WHERE LOWER(asciiname) = '%s';" % name.lower())
        placename = cur.fetchone()
        cur.close()
        conn.close()
        return placename
