
from south.db import db
from django.db import models
from designfirst.wizard.models import *

class Migration:
    
    def forwards(self, orm):
        
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
            ('celiling_height', orm['wizard.WorkingOrder:celiling_height']),
            ('crown_moulding_type', orm['wizard.WorkingOrder:crown_moulding_type']),
            ('skirt_moulding_type', orm['wizard.WorkingOrder:skirt_moulding_type']),
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
        
        # Deleting model 'AttachPreview'
        db.delete_table('wizard_attachpreview')
        
        # Deleting model 'Attachment'
        db.delete_table('wizard_attachment')
        
        # Deleting model 'WorkingOrder'
        db.delete_table('wizard_workingorder')
        
        # Deleting model 'Appliance'
        db.delete_table('wizard_appliance')
        
    
    
    models = {
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
            'celiling_height': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'client_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'corables': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'crown_moulding_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'degree90_corner_base': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'degree90_corner_base_shelv': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'degree90_corner_wall': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'depth': ('DimensionField', [], {'null': 'True', 'blank': 'True'}),
            'desired': ('django.db.models.fields.DateTimeField', [], {}),
            'diagonal_corner_base': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'diagonal_corner_base_shelv': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'diagonal_corner_wall': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'diagonal_corner_wall_shelv': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'dimension_style': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'door_handle_model': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'door_handle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'drawer_handle_model': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'drawer_handle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'glass_doors': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lazy_susan': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'leas_feet': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'plate_rack': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'posts': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'project_name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'range_hood': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'skirt_moulding_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'slide_out_trays': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'soffit_depth': ('DimensionField', ["'Depth'"], {'null': 'True', 'blank': 'True'}),
            'soffit_height': ('DimensionField', ["'Height'"], {'null': 'True', 'blank': 'True'}),
            'soffit_width': ('DimensionField', ["'Width'"], {'null': 'True', 'blank': 'True'}),
            'standard_sizes': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'valance': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'vanity_cabinet_height': ('DimensionField', [], {'null': 'True', 'blank': 'True'}),
            'wall_cabinet_height': ('DimensionField', [], {'null': 'True', 'blank': 'True'}),
            'waste_bin': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'wine_rack': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        }
    }
    
    complete_apps = ['wizard']
