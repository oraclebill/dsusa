
from south.db import db
from django.db import models
from ordermgr.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Invoice'
        db.create_table('ordermgr_invoice', (
            ('id', orm['ordermgr.invoice:id']),
            ('start_date', orm['ordermgr.invoice:start_date']),
            ('end_date', orm['ordermgr.invoice:end_date']),
            ('generated_on', orm['ordermgr.invoice:generated_on']),
            ('owner', orm['ordermgr.invoice:owner']),
        ))
        db.send_create_signal('ordermgr', ['Invoice'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Invoice'
        db.delete_table('ordermgr_invoice')
        
    
    
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
        'ordermgr.designorder': {
            'arrived': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'color_views': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'completed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'designer': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'elevations': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'final_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'kit_file': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'quote_cabinet_list': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'rush': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'source_id': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'})
        },
        'ordermgr.designorderevent': {
            'actor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'event_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ordermgr.DesignOrder']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'ordermgr.designpackage': {
            'delivered': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kitfile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attachments'", 'to': "orm['ordermgr.DesignOrder']"}),
            'price_report': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'views_archive': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'ordermgr.invoice': {
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'generated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        'ordermgr.kitchendesignrequest': {
            'appliance_garage': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'backsplash': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'base_corner_cabinet': ('django.db.models.fields.CharField', [], {'default': "'ANY'", 'max_length': '5'}),
            'base_corner_cabinet_opening': ('django.db.models.fields.CharField', [], {'default': "'ANY'", 'max_length': '5'}),
            'base_corner_cabinet_shelving': ('django.db.models.fields.CharField', [], {'default': "'ANY'", 'max_length': '15'}),
            'bottom_moulding_1': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'bottom_moulding_2': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'bottom_moulding_3': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'cabinet_door_style': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'cabinet_finish': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'cabinet_finish_options': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'cabinet_manufacturer': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'cabinet_stain': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'cabinet_wood': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'cabinetry_notes': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'ceiling_height': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'corbels_brackets': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'countertop_option': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'designorder_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['ordermgr.DesignOrder']", 'unique': 'True', 'primary_key': 'True'}),
            'door_hardware_model': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'door_hardware_type': ('django.db.models.fields.CharField', [], {'default': "'ANY'", 'max_length': "'5'"}),
            'drawer_hardware_model': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'drawer_hardware_type': ('django.db.models.fields.CharField', [], {'default': "'ANY'", 'max_length': "'5'"}),
            'glass_doors': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'island_peninsula_option': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '1'}),
            'lazy_susan': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'legs_feet': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'plate_rack': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'posts': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'range_hood': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'slide_out_trays': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'soffit_depth': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'soffit_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'soffit_width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'soffits': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'stacked_staggered': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'toekick': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'top_moulding_1': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'top_moulding_2': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'top_moulding_3': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'user_sketch': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'valance': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'vanity_cabinet_depth': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'vanity_cabinet_height': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'wall_cabinet_height': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'wall_corner_cabinet': ('django.db.models.fields.CharField', [], {'default': "'ANY'", 'max_length': '5'}),
            'wall_corner_cabinet_opening': ('django.db.models.fields.CharField', [], {'default': "'ANY'", 'max_length': '5'}),
            'wall_corner_cabinet_shelving': ('django.db.models.fields.CharField', [], {'default': "'ANY'", 'max_length': '15'}),
            'waste_bin': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'wine_rack': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        },
        'ordermgr.userprofile': {
            'is_manager': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_notified': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'user': ('AutoOneToOneField', ["orm['auth.User']"], {'related_name': "'order_profile'", 'primary_key': 'True'})
        }
    }
    
    complete_apps = ['ordermgr']
