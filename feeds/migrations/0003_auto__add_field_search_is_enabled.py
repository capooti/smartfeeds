# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Search.is_enabled'
        db.add_column('feeds_search', 'is_enabled',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Search.is_enabled'
        db.delete_column('feeds_search', 'is_enabled')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'feeds.country': {
            'Meta': {'ordering': "['name']", 'object_name': 'Country'},
            'fips': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'geometry': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso2': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'iso3': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'feeds.domain': {
            'Meta': {'ordering': "['name']", 'object_name': 'Domain'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feeds.Country']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'feeds.feed': {
            'Meta': {'ordering': "['name']", 'object_name': 'Feed'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url_html': ('django.db.models.fields.URLField', [], {'max_length': '255'}),
            'url_xml': ('django.db.models.fields.URLField', [], {'max_length': '255'})
        },
        'feeds.filter': {
            'Meta': {'object_name': 'Filter'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.TextField', [], {})
        },
        'feeds.image': {
            'Meta': {'object_name': 'Image'},
            'alt': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feeds.Item']"}),
            'src': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'feeds.item': {
            'Meta': {'object_name': 'Item'},
            'archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feeds.Domain']"}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feeds.Feed']"}),
            'filtered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.TextField', [], {}),
            'summary': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        'feeds.keyword': {
            'Meta': {'object_name': 'Keyword'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'})
        },
        'feeds.person': {
            'Meta': {'ordering': "['name']", 'object_name': 'Person'},
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'tweets': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['feeds.Tweet']", 'null': 'True', 'blank': 'True'})
        },
        'feeds.place': {
            'Meta': {'object_name': 'Place'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feeds.Country']", 'null': 'True'}),
            'from_gps': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'geometry': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'})
        },
        'feeds.search': {
            'Meta': {'ordering': "['name']", 'object_name': 'Search'},
            'geometry': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'keywords': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['feeds.Keyword']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tweets': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['feeds.Tweet']", 'null': 'True', 'blank': 'True'})
        },
        'feeds.tweet': {
            'Meta': {'object_name': 'Tweet'},
            'archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'filtered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'places': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['feeds.Place']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'twitter_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_tagged_items'", 'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taggit_taggeditem_items'", 'to': "orm['taggit.Tag']"})
        }
    }

    complete_apps = ['feeds']