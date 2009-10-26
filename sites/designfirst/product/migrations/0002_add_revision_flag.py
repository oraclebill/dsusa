
from south.db import db
from django.db import models
from designfirst.product.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Invoice'
        db.create_table('product_invoice', (
            ('id', orm['product.invoice:id']),
            ('customer', orm['product.invoice:customer']),
            ('status', orm['product.invoice:status']),
            ('description', orm['product.invoice:description']),
            ('created', orm['product.invoice:created']),
        ))
        db.send_create_signal('product', ['Invoice'])
        
        # Adding model 'CartItem'
        db.create_table('product_cartitem', (
            ('id', orm['product.cartitem:id']),
            ('session_key', orm['product.cartitem:session_key']),
            ('product', orm['product.cartitem:product']),
            ('quantity', orm['product.cartitem:quantity']),
        ))
        db.send_create_signal('product', ['CartItem'])
        
        # Adding model 'InvoiceLine'
        db.create_table('product_invoiceline', (
            ('id', orm['product.invoiceline:id']),
            ('invoice', orm['product.invoiceline:invoice']),
            ('number', orm['product.invoiceline:number']),
            ('description', orm['product.invoiceline:description']),
            ('quantity', orm['product.invoiceline:quantity']),
            ('unit_price', orm['product.invoiceline:unit_price']),
            ('_unit_credit', orm['product.invoiceline:_unit_credit']),
        ))
        db.send_create_signal('product', ['InvoiceLine'])
        
        # Adding field 'Product.is_revision'
        db.add_column('product_product', 'is_revision', orm['product.product:is_revision'])
        
        # Deleting field 'Product.verbose_name'
        db.delete_column('product_product', 'verbose_name')
        
        # Changing field 'Product.name'
        # (to signature: django.db.models.fields.CharField(max_length=120))
        db.alter_column('product_product', 'name', orm['product.product:name'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Invoice'
        db.delete_table('product_invoice')
        
        # Deleting model 'CartItem'
        db.delete_table('product_cartitem')
        
        # Deleting model 'InvoiceLine'
        db.delete_table('product_invoiceline')
        
        # Deleting field 'Product.is_revision'
        db.delete_column('product_product', 'is_revision')
        
        # Adding field 'Product.verbose_name'
        db.add_column('product_product', 'verbose_name', orm['product.product:verbose_name'])
        
        # Changing field 'Product.name'
        # (to signature: django.db.models.fields.CharField(max_length=20))
        db.alter_column('product_product', 'name', orm['product.product:name'])
        
    
    
    models = {
        'home.dealerorganization': {
            'credit_balance': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            'default_measure_units': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'organization_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['home.Organization']", 'unique': 'True', 'primary_key': 'True'})
        },
        'home.organization': {
            'company_address_1': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'company_address_2': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'company_city': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'company_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'company_fax': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'company_phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'company_state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'company_zip4': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'ACT'", 'max_length': '3'})
        },
        'product.cartitem': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['product.Product']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {}),
            'session_key': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        'product.invoice': {
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['home.DealerOrganization']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'default': "'fac94f6ac21111dea6ff00254bb5eab6'", 'max_length': '50', 'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'product.invoiceline': {
            '_unit_credit': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['product.Invoice']"}),
            'number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {}),
            'unit_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'})
        },
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
            'is_revision': ('django.db.models.fields.NullBooleanField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'purchaseable': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '100'})
        }
    }
    
    complete_apps = ['product']
