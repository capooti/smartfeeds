import csv
from feeds.models import Place
from django.template.defaultfilters import slugify
from django.contrib.gis.geos import Point

with open('/home/capooti/temp/allCountries.txt', 'rb') as csvfile:
    Place.objects.all().delete()
    csvreader = csv.reader(csvfile, delimiter='\t')
    for row in csvreader:
        name = row[1]
        lat = float(row[4])
        lon = float(row[5])
        print name, lat, lon
        p = Place()
        p.name = name
        p.slug = slugify(name)
        p.geometry = Point(lon, lat)
        p.save()
