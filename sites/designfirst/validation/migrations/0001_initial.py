
from south.db import db
from django.db import models
from validation.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'ProductLine'
        db.create_table('validation_productline', (
            ('name', orm['validation.ProductLine:name']),
            ('manufacturer', orm['validation.ProductLine:manufacturer']),
        ))
        db.send_create_signal('validation', ['ProductLine'])
        
        # Adding model 'FinishOption'
        db.create_table('validation_finishoption', (
            ('name', orm['validation.FinishOption:name']),
            ('manufacturer', orm['validation.FinishOption:manufacturer']),
            ('product_line', orm['validation.FinishOption:product_line']),
            ('image', orm['validation.FinishOption:image']),
        ))
        db.send_create_signal('validation', ['FinishOption'])
        
        # Adding model 'GeneralOption'
        db.create_table('validation_generaloption', (
            ('name', orm['validation.GeneralOption:name']),
            ('type', orm['validation.GeneralOption:type']),
            ('description', orm['validation.GeneralOption:description']),
            ('manufacturer', orm['validation.GeneralOption:manufacturer']),
            ('product_line', orm['validation.GeneralOption:product_line']),
            ('image', orm['validation.GeneralOption:image']),
        ))
        db.send_create_signal('validation', ['GeneralOption'])
        
        # Adding model 'DoorStyle'
        db.create_table('validation_doorstyle', (
            ('name', orm['validation.DoorStyle:name']),
            ('manufacturer', orm['validation.DoorStyle:manufacturer']),
            ('product_line', orm['validation.DoorStyle:product_line']),
            ('thumbnail', orm['validation.DoorStyle:thumbnail']),
            ('image', orm['validation.DoorStyle:image']),
        ))
        db.send_create_signal('validation', ['DoorStyle'])
        
        # Adding model 'Manufacturer'
        db.create_table('validation_manufacturer', (
            ('name', orm['validation.Manufacturer:name']),
            ('small_logo', orm['validation.Manufacturer:small_logo']),
            ('large_logo', orm['validation.Manufacturer:large_logo']),
        ))
        db.send_create_signal('validation', ['Manufacturer'])
        
        # Adding model 'WoodOption'
        db.create_table('validation_woodoption', (
            ('name', orm['validation.WoodOption:name']),
            ('manufacturer', orm['validation.WoodOption:manufacturer']),
            ('product_line', orm['validation.WoodOption:product_line']),
            ('image', orm['validation.WoodOption:image']),
        ))
        db.send_create_signal('validation', ['WoodOption'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'ProductLine'
        db.delete_table('validation_productline')
        
        # Deleting model 'FinishOption'
        db.delete_table('validation_finishoption')
        
        # Deleting model 'GeneralOption'
        db.delete_table('validation_generaloption')
        
        # Deleting model 'DoorStyle'
        db.delete_table('validation_doorstyle')
        
        # Deleting model 'Manufacturer'
        db.delete_table('validation_manufacturer')
        
        # Deleting model 'WoodOption'
        db.delete_table('validation_woodoption')
        
    
    
    models = {
        'validation.doorstyle': {
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['validation.Manufacturer']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'primary_key': 'True'}),
            'product_line': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['validation.ProductLine']", 'null': 'True', 'blank': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'validation.finishoption': {
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['validation.Manufacturer']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'primary_key': 'True'}),
            'product_line': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['validation.ProductLine']", 'null': 'True', 'blank': 'True'})
        },
        'validation.generaloption': {
            'description': ('django.db.models.fields.TextField', [], {'max_length': '30'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['validation.Manufacturer']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'primary_key': 'True'}),
            'product_line': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['validation.ProductLine']", 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'validation.manufacturer': {
            'large_logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'primary_key': 'True'}),
            'small_logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'})
        },
        'validation.productline': {
            'manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['validation.Manufacturer']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'primary_key': 'True'})
        },
        'validation.woodoption': {
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'manufacturer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['validation.Manufacturer']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'primary_key': 'True'}),
            'product_line': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['validation.ProductLine']", 'null': 'True', 'blank': 'True'})
        }
    }
    
    complete_apps = ['validation']
