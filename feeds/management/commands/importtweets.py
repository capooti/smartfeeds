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
# smartfeed
from feeds.models import Tweet, Place, Filter, Country, Keyword, Person, Search
from feeds.utils.placemaker import placemaker

class Command(BaseCommand):
    """
    Load tweets from twitter in the database.
    This command must be scheduled in crontab, and should run every hour or so.
    """ 
    help = 'Load tweets from Twitter in the database.'

    def handle(self, *args, **options):
        #try:
        #Item.objects.all().delete()
        #Place.objects.all().delete()
        #Domain.objects.all().delete()
        query = "flood"
        consumer_key = settings.TWITTER_AUTH['CONSUMER_KEY']
        consumer_secret = settings.TWITTER_AUTH['CONSUMER_SECRET']
        access_token = settings.TWITTER_AUTH['ACCESS_TOKEN']
        access_secret = settings.TWITTER_AUTH['ACCESS_SECRET']
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        api = tweepy.API(auth)
        #Tweet.objects.all().delete()
        #Place.objects.all().delete()
        for search in Search.objects.all():
            if search.is_enabled:
                for keyword in search.keywords.all():
                    results = api.search(q=keyword.name, count=100)
                    #results = tweepy.Cursor(api.search(q=keyword.name)).items()
                    for result in results:
                        #import ipdb;ipdb.set_trace()
                        print " ID: %s" % result.id
                        print " From: %s" % result.user.name.encode('utf-8')
                        print " Created : %s" % result.created_at
                        print " %s" % result.text.encode('utf-8')
                        self.loadtweet(search, result)

    def loadtweet(self, search, result):
        tweets = Tweet.objects.filter(twitter_id=result.id)
        if len(tweets)==0: # new item, must import it!
            if True:
                # store item
                t = Tweet()
                t.twitter_id = result.id
                t.status = result.text.encode('utf-8')
                t.username = result.user.name.encode('utf-8')
                t.created_at = result.created_at
                t.save()
                t.search_set.add(search)
                
                # define text to be parsed
                text2parse = t.status

                # 2. people
                people = Person.objects.all()
                for person in people:
                    if re.search(person.name, text2parse, re.IGNORECASE):
                        self.stdout.write('\n***Person %s is in this item.' % person.name)
                        #import ipdb;ipdb.set_trace()
                        person.tweets.add(t)
                        
                # 4. tags
                tags = Tag.objects.all()
                for tag in tags:
                    if re.search(tag.name, text2parse, re.IGNORECASE):
                        self.stdout.write('\n***Tag %s is in this item.' % tag.name)
                        t.tags.add(tag)
                        
                # 5. places
                for p_key in t.status.split():
                    p_key = p_key.translate(None, "?,#:'\"") # remove certain characters
                    if len(p_key) > 3:
                        place = None
                        if Place.objects.filter(name__iexact=p_key).exists():
                            #import ipdb;ipdb.set_trace()
                            place = Place.objects.filter(name__iexact=p_key)[0]
                        else:
                            placename = self.get_placename(p_key)
                            if placename:
                                #import ipdb;ipdb.set_trace()
                                place = Place()
                                place.name = p_key #placename[0]
                                place.slug = slugify(placename[0])
                                place.geometry = Point(placename[1], placename[2])
                        if place:
                            # if we have a place, check if the place is on the search geometry
                            #qs = SpatialFilter.objects.filter(geometry__contains=place.geometry)
                            if search.geometry.contains(place.geometry):
                                place.save()
                                t.places.add(place)
                # we can have the geo place from twitter
                if result.geo:
                    place = Place()
                    place.name = t.status
                    place.slug = slugify(t.status)
                    place.geometry = Point(result.geo['coordinates'][1], result.geo['coordinates'][0])
                    place.from_gps = True
                    print place.geometry.x, place.geometry.y, search.name
                    print search.geometry.extent
                    if search.geometry.contains(place.geometry):
                        place.save()
                        t.places.add(place)
                # remove the tweet if it if has no places
                if t.places.count()==0:
                    t.delete()
                        
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
