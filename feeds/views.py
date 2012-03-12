# django
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.utils import simplejson
from django.contrib.gis.shortcuts import render_to_kml
from django.db.models import Count
from django.contrib.auth.decorators import login_required
import settings
# application
from models import Feed, Item, Place, Person, Domain, Keyword, Filter
from forms import PlaceForm

@login_required
def filters(request):
    """
    View a full list of the filters, and form for updating them.
    """
    # TODO for now we have just one filter containing all the keywords
    filters = Filter.objects.all()[0]
    instance = FilterForm.Meta.model.objects.get(pk=filters.id)
    form = FilterForm(instance=instance)
    # if it is a POST then we need to update the filter
    if request.method == 'POST': # POST
        form = FilterForm(request.POST, instance=instance)
        try:
            model = form.save()
            filter_items()
        except ValueError:
            pass
    return render_to_response('feeds/filter_list.html',
            {'form': form, },
            RequestContext(request))

def filter_items():
    """
    Filter all unarchive items based on the filters.
    """
    import re
    keywords = Filter.objects.all()[0].keywords
    keywords = keywords.splitlines()
    items = Item.objects.filter(archived=False)
    for item in items:
        text2filter = item.title + item.summary
        combined = "(" + ")|(".join(keywords) + ")"
        if re.search(combined, text2filter, re.IGNORECASE):
            print('\n***Item is going to be filtered!\n')
            item.filtered = True
        else:
            item.filtered = False
        item.save()

def get_kml_places(request):
    """
    View for generating kml for countries.
    """
    places = Place.objects.kml()
    return render_to_kml("gis/kml/placemarks.kml", {'places' : places})

@login_required
def item_archive(request, id):
    """
    Archive/Unarchive an Item
    """
    item = Item.objects.get(pk=id)
    print 'archiving item %s' % item.id
    status = 'archived'
    if item.archived:
        item.archived = False
        status = 'unarchived'
        if item.filtered:
            status = 'filtered'
    else:
        item.archived = True
    item.save()
    return HttpResponse(status)

def list_feeds_for_class(request, feedclass):
    """
    List the feeds name given a class.
    """
    feeds = Feed.objects.all()
    if feedclass != 'ALL':
        feeds = feeds.filter(feed_class=feedclass)
    print 'listing feeds for class: %s' % feedclass
    result = []
    for feed in feeds:
        result.append({"id":feed.id, "name":feed.name, "unarchived": feed.unarchived()})
    return HttpResponse(simplejson.dumps(result), mimetype='application/json')

# item

def items_list(request):
    """
    View a full list of items for a given feed, with certain filters.
    """
    #import ipdb;ipdb.set_trace()
    # query
    items = Item.objects.all().order_by('-updated')
    # feeds list
    feeds = Feed.objects.all().order_by('name')
    # check for filters
    # 1. filter for feedclass
    feedclass = 'ALL'
    if 'feedclass' in request.GET:
        feedclass = request.GET.get('feedclass', 'ALL')
        if feedclass != 'ALL':
            items = items.filter(feed__feed_class__exact=feedclass)
            feeds = feeds.filter(feed_class=feedclass)
    # 2. filter for archived
    archived = False
    if 'archived' in request.GET:
        archived = True
        if archived:
            items = items.filter(archived=False)
    # 3. filter for filtered
    filtered = False
    if 'filtered' in request.GET:
        filtered = True
        if filtered:
            items = items.filter(filtered=False)
    # 4. filter for geoparsed
    geoparsed = False
    if 'geoparsed' in request.GET:
        geoparsed = True
        if geoparsed:
            items = items.annotate(num_places=Count('place'))
            items = items.filter(num_places__gt=0)
    # 5. filter for feed
    feed = None
    if 'feedid' in request.GET:
        feed_id = int(request.GET.get('feedid', '9999'))
        if feed_id != 9999:
            feed = Feed.objects.get(pk=feed_id)
            items = items.filter(feed=feed)

    # is it an archive request?
    if 'submit-archive' in request.POST:
        # only if user is authenticated
        if request.user.is_authenticated():
            print 'Archiving %s items...' % items.filter(archived=False).count()
            for item in items:
                item.archived=True
                item.save()

    # archived and unarchive items count
    archived_count = items.filter(archived=True).count()

    return render_to_response('items/item_list.html', 
        {   'feeds' : feeds,
            'items' : items,
            'feedclass': feedclass,
            'archived': archived,
            'filtered': filtered,
            'geoparsed': geoparsed,
            'selectedfeed': feed,
            'archived_count': archived_count,
        },
        context_instance=RequestContext(request))

def item_detail(request, id):
    """
    Item detail for a given pk.
    """
    item = get_object_or_404(Item, pk=id)
    return render_to_response('items/item_detail.html',
            {'item': item, },
            RequestContext(request))
            
# place

def places_list(request):
    """
    View a full list of places.
    """
    places = Place.objects.all()
    return render_to_response('places/place_list.html', 
        {
            'places': places,
        },
        context_instance=RequestContext(request))

def place_detail(request, place_slug):
    """
    Place detail for a given name.
    """
    place = get_object_or_404(Place, slug=place_slug)
    form = PlaceForm(instance=place)
    return render_to_response('places/place_detail.html',
            {'place': place, 'form': form},
            RequestContext(request))
            
# person

def people_list(request):
    """
    View a full list of people.
    """
    people = Person.objects.all()
    return render_to_response('people/people_list.html', 
        {
            'people': people,
        },
        context_instance=RequestContext(request))

def person_detail(request, person_slug):
    """
    Person detail for a given name.
    """
    person = get_object_or_404(Person, slug=person_slug)
    return render_to_response('people/person_detail.html',
            {'person': person, },
            RequestContext(request))
            
# domain

def domains_list(request):
    """
    View a full list of domains.
    """
    domains = Domain.objects.all()
    return render_to_response('domains/domain_list.html', 
        {
            'domains': domains,
        },
        context_instance=RequestContext(request))

def domain_detail(request, id):
    """
    Domain detail for a given pk.
    """
    domain = get_object_or_404(Domain, pk=id)
    return render_to_response('domains/domain_detail.html',
            {'domain': domain, },
            RequestContext(request))
            
# keyword

def keyword_detail(request, keyword_name):
    """
    Keyword detail for a given name.
    """
    keyword = get_object_or_404(Keyword, name=keyword_name)
    return render_to_response('keywords/keyword_detail.html',
            {'keyword': keyword, },
            RequestContext(request))
            
# tag

def tags_list(request):
    """
    View a full list of tags.
    """
    return render_to_response('tags/tag_list.html', 
        {
        },
        context_instance=RequestContext(request))

def tag_detail(request, tag_slug):
    """
    Tag detail for a given name.
    """
    items = Item.objects.filter(tags__name__in=[tag_slug])
    return render_to_response('tags/tag_detail.html',
            {'tag_slug': tag_slug,
             'items': items, },
            RequestContext(request))
    
# test method
def test(request):
    """
    A view for test.
    """
    num_news = 10
    return render_to_response('others/test.html', 
        {'num_news' : num_news},
        RequestContext(request))
        
