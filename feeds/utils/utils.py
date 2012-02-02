from datetime import datetime
from geofeeds.models import Item

def archive_items(year, month, day):
    items = Item.objects.all()
    old_items = items.filter(updated__lt=datetime(year, month, day))
    for item in old_items:
        item.archived = True
        item.save()
    print '%s items archived.' % len(old_items)

