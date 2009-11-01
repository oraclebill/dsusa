
from south.db import db
from django.db import models
from designfirst.customer.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'OrderNotes'
        db.create_table('home_ordernotes', (
            ('id', orm['customer.OrderNotes:id']),
            ('order', orm['customer.OrderNotes:order']),
            ('sequence', orm['customer.OrderNotes:sequence']),
            ('created', orm['customer.OrderNotes:created']),
        ))
        db.send_create_signal('home', ['OrderNotes'])
        
        # Adding model 'DesignOrder'
        db.create_table('home_designorder', (
            ('id', orm['customer.DesignOrder:id']),
            ('client_account', orm['customer.DesignOrder:client_account']),
            ('project_name', orm['customer.DesignOrder:project_name']),
            ('description', orm['customer.DesignOrder:description']),
            ('status', orm['customer.DesignOrder:status']),
            ('cost', orm['customer.DesignOrder:cost']),
            ('designer', orm['customer.DesignOrder:designer']),
            ('color_views', orm['customer.DesignOrder:color_views']),
            ('elevations', orm['customer.DesignOrder:elevations']),
            ('quote_cabinet_list', orm['customer.DesignOrder:quote_cabinet_list']),
            ('cabinet_manufacturer', orm['customer.DesignOrder:cabinet_manufacturer']),
            ('cabinet_door_style', orm['customer.DesignOrder:cabinet_door_style']),
            ('cabinet_wood', orm['customer.DesignOrder:cabinet_wood']),
            ('cabinet_stain', orm['customer.DesignOrder:cabinet_stain']),
            ('cabinet_finish', orm['customer.DesignOrder:cabinet_finish']),
            ('cabinet_finish_options', orm['customer.DesignOrder:cabinet_finish_options']),
            ('cabinetry_notes', orm['customer.DesignOrder:cabinetry_notes']),
            ('include_hardware', orm['customer.DesignOrder:include_hardware']),
            ('door_hardware', orm['customer.DesignOrder:door_hardware']),
            ('drawer_hardware', orm['customer.DesignOrder:drawer_hardware']),
            ('ceiling_height', orm['customer.DesignOrder:ceiling_height']),
            ('crown_mouldings', orm['customer.DesignOrder:crown_mouldings']),
            ('skirt_mouldings', orm['customer.DesignOrder:skirt_mouldings']),
            ('soffits', orm['customer.DesignOrder:soffits']),
            ('soffit_height', orm['customer.DesignOrder:soffit_height']),
            ('soffit_width', orm['customer.DesignOrder:soffit_width']),
            ('soffit_depth', orm['customer.DesignOrder:soffit_depth']),
            ('stacked_staggered', orm['customer.DesignOrder:stacked_staggered']),
            ('wall_cabinet_height', orm['customer.DesignOrder:wall_cabinet_height']),
            ('vanity_cabinet_height', orm['customer.DesignOrder:vanity_cabinet_height']),
            ('vanity_cabinet_depth', orm['customer.DesignOrder:vanity_cabinet_depth']),
            ('corner_cabinet_base_bc', orm['customer.DesignOrder:corner_cabinet_base_bc']),
            ('corner_cabinet_base_bc_direction', orm['customer.DesignOrder:corner_cabinet_base_bc_direction']),
            ('corner_cabinet_wall_bc', orm['customer.DesignOrder:corner_cabinet_wall_bc']),
            ('corner_cabinet_wall_bc_direction', orm['customer.DesignOrder:corner_cabinet_wall_bc_direction']),
            ('island_peninsula_option', orm['customer.DesignOrder:island_peninsula_option']),
            ('countertop_option', orm['customer.DesignOrder:countertop_option']),
            ('backsplash', orm['customer.DesignOrder:backsplash']),
            ('toekick', orm['customer.DesignOrder:toekick']),
            ('lazy_susan', orm['customer.DesignOrder:lazy_susan']),
            ('slide_out_trays', orm['customer.DesignOrder:slide_out_trays']),
            ('waste_bin', orm['customer.DesignOrder:waste_bin']),
            ('wine_rack', orm['customer.DesignOrder:wine_rack']),
            ('plate_rack', orm['customer.DesignOrder:plate_rack']),
            ('appliance_garage', orm['customer.DesignOrder:appliance_garage']),
            ('corbels_brackets', orm['customer.DesignOrder:corbels_brackets']),
            ('valance', orm['customer.DesignOrder:valance']),
            ('legs_feet', orm['customer.DesignOrder:legs_feet']),
            ('glass_doors', orm['customer.DesignOrder:glass_doors']),
            ('range_hood', orm['customer.DesignOrder:range_hood']),
            ('posts', orm['customer.DesignOrder:posts']),
            ('miscellaneous_notes', orm['customer.DesignOrder:miscellaneous_notes']),
            ('client_diagram', orm['customer.DesignOrder:client_diagram']),
            ('client_diagram_source', orm['customer.DesignOrder:client_diagram_source']),
            ('client_diagram_notes', orm['customer.DesignOrder:client_diagram_notes']),
            ('designer_package', orm['customer.DesignOrder:designer_package']),
            ('designer_package_notes', orm['customer.DesignOrder:designer_package_notes']),
            ('client_review_rating', orm['customer.DesignOrder:client_review_rating']),
            ('client_review_notes', orm['customer.DesignOrder:client_review_notes']),
            ('client_notes', orm['customer.DesignOrder:client_notes']),
            ('designer_notes', orm['customer.DesignOrder:designer_notes']),
            ('created', orm['customer.DesignOrder:created']),
            ('modified', orm['customer.DesignOrder:modified']),
            ('modified_by', orm['customer.DesignOrder:modified_by']),
            ('visited_status', orm['customer.DesignOrder:visited_status']),
            ('valid_status', orm['customer.DesignOrder:valid_status']),
            ('desired', orm['customer.DesignOrder:desired']),
            ('submitted', orm['customer.DesignOrder:submitted']),
            ('assigned', orm['customer.DesignOrder:assigned']),
            ('projected', orm['customer.DesignOrder:projected']),
            ('completed', orm['customer.DesignOrder:completed']),
            ('closed', orm['customer.DesignOrder:closed']),
            ('tracking_notes', orm['customer.DesignOrder:tracking_notes']),
        ))
        db.send_create_signal('home', ['DesignOrder'])
        
        # Adding model 'Transaction'
        db.create_table('home_transaction', (
            ('id', orm['customer.Transaction:id']),
            ('trace_id', orm['customer.Transaction:trace_id']),
            ('account', orm['customer.Transaction:account']),
            ('debit_or_credit', orm['customer.Transaction:debit_or_credit']),
            ('trans_type', orm['customer.Transaction:trans_type']),
            ('amount', orm['customer.Transaction:amount']),
            ('description', orm['customer.Transaction:description']),
            ('timestamp', orm['customer.Transaction:timestamp']),
        ))
        db.send_create_signal('home', ['Transaction'])
        
        # Adding model 'OrderAttachment'
        db.create_table('home_orderattachment', (
            ('id', orm['customer.OrderAttachment:id']),
            ('document_id', orm['customer.OrderAttachment:document_id']),
            ('document', orm['customer.OrderAttachment:document']),
            ('order', orm['customer.OrderAttachment:order']),
            ('source', orm['customer.OrderAttachment:source']),
            ('doctype', orm['customer.OrderAttachment:doctype']),
            ('method', orm['customer.OrderAttachment:method']),
            ('user', orm['customer.OrderAttachment:user']),
            ('org', orm['customer.OrderAttachment:org']),
            ('timestamp', orm['customer.OrderAttachment:timestamp']),
        ))
        db.send_create_signal('home', ['OrderAttachment'])
        
        # Adding model 'Organization'
        db.create_table('home_organization', (
            ('id', orm['customer.Organization:id']),
            ('status', orm['customer.Organization:status']),
            ('legal_name', orm['customer.Organization:legal_name']),
            ('address_1', orm['customer.Organization:address_1']),
            ('address_2', orm['customer.Organization:address_2']),
            ('city', orm['customer.Organization:city']),
            ('state', orm['customer.Organization:state']),
            ('zip4', orm['customer.Organization:zip4']),
            ('phone', orm['customer.Organization:phone']),
            ('fax', orm['customer.Organization:fax']),
            ('email', orm['customer.Organization:email']),
        ))
        db.send_create_signal('home', ['Organization'])
        
        # Adding model 'OrderAppliance'
        db.create_table('home_orderappliance', (
            ('id', orm['customer.OrderAppliance:id']),
            ('order', orm['customer.OrderAppliance:order']),
            ('appliance_type', orm['customer.OrderAppliance:appliance_type']),
            ('description', orm['customer.OrderAppliance:description']),
            ('height', orm['customer.OrderAppliance:height']),
            ('width', orm['customer.OrderAppliance:width']),
            ('depth', orm['customer.OrderAppliance:depth']),
            ('options', orm['customer.OrderAppliance:options']),
        ))
        db.send_create_signal('home', ['OrderAppliance'])
        
        # Adding model 'DealerOrganization'
        db.create_table('home_dealerorganization', (
            ('organization_ptr', orm['customer.DealerOrganization:organization_ptr']),
            ('default_measure_units', orm['customer.DealerOrganization:default_measure_units']),
            ('credit_balance', orm['customer.DealerOrganization:credit_balance']),
        ))
        db.send_create_signal('home', ['DealerOrganization'])
        
        # Adding model 'UserProfile'
        db.create_table('home_userprofile', (
            ('id', orm['customer.UserProfile:id']),
            ('user', orm['customer.UserProfile:user']),
            ('account', orm['customer.UserProfile:account']),
            ('usertype', orm['customer.UserProfile:usertype']),
        ))
        db.send_create_signal('home', ['UserProfile'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'OrderNotes'
        db.delete_table('home_ordernotes')
        
        # Deleting model 'DesignOrder'
        db.delete_table('home_designorder')
        
        # Deleting model 'Transaction'
        db.delete_table('home_transaction')
        
        # Deleting model 'OrderAttachment'
        db.delete_table('home_orderattachment')
        
        # Deleting model 'Organization'
        db.delete_table('home_organization')
        
        # Deleting model 'OrderAppliance'
        db.delete_table('home_orderappliance')
        
        # Deleting model 'DealerOrganization'
        db.delete_table('home_dealerorganization')
        
        # Deleting model 'UserProfile'
        db.delete_table('home_userprofile')
        
    
    
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
        'customer.dealerorganization': {
            'credit_balance': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            'default_measure_units': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'organization_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['customer.Organization']", 'unique': 'True', 'primary_key': 'True'})
        },
        'customer.designorder': {
            'appliance_garage': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'assigned': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'backsplash': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'cabinet_door_style': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'cabinet_finish': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'cabinet_finish_options': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'cabinet_manufacturer': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'cabinet_stain': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'cabinet_wood': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'cabinetry_notes': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'ceiling_height': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'client_account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'created_orders'", 'to': "orm['customer.Organization']"}),
            'client_diagram': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'client_diagram_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'client_diagram_source': ('django.db.models.fields.CharField', [], {'default': "'UPL'", 'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'client_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'client_review_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'client_review_rating': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'closed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'color_views': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'completed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'corbels_brackets': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'corner_cabinet_base_bc': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'corner_cabinet_base_bc_direction': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'corner_cabinet_wall_bc': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'corner_cabinet_wall_bc_direction': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'cost': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'countertop_option': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'crown_mouldings': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'designer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'serviced_orders'", 'null': 'True', 'to': "orm['auth.User']"}),
            'designer_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'designer_package': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'designer_package_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'desired': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'door_hardware': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'drawer_hardware': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'elevations': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'glass_doors': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'include_hardware': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'island_peninsula_option': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'lazy_susan': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'legs_feet': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'miscellaneous_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'modified_by': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'plate_rack': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'posts': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'project_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'projected': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'quote_cabinet_list': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'range_hood': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'skirt_mouldings': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'slide_out_trays': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'soffit_depth': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'soffit_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'soffit_width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'soffits': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'stacked_staggered': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'DLR'", 'max_length': '3'}),
            'submitted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'toekick': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'tracking_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'valance': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'valid_status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'vanity_cabinet_depth': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'vanity_cabinet_height': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'visited_status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'wall_cabinet_height': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'waste_bin': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'wine_rack': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        },
        'customer.orderappliance': {
            'appliance_type': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'depth': ('django.db.models.fields.IntegerField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'options': ('django.db.models.fields.CharField', [], {'max_length': '240', 'blank': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['customer.DesignOrder']"}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        },
        'customer.orderattachment': {
            'doctype': ('django.db.models.fields.SmallIntegerField', [], {}),
            'document': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'document_id': ('django.db.models.fields.CharField', [], {'max_length': '24', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.SmallIntegerField', [], {}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['customer.DesignOrder']", 'null': 'True', 'blank': 'True'}),
            'org': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['customer.Organization']", 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.SmallIntegerField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'customer.ordernotes': {
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['customer.DesignOrder']"}),
            'sequence': ('django.db.models.fields.IntegerField', [], {})
        },
        'customer.organization': {
            'address_1': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'address_2': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'legal_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'zip4': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'ACT'", 'max_length': '3'})
        },
        'customer.transaction': {
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['customer.DealerOrganization']"}),
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'debit_or_credit': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'trace_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'trans_type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'customer.userprofile': {
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['customer.Organization']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'usertype': ('django.db.models.fields.CharField', [], {'default': "'dealer'", 'max_length': '10'})
        }
    }
    
    complete_apps = ['home']
