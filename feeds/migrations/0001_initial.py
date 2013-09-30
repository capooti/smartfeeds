# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Country'
        db.create_table('feeds_country', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('fips', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('iso2', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('iso3', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')()),
        ))
        db.send_create_signal('feeds', ['Country'])

        # Adding model 'Domain'
        db.create_table('feeds_domain', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['feeds.Country'], null=True)),
        ))
        db.send_create_signal('feeds', ['Domain'])

        # Adding model 'Feed'
        db.create_table('feeds_feed', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url_xml', self.gf('django.db.models.fields.URLField')(max_length=255)),
            ('url_html', self.gf('django.db.models.fields.URLField')(max_length=255)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('icon', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('feeds', ['Feed'])

        # Adding model 'Item'
        db.create_table('feeds_item', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('summary', self.gf('django.db.models.fields.TextField')()),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('link', self.gf('django.db.models.fields.TextField')()),
            ('filtered', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('archived', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['feeds.Feed'])),
            ('domain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['feeds.Domain'])),
        ))
        db.send_create_signal('feeds', ['Item'])

        # Adding model 'Place'
        db.create_table('feeds_place', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['feeds.Country'], null=True)),
        ))
        db.send_create_signal('feeds', ['Place'])

        # Adding model 'Tweet'
        db.create_table('feeds_tweet', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('twitter_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('filtered', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('archived', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('feeds', ['Tweet'])

        # Adding M2M table for field places on 'Tweet'
        db.create_table('feeds_tweet_places', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tweet', models.ForeignKey(orm['feeds.tweet'], null=False)),
            ('place', models.ForeignKey(orm['feeds.place'], null=False))
        ))
        db.create_unique('feeds_tweet_places', ['tweet_id', 'place_id'])

        # Adding model 'Person'
        db.create_table('feeds_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
        ))
        db.send_create_signal('feeds', ['Person'])

        # Adding M2M table for field tweets on 'Person'
        db.create_table('feeds_person_tweets', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm['feeds.person'], null=False)),
            ('tweet', models.ForeignKey(orm['feeds.tweet'], null=False))
        ))
        db.create_unique('feeds_person_tweets', ['person_id', 'tweet_id'])

        # Adding model 'Keyword'
        db.create_table('feeds_keyword', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
        ))
        db.send_create_signal('feeds', ['Keyword'])

        # Adding model 'Search'
        db.create_table('feeds_search', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')()),
        ))
        db.send_create_signal('feeds', ['Search'])

        # Adding M2M table for field keywords on 'Search'
        db.create_table('feeds_search_keywords', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('search', models.ForeignKey(orm['feeds.search'], null=False)),
            ('keyword', models.ForeignKey(orm['feeds.keyword'], null=False))
        ))
        db.create_unique('feeds_search_keywords', ['search_id', 'keyword_id'])

        # Adding M2M table for field tweets on 'Search'
        db.create_table('feeds_search_tweets', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('search', models.ForeignKey(orm['feeds.search'], null=False)),
            ('tweet', models.ForeignKey(orm['feeds.tweet'], null=False))
        ))
        db.create_unique('feeds_search_tweets', ['search_id', 'tweet_id'])

        # Adding model 'Image'
        db.create_table('feeds_image', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('src', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('alt', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['feeds.Item'])),
        ))
        db.send_create_signal('feeds', ['Image'])

        # Adding model 'Filter'
        db.create_table('feeds_filter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('keywords', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('feeds', ['Filter'])


    def backwards(self, orm):
        # Deleting model 'Country'
        db.delete_table('feeds_country')

        # Deleting model 'Domain'
        db.delete_table('feeds_domain')

        # Deleting model 'Feed'
        db.delete_table('feeds_feed')

        # Deleting model 'Item'
        db.delete_table('feeds_item')

        # Deleting model 'Place'
        db.delete_table('feeds_place')

        # Deleting model 'Tweet'
        db.delete_table('feeds_tweet')

        # Removing M2M table for field places on 'Tweet'
        db.delete_table('feeds_tweet_places')

        # Deleting model 'Person'
        db.delete_table('feeds_person')

        # Removing M2M table for field tweets on 'Person'
        db.delete_table('feeds_person_tweets')

        # Deleting model 'Keyword'
        db.delete_table('feeds_keyword')

        # Deleting model 'Search'
        db.delete_table('feeds_search')

        # Removing M2M table for field keywords on 'Search'
        db.delete_table('feeds_search_keywords')

        # Removing M2M table for field tweets on 'Search'
        db.delete_table('feeds_search_tweets')

        # Deleting model 'Image'
        db.delete_table('feeds_image')

        # Deleting model 'Filter'
        db.delete_table('feeds_filter')


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
            'geometry': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'})
        },
        'feeds.search': {
            'Meta': {'ordering': "['name']", 'object_name': 'Search'},
            'geometry': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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