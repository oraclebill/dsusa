
from south.db import db
from django.db import models
from designfirst.wizard.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Moulding'
        db.create_table('wizard_moulding', (
            ('id', orm['wizard.Moulding:id']),
            ('order', orm['wizard.Moulding:order']),
            ('num', orm['wizard.Moulding:num']),
            ('type', orm['wizard.Moulding:type']),
            ('name', orm['wizard.Moulding:name']),
        ))
        db.send_create_signal('wizard', ['Moulding'])
        
        # Adding model 'AttachPreview'
        db.create_table('wizard_attachpreview', (
            ('id', orm['wizard.AttachPreview:id']),
            ('attachment', orm['wizard.AttachPreview:attachment']),
            ('page', orm['wizard.AttachPreview:page']),
            ('file', orm['wizard.AttachPreview:file']),
        ))
        db.send_create_signal('wizard', ['AttachPreview'])
        
        # Adding model 'Attachment'
        db.create_table('wizard_attachment', (
            ('id', orm['wizard.Attachment:id']),
            ('order', orm['wizard.Attachment:order']),
            ('type', orm['wizard.Attachment:type']),
            ('file', orm['wizard.Attachment:file']),
            ('timestamp', orm['wizard.Attachment:timestamp']),
        ))
        db.send_create_signal('wizard', ['Attachment'])
        
        # Adding model 'WorkingOrder'
        db.create_table('wizard_workingorder', (
            ('id', orm['wizard.WorkingOrder:id']),
            ('owner', orm['wizard.WorkingOrder:owner']),
            ('status', orm['wizard.WorkingOrder:status']),
            ('color_views', orm['wizard.WorkingOrder:color_views']),
            ('elevations', orm['wizard.WorkingOrder:elevations']),
            ('quoted_cabinet_list', orm['wizard.WorkingOrder:quoted_cabinet_list']),
            ('project_name', orm['wizard.WorkingOrder:project_name']),
            ('desired', orm['wizard.WorkingOrder:desired']),
            ('cost', orm['wizard.WorkingOrder:cost']),
            ('client_notes', orm['wizard.WorkingOrder:client_notes']),
            ('cabinet_manufacturer', orm['wizard.WorkingOrder:cabinet_manufacturer']),
            ('cabinet_product_line', orm['wizard.WorkingOrder:cabinet_product_line']),
            ('cabinet_door_style', orm['wizard.WorkingOrder:cabinet_door_style']),
            ('cabinet_wood', orm['wizard.WorkingOrder:cabinet_wood']),
            ('cabinet_finish', orm['wizard.WorkingOrder:cabinet_finish']),
            ('cabinet_finish_options', orm['wizard.WorkingOrder:cabinet_finish_options']),
            ('cabinetry_notes', orm['wizard.WorkingOrder:cabinetry_notes']),
            ('door_handle_type', orm['wizard.WorkingOrder:door_handle_type']),
            ('door_handle_model', orm['wizard.WorkingOrder:door_handle_model']),
            ('drawer_handle_type', orm['wizard.WorkingOrder:drawer_handle_type']),
            ('drawer_handle_model', orm['wizard.WorkingOrder:drawer_handle_model']),
            ('soffit_width', orm['wizard.WorkingOrder:soffit_width']),
            ('soffit_height', orm['wizard.WorkingOrder:soffit_height']),
            ('soffit_depth', orm['wizard.WorkingOrder:soffit_depth']),
            ('dimension_style', orm['wizard.WorkingOrder:dimension_style']),
            ('standard_sizes', orm['wizard.WorkingOrder:standard_sizes']),
            ('wall_cabinet_height', orm['wizard.WorkingOrder:wall_cabinet_height']),
            ('vanity_cabinet_height', orm['wizard.WorkingOrder:vanity_cabinet_height']),
            ('depth', orm['wizard.WorkingOrder:depth']),
            ('diagonal_corner_base', orm['wizard.WorkingOrder:diagonal_corner_base']),
            ('diagonal_corner_base_shelv', orm['wizard.WorkingOrder:diagonal_corner_base_shelv']),
            ('diagonal_corner_wall', orm['wizard.WorkingOrder:diagonal_corner_wall']),
            ('diagonal_corner_wall_shelv', orm['wizard.WorkingOrder:diagonal_corner_wall_shelv']),
            ('degree90_corner_base', orm['wizard.WorkingOrder:degree90_corner_base']),
            ('degree90_corner_base_shelv', orm['wizard.WorkingOrder:degree90_corner_base_shelv']),
            ('degree90_corner_wall', orm['wizard.WorkingOrder:degree90_corner_wall']),
            ('lazy_susan', orm['wizard.WorkingOrder:lazy_susan']),
            ('slide_out_trays', orm['wizard.WorkingOrder:slide_out_trays']),
            ('waste_bin', orm['wizard.WorkingOrder:waste_bin']),
            ('wine_rack', orm['wizard.WorkingOrder:wine_rack']),
            ('plate_rack', orm['wizard.WorkingOrder:plate_rack']),
            ('apliance_garage', orm['wizard.WorkingOrder:apliance_garage']),
            ('corables', orm['wizard.WorkingOrder:corables']),
            ('brackets', orm['wizard.WorkingOrder:brackets']),
            ('valance', orm['wizard.WorkingOrder:valance']),
            ('leas_feet', orm['wizard.WorkingOrder:leas_feet']),
            ('glass_doors', orm['wizard.WorkingOrder:glass_doors']),
            ('range_hood', orm['wizard.WorkingOrder:range_hood']),
            ('posts', orm['wizard.WorkingOrder:posts']),
        ))
        db.send_create_signal('wizard', ['WorkingOrder'])
        
        # Adding model 'Appliance'
        db.create_table('wizard_appliance', (
            ('id', orm['wizard.Appliance:id']),
            ('order', orm['wizard.Appliance:order']),
            ('type', orm['wizard.Appliance:type']),
            ('description', orm['wizard.Appliance:description']),
            ('width', orm['wizard.Appliance:width']),
            ('height', orm['wizard.Appliance:height']),
            ('depth', orm['wizard.Appliance:depth']),
        ))
        db.send_create_signal('wizard', ['Appliance'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Moulding'
        db.delete_table('wizard_moulding')
        
        # Deleting model 'AttachPreview'
        db.delete_table('wizard_attachpreview')
        
        # Deleting model 'Attachment'
        db.delete_table('wizard_attachment')
        
        # Deleting model 'WorkingOrder'
        db.delete_table('wizard_workingorder')
        
        # Deleting model 'Appliance'
        db.delete_table('wizard_appliance')
        
    
    
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
        'wizard.appliance': {
            'depth': ('DimensionField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'height': ('DimensionField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wizard.WorkingOrder']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'width': ('DimensionField', [], {'null': 'True', 'blank': 'True'})
        },
        'wizard.attachment': {
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attachments'", 'to': "orm['wizard.WorkingOrder']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'wizard.attachpreview': {
            'attachment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wizard.Attachment']"}),
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'wizard.moulding': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'num': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mouldings'", 'to': "orm['wizard.WorkingOrder']"}),
            'type': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'wizard.workingorder': {
            'apliance_garage': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'brackets': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'cabinet_door_style': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'cabinet_finish': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'cabinet_finish_options': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'cabinet_manufacturer': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'cabinet_product_line': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'cabinet_wood': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'cabinetry_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'client_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'color_views': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'corables': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'degree90_corner_base': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'degree90_corner_base_shelv': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'degree90_corner_wall': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'depth': ('DimensionField', [], {'null': 'True', 'blank': 'True'}),
            'desired': ('django.db.models.fields.DateTimeField', [], {}),
            'diagonal_corner_base': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'diagonal_corner_base_shelv': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'diagonal_corner_wall': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'diagonal_corner_wall_shelv': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'dimension_style': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'door_handle_model': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'door_handle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'drawer_handle_model': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'drawer_handle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'elevations': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'glass_doors': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lazy_susan': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'leas_feet': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'plate_rack': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'posts': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'project_name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'quoted_cabinet_list': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'range_hood': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'slide_out_trays': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'soffit_depth': ('DimensionField', ["'Depth'"], {'null': 'True', 'blank': 'True'}),
            'soffit_height': ('DimensionField', ["'Height'"], {'null': 'True', 'blank': 'True'}),
            'soffit_width': ('DimensionField', ["'Width'"], {'null': 'True', 'blank': 'True'}),
            'standard_sizes': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'valance': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'vanity_cabinet_height': ('DimensionField', [], {'null': 'True', 'blank': 'True'}),
            'wall_cabinet_height': ('DimensionField', [], {'null': 'True', 'blank': 'True'}),
            'waste_bin': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'wine_rack': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        }
    }
    
    complete_apps = ['wizard']
