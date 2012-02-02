# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Region'
        db.create_table('regions_region', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('parent_region', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['regions.Region'], null=True, blank=True)),
        ))
        db.send_create_signal('regions', ['Region'])


    def backwards(self, orm):
        
        # Deleting model 'Region'
        db.delete_table('regions_region')


    models = {
        'regions.region': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Region'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'parent_region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['regions.Region']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['regions']
