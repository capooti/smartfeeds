# -*- coding: utf-8 -*-
#******************************************************************************
#  $Id$
# 
#  Project:  Sm@rtFeeds
#  Purpose:  Utility commands for the feeds application
#  Author:   Paolo Corti, paolo.corti@jrc.ec.europa.eu
# 
#******************************************************************************

# imports python
import datetime
from time import mktime
import re
import urlparse
import urllib
from urllib2 import urlopen
from urllib import urlretrieve
from BeautifulSoup import BeautifulSoup as bs
import os
import sys
# imports django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.template.defaultfilters import slugify
from django.contrib.gis.utils import GeoIP
# imports feeds
from feeds.models import (Feed, Item, Place, Filter, Country, Person, Keyword, 
    Image, Domain)
from feeds.utils.placemaker import placemaker
import settings
# externals
import feedparser
from taggit.models import Tag

def get_original_url(url):
    urlsplitted = url.split('http://')
    url = 'http://%s' % urlsplitted[len(urlsplitted)-1]
    return url

class Command(BaseCommand):
    """
    Load feeds from RSS in the database.
    This command must be scheduled in crontab, and should run every hour or so.
    """ 
    help = 'Load feeds from RSS in the database.'

    def handle(self, *args, **options):
        #try:
        #Item.objects.all().delete()
        #Place.objects.all().delete()
        #Domain.objects.all().delete()
        self.loadfeeds()
        self.stdout.write('\nFeeds succesfully loaded in database.\n')
        #except Exception,e:
            #self.stdout.write(e)
            #self.stdout.write('An error as occourred storing the feeds.\n')

    def loadfeeds(self):
        # for now I keep this utility command very basic, much more refactoring in future
        # now we start sorting the feeds
        feeds = Feed.objects.all().filter(enabled=True)
        for feed in feeds:
            self.stdout.write('\n***Parsing feed %s' % feed.name.encode('utf-8'))
            feed_parsed = feedparser.parse(feed.url_xml)
            import ipdb;ipdb.set_trace()
            for item_parsed in feed_parsed.entries:
                biased_link = item_parsed.link
                # link must be restored to original (in some case it is: http://news.google.com/news...&url=http//www.example.com
                self.stdout.write('Biased link: %s' % biased_link)
                link = get_original_url(biased_link)
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
                        self.stdout.write('\nImporting item %s' % item_parsed.title.encode('utf-8'))
                        # store item
                        item = Item()
                        item.title = item_parsed.title[:255].encode('utf-8')
                        item.summary = item_parsed.summary.encode('utf-8')
                        item.link = link
                        item.feed = feed
                        item.updated = datetime.datetime.fromtimestamp(mktime(item_parsed.updated_parsed))
                        
                        # 0. domain
                        # first let's check domain country
                        parsed = urlparse.urlsplit(link)
                        domain_name = parsed.netloc.encode('utf-8')
                        g = GeoIP()
                        country_code = g.country(domain_name)['country_code']
                        self.stdout.write('\nDomain: %s, country code: %s' % (domain_name, country_code))
                            
                        countries = Country.objects.filter(iso2=country_code)
                        country = None
                        if countries.count() > 0:
                            country = countries[0]
                        # check if if we need to add domain in db
                        domains = Domain.objects.all().filter(name=domain_name)
                        if not domains:
                            self.stdout.write('\nAdding a new domain to the system: %s for this item.' % domain_name)
                            domain = Domain()
                            domain.name = domain_name
                            domain.country = country
                            domain.save()
                        else:
                            domain = domains[0]
                        # add the item to the place
                        item.domain = domain
                        
                        # save item
                        item.save()
                        
                        # define text to be parsed
                        text2parse = item.title + item.summary
                        # 1. keywords
                        keywords = Keyword.objects.all()
                        for keyword in keywords:
                            if re.search(keyword.name, text2parse, re.IGNORECASE):
                                self.stdout.write('\n***Keyword %s is in this item.' % keyword.name)
                                #import ipdb;ipdb.set_trace()
                                keyword.item.add(item)
                                
                        # 2. people
                        people = Person.objects.all()
                        for person in people:
                            if re.search(person.name, text2parse, re.IGNORECASE):
                                self.stdout.write('\n***Person %s is in this item.' % person.name)
                                #import ipdb;ipdb.set_trace()
                                person.item.add(item)
                                
                        # 3. images
                        #url = item.link
                        #soup = bs(urlopen(url))
                        #parsed = list(urlparse.urlparse(url))
                        soup = bs(item.summary)
                        parsed = list(item.summary)
                        for img in soup.findAll("img"):
                            print img
                            alt = ''
                            if img.has_key('src'):
                                if img.has_key('alt'):
                                    alt = img["alt"]
                                if img["src"].lower().startswith("http"):
                                    #import ipdb;ipdb.set_trace()
                                    src = img["src"]
                                else:
                                    # TODO src extraction from relative url
                                    src = urlparse.urlunparse(parsed)
                                print src
                                image = Image()
                                image.src = src
                                image.alt = alt
                                image.item = item
                                image.save()
                                
                        # 4. tags
                        tags = Tag.objects.all()
                        for tag in tags:
                            if re.search(tag.name, text2parse, re.IGNORECASE):
                                self.stdout.write('\n***Tag %s is in this item.' % tag.name)
                                item.tags.add(tag)
                            
                        # 5. places
                        # let's check if there are places linked to this item
                        pm=placemaker(settings.PLACEMAKER_KEY)
                        pm_places = pm.find_places(text2parse)
                        for pm_place in pm_places:
                            #import ipdb;ipdb.set_trace()
                            placename = pm_place.name.decode('utf-8')
                            # first check if we need to add new place
                            places = Place.objects.all().filter(name=placename)
                            if not places:
                                self.stdout.write('\nAdding a new place to the system: %s for this item.' % pm_place.name)
                                place = Place()
                                place.name = placename
                                place.slug = slugify(place.name)
                                place.geometry = 'POINT(%s %s)' % (pm_place.centroid.longitude, pm_place.centroid.latitude)
                                place.save()
                            else:
                                place = places[0]
                            # add the item to the place
                            #import ipdb;ipdb.set_trace()
                            place.items.add(item)
                        # if the item has not places in some cases we are not interested
                        if item.place_set.count()==0:
                            item.delete()
                    #except Exception,e:
                    #    self.stdout.write('\nThere was an error importing this item. Skipping to the next one...')
        # finally let's remove old items
        self.stdout.write('\n***Removing old items')
        firstday = datetime.date.today()-datetime.timedelta(days=int(settings.DAYS_TO_KEEP))
        Item.objects.filter(updated__lte=firstday).delete()







