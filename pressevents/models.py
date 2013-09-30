# django
from django.db import models
from django.contrib.gis.db import models as gismodels

class EventCode(gismodels.Model):
    """
    CAMEO Event Codes for Events.
    """
    code = gismodels.CharField(max_length=5)
    description = gismodels.CharField(max_length=255)
    
    def __unicode__(self):
        return '%s' % (self.description)

class Event(gismodels.Model):
    """
    Spatial model for Events.
    """
    
    KEYWORD_CHOICES = (
        (0, 'N/A'),
        (1, 'Earthquake'),
        (2, 'Flood'),
        (3, 'Refugee'),
        (4, 'Conflict'),
        (5, 'Rebel'),
    )

    globaleventid = gismodels.IntegerField()
    date = gismodels.DateField()
    url = gismodels.URLField(max_length=255)
    num_mentions = gismodels.IntegerField()
    num_sources = gismodels.IntegerField()
    num_articles = gismodels.IntegerField()
    action_geotype = gismodels.IntegerField()
    eventcode = models.ForeignKey(EventCode, null=True)
    keyword = models.IntegerField(choices=KEYWORD_CHOICES, default=0)
    geometry = gismodels.PointField(srid=4326)
    
    objects = gismodels.GeoManager()

    def __unicode__(self):
        return '%s' % (self.globaleventid)
