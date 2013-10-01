# python
import urlparse
# django
from django.db import models
from django.contrib.gis.db import models as gismodels
from django.db.models.signals import pre_save
# django-taggit
from taggit.managers import TaggableManager

class Country(gismodels.Model):
    """
    Spatial model for Countries.
    """
    # attributes
    name = gismodels.CharField(max_length=50)
    fips = gismodels.CharField(max_length=2)
    iso2 = gismodels.CharField(max_length=2)
    iso3 = gismodels.CharField(max_length=3)
    geometry = gismodels.MultiPolygonField(srid=4326)
    objects = gismodels.GeoManager()

    def __unicode__(self):
        return '%s' % (self.name)
        
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Countries"
        
class Domain(models.Model):
    """
    Model for Internet Domain.
    """
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, null=True)
    
    def __unicode__(self):
        return '%s' % (self.name)
    
    class Meta:
        ordering = ['name']

class Feed(models.Model):
    """
    Model for Feeds.
    """
    # attributes
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    url_xml = models.URLField(max_length=255)
    url_html = models.URLField(max_length=255)
    enabled = models.BooleanField()
    icon = models.ImageField(null=True, blank=True, upload_to='feeds')
    tags = TaggableManager()

    def __unicode__(self):
        return '%s' % (self.name)

    def unarchived(self):
        return self.item_set.all().filter(archived=False).count()
        
    class Meta:
        ordering = ['name']

class Item(models.Model):
    """
    Model for Items.
    """
    # attributes
    title = models.CharField(max_length=255)
    summary = models.TextField()
    updated = models.DateTimeField(null=True)
    link = models.TextField()
    filtered = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    
    feed = models.ForeignKey(Feed)
    domain = models.ForeignKey(Domain)
    
    tags = TaggableManager()

    def item_type(self):
        if self.archived:
            return 'archived-item'
        if self.filtered:
            return 'filtered-item'
        return 'simple-item'

    #def domain(self):
    #    parsed = urlparse.urlsplit(self.link)
    #    return parsed.netloc.encode('utf-8')

    def __unicode__(self):
        return '%s' % (self.title)

class Place(gismodels.Model):
    """
    Spatial model for Countries.
    """
    # attributes
    name = gismodels.CharField(max_length=255)
    slug = gismodels.SlugField(max_length=255)
    geometry = gismodels.PointField(srid=4326)
    #tweets = models.ManyToManyField(Tweet, null=True, blank=True)
    from_gps = gismodels.BooleanField()
    country = models.ForeignKey(Country, null=True, blank=True) # derived
    objects = gismodels.GeoManager()

    def __unicode__(self):
        return '%s' % (self.name)
        
class Tweet(models.Model):
    """
    Model for Tweets.
    """
    # attributes
    twitter_id = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(null=True)
    username = models.CharField(max_length=255)
    filtered = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    places = models.ManyToManyField(Place, null=True, blank=True)
    
    tags = TaggableManager()

    def item_type(self):
        if self.archived:
            return 'archived-item'
        if self.filtered:
            return 'filtered-item'
        return 'simple-item'

    def __unicode__(self):
        return '%s' % (self.status)
        
    def the_places(self):
        return "\n".join([p.name for p in self.places.all()])
        
    def the_searches(self):
        return "\n".join([s.name for s in self.search_set.all()])
        
class Person(gismodels.Model):
    """
    Model for Person.
    """
    # attributes
    name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    tweets = models.ManyToManyField(Tweet, null=True, blank=True)

    def __unicode__(self):
        return '%s' % (self.name)
        
    class Meta:
        ordering = ['name']
        verbose_name_plural = "People"
        
class Keyword(gismodels.Model):
    """
    Model for Keyword.
    """
    # attributes
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    def __unicode__(self):
        return '%s' % (self.name)
        
class Search(gismodels.Model):
    """
    Spatial model for Search.
    """
    # attributes
    name = gismodels.CharField(max_length=50)
    geometry = gismodels.MultiPolygonField(srid=4326)
    keywords = models.ManyToManyField(Keyword, null=True, blank=True)
    tweets = models.ManyToManyField(Tweet, null=True, blank=True)
    is_enabled = models.BooleanField()
    objects = gismodels.GeoManager()

    def __unicode__(self):
        return '%s' % (self.name)
        
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Searches"
        
    def the_keywords(self):
        return "\n".join([k.name for k in self.keywords.all()])
        
class Image(gismodels.Model):
    """
    Model for Image.
    """
    # attributes
    src = models.CharField(max_length=255)
    alt = models.CharField(max_length=255)
    item = models.ForeignKey(Item)

    def __unicode__(self):
        return '%s' % (self.alt)
    
class Filter(models.Model):
    """
    Model for Filter.
    """
    # attributes
    keywords = models.TextField()  
    # TODO maybe we may have a keywords list for each feed? For now is global
    # TODO maybe we have a end date for a certain filter? For now is manual

### signals

def place_pre_save(sender, **kwargs):
    # country
    place = kwargs["instance"]
    rsc = Country.objects.filter(geometry__contains=place.geometry)
    if rsc.count()>0:
        country = rsc[0]
        place.country = country
       
pre_save.connect(place_pre_save, sender=Place)
