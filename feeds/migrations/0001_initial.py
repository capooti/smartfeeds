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

        # Adding M2M table for field item on 'Place'
        db.create_table('feeds_place_item', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('place', models.ForeignKey(orm['feeds.place'], null=False)),
            ('item', models.ForeignKey(orm['feeds.item'], null=False))
        ))
        db.create_unique('feeds_place_item', ['place_id', 'item_id'])

        # Adding model 'Person'
        db.create_table('feeds_person', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
        ))
        db.send_create_signal('feeds', ['Person'])

        # Adding M2M table for field item on 'Person'
        db.create_table('feeds_person_item', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm['feeds.person'], null=False)),
            ('item', models.ForeignKey(orm['feeds.item'], null=False))
        ))
        db.create_unique('feeds_person_item', ['person_id', 'item_id'])

        # Adding model 'Keyword'
        db.create_table('feeds_keyword', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
        ))
        db.send_create_signal('feeds', ['Keyword'])

        # Adding M2M table for field item on 'Keyword'
        db.create_table('feeds_keyword_item', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('keyword', models.ForeignKey(orm['feeds.keyword'], null=False)),
            ('item', models.ForeignKey(orm['feeds.item'], null=False))
        ))
        db.create_unique('feeds_keyword_item', ['keyword_id', 'item_id'])

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

        # Removing M2M table for field item on 'Place'
        db.delete_table('feeds_place_item')

        # Deleting model 'Person'
        db.delete_table('feeds_person')

        # Removing M2M table for field item on 'Person'
        db.delete_table('feeds_person_item')

        # Deleting model 'Keyword'
        db.delete_table('feeds_keyword')

        # Removing M2M table for field item on 'Keyword'
        db.delete_table('feeds_keyword_item')

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
            'item': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['feeds.Item']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'})
        },
        'feeds.person': {
            'Meta': {'ordering': "['name']", 'object_name': 'Person'},
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['feeds.Item']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'})
        },
        'feeds.place': {
            'Meta': {'object_name': 'Place'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feeds.Country']", 'null': 'True'}),
            'geometry': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['feeds.Item']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'})
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