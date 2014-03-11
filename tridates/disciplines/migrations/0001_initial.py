# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Discipline'
        db.create_table('disciplines_discipline', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True)),
            ('parent_discipline', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['disciplines.Discipline'], null=True, blank=True)),
        ))
        db.send_create_signal('disciplines', ['Discipline'])


    def backwards(self, orm):
        
        # Deleting model 'Discipline'
        db.delete_table('disciplines_discipline')


    models = {
        'disciplines.discipline': {
            'Meta': {'object_name': 'Discipline'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'parent_discipline': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['disciplines.Discipline']", 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['disciplines']
