# geodjango batteries
from django.contrib.gis.utils import LayerMapping
# geofeeds
from feeds.models import Country

def import_shp(shp='feeds/data/shapefile/TM_WORLD_BORDERS-0.3.shp'):
    # firest delete all features (if any)
    Country.objects.all().delete()
    # mapping model-shp
    country_mapping = {
        'name' : 'NAME',
        'fips' : 'FIPS',
        'iso2' : 'ISO2',
        'iso3' : 'ISO3',
        'geometry' : 'MULTIPOLYGON',
    }
    # import features from shapefile to model
    countries = LayerMapping(Country, shp, country_mapping, transform=False, 
        encoding='iso-8859-1')
    countries.save(verbose=True, progress=True)
    print 'Import completed.'

import_shp()
