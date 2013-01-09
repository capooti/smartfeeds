from django import template
from feeds.models import Item
import settings

register = template.Library()

@register.inclusion_tag('template_tags/places.html')
def show_places(item):
    places = item.place_set.all()
    return {
        'places': places,
    }
    
@register.inclusion_tag('template_tags/people_short.html')
def show_people_short(item):
    people = item.person_set.all()
    #import ipdb;ipdb.set_trace()
    return {
        'people': people,
    }
    
@register.inclusion_tag('template_tags/people_long.html')
def show_people_long(item):
    people = item.person_set.all()
    return {
        'people': people,
    }

@register.inclusion_tag('template_tags/domain.html')
def show_domain(item):
    return {
        'item': item,
    }
    
@register.inclusion_tag('template_tags/keywords_long.html')
def show_keywords_long(item):
    keywords = item.keyword_set.all()
    return {
        'keywords': keywords,
    }
    
@register.inclusion_tag('template_tags/keywords_short.html')
def show_keywords_short(item):
    keywords = item.keyword_set.all()
    return {
        'keywords': keywords,
    }
    
@register.inclusion_tag('template_tags/images_short.html')
def show_images_short(item):
    images = item.image_set.all()
    return {
        'count': images.count(),
    }
    
@register.inclusion_tag('template_tags/images_long.html')
def show_images_long(item):
    images = item.image_set.all()
    return {
        'images': images,
    }
    
@register.inclusion_tag('template_tags/tags.html')
def show_tags(item):
    tags = item.tags.all()
    return {
        'tags': tags,
    }
    
@register.inclusion_tag('template_tags/show_place_map.html')
def show_map(place):
    return {
        'place': place,
        'cloudmade_api_key': settings.CLOUDMADE_API_KEY
    }
    
@register.inclusion_tag('template_tags/show_places_map.html')
def show_places_map(items):
    return {
        'items': items,
        'cloudmade_api_key': settings.CLOUDMADE_API_KEY
    }
    
    
