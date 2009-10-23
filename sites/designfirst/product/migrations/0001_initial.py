
from south.db import db
from django.db import models
from designfirst.product.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Product'
        db.create_table('product_product', (
            ('id', orm['product.Product:id']),
            ('name', orm['product.Product:name']),
            ('verbose_name', orm['product.Product:verbose_name']),
            ('description', orm['product.Product:description']),
            ('sort_order', orm['product.Product:sort_order']),
            ('base_price', orm['product.Product:base_price']),
            ('credit_value', orm['product.Product:credit_value']),
            ('purchaseable', orm['product.Product:purchaseable']),
            ('debitable', orm['product.Product:debitable']),
        ))
        db.send_create_signal('product', ['Product'])
        
        # Adding model 'PriceSchedule'
        db.create_table('product_priceschedule', (
            ('id', orm['product.PriceSchedule:id']),
            ('name', orm['product.PriceSchedule:name']),
            ('description', orm['product.PriceSchedule:description']),
            ('is_default', orm['product.PriceSchedule:is_default']),
        ))
        db.send_create_signal('product', ['PriceSchedule'])
        
        # Adding model 'PriceScheduleEntry'
        db.create_table('product_pricescheduleentry', (
            ('id', orm['product.PriceScheduleEntry:id']),
            ('price_sheet', orm['product.PriceScheduleEntry:price_sheet']),
            ('product', orm['product.PriceScheduleEntry:product']),
            ('retail_price', orm['product.PriceScheduleEntry:retail_price']),
        ))
        db.send_create_signal('product', ['PriceScheduleEntry'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Product'
        db.delete_table('product_product')
        
        # Deleting model 'PriceSchedule'
        db.delete_table('product_priceschedule')
        
        # Deleting model 'PriceScheduleEntry'
        db.delete_table('product_pricescheduleentry')
        
    
    
    models = {
        'product.priceschedule': {
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'product.pricescheduleentry': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price_sheet': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['product.PriceSchedule']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['product.Product']"}),
            'retail_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'})
        },
        'product.product': {
            'base_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'credit_value': ('django.db.models.fields.SmallIntegerField', [], {}),
            'debitable': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'purchaseable': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'verbose_name': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        }
    }
    
    complete_apps = ['product']
