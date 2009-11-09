
from south.db import db
from django.db import models
from designfirst.customer.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'UserProfile.last_name'
        db.add_column('customer_userprofile', 'last_name', orm['customer.userprofile:last_name'])
        
        # Adding field 'UserProfile.first_name'
        db.add_column('customer_userprofile', 'first_name', orm['customer.userprofile:first_name'])
        
        # Adding field 'UserProfile.id'
        db.add_column('customer_userprofile', 'id', orm['customer.userprofile:id'])
        
        # Adding field 'UserProfile.email'
        db.add_column('customer_userprofile', 'email', orm['customer.userprofile:email'])
        
        # Changing field 'Dealer.internal_name'
        # (to signature: django.db.models.fields.SlugField(db_index=True, max_length=50, blank=True))
        db.alter_column('customer_dealer', 'internal_name', orm['customer.dealer:internal_name'])
        
        # Changing field 'Invoice.id'
        # (to signature: django.db.models.fields.CharField(default='4e6994daccb311deb92c0026b0f0d09c', max_length=50, primary_key=True))
        db.alter_column('customer_invoice', 'id', orm['customer.invoice:id'])
        
        # Changing field 'UserProfile.user'
        # (to signature: django.db.models.fields.related.ForeignKey(to=orm['auth.User'], unique=True, null=True, blank=True))
        db.alter_column('customer_userprofile', 'user_id', orm['customer.userprofile:user'])
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'UserProfile.last_name'
        db.delete_column('customer_userprofile', 'last_name')
        
        # Deleting field 'UserProfile.first_name'
        db.delete_column('customer_userprofile', 'first_name')
        
        # Deleting field 'UserProfile.id'
        db.delete_column('customer_userprofile', 'id')
        
        # Deleting field 'UserProfile.email'
        db.delete_column('customer_userprofile', 'email')
        
        # Changing field 'Dealer.internal_name'
        # (to signature: django.db.models.fields.SlugField(max_length=50, db_index=True))
        db.alter_column('customer_dealer', 'internal_name', orm['customer.dealer:internal_name'])
        
        # Changing field 'Invoice.id'
        # (to signature: django.db.models.fields.CharField(default='c9722d88c85111deb69900264a074028', max_length=50, primary_key=True))
        db.alter_column('customer_invoice', 'id', orm['customer.invoice:id'])
        
        # Changing field 'UserProfile.user'
        # (to signature: django.db.models.fields.related.ForeignKey(to=orm['auth.User'], unique=True, primary_key=True))
        db.alter_column('customer_userprofile', 'user_id', orm['customer.userprofile:user'])
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'customer.dealer': {
            'account_rep': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'rep_for_dealers'", 'null': 'True', 'to': "orm['auth.User']"}),
            'account_rep_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'address_1': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'address_2': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'credit_balance': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_name': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'legal_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'notes': ('django.db.models.fields.TextField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'num_locations': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'P'", 'max_length': '1'}),
            'zip4': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        'customer.invoice': {
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['customer.Dealer']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'default': "'4eb5409cccb311deb92c0026b0f0d09c'", 'max_length': '50', 'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'customer.invoiceline': {
            '_unit_credit': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lines'", 'to': "orm['customer.Invoice']"}),
            'number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {}),
            'unit_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'})
        },
        'customer.userprofile': {
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['customer.Dealer']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'primary': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True', 'null': 'True', 'blank': 'True'})
        }
    }
    
    complete_apps = ['customer']
