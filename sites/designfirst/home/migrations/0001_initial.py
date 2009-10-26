
from south.db import db
from django.db import models
from designfirst.home.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'OrderNotes'
        db.create_table('home_ordernotes', (
            ('id', orm['home.OrderNotes:id']),
            ('order', orm['home.OrderNotes:order']),
            ('sequence', orm['home.OrderNotes:sequence']),
            ('created', orm['home.OrderNotes:created']),
        ))
        db.send_create_signal('home', ['OrderNotes'])
        
        # Adding model 'DesignOrder'
        db.create_table('home_designorder', (
            ('id', orm['home.DesignOrder:id']),
            ('client_account', orm['home.DesignOrder:client_account']),
            ('project_name', orm['home.DesignOrder:project_name']),
            ('description', orm['home.DesignOrder:description']),
            ('status', orm['home.DesignOrder:status']),
            ('cost', orm['home.DesignOrder:cost']),
            ('designer', orm['home.DesignOrder:designer']),
            ('color_views', orm['home.DesignOrder:color_views']),
            ('elevations', orm['home.DesignOrder:elevations']),
            ('quote_cabinet_list', orm['home.DesignOrder:quote_cabinet_list']),
            ('cabinet_manufacturer', orm['home.DesignOrder:cabinet_manufacturer']),
            ('cabinet_door_style', orm['home.DesignOrder:cabinet_door_style']),
            ('cabinet_wood', orm['home.DesignOrder:cabinet_wood']),
            ('cabinet_stain', orm['home.DesignOrder:cabinet_stain']),
            ('cabinet_finish', orm['home.DesignOrder:cabinet_finish']),
            ('cabinet_finish_options', orm['home.DesignOrder:cabinet_finish_options']),
            ('cabinetry_notes', orm['home.DesignOrder:cabinetry_notes']),
            ('include_hardware', orm['home.DesignOrder:include_hardware']),
            ('door_hardware', orm['home.DesignOrder:door_hardware']),
            ('drawer_hardware', orm['home.DesignOrder:drawer_hardware']),
            ('ceiling_height', orm['home.DesignOrder:ceiling_height']),
            ('crown_mouldings', orm['home.DesignOrder:crown_mouldings']),
            ('skirt_mouldings', orm['home.DesignOrder:skirt_mouldings']),
            ('soffits', orm['home.DesignOrder:soffits']),
            ('soffit_height', orm['home.DesignOrder:soffit_height']),
            ('soffit_width', orm['home.DesignOrder:soffit_width']),
            ('soffit_depth', orm['home.DesignOrder:soffit_depth']),
            ('stacked_staggered', orm['home.DesignOrder:stacked_staggered']),
            ('wall_cabinet_height', orm['home.DesignOrder:wall_cabinet_height']),
            ('vanity_cabinet_height', orm['home.DesignOrder:vanity_cabinet_height']),
            ('vanity_cabinet_depth', orm['home.DesignOrder:vanity_cabinet_depth']),
            ('corner_cabinet_base_bc', orm['home.DesignOrder:corner_cabinet_base_bc']),
            ('corner_cabinet_base_bc_direction', orm['home.DesignOrder:corner_cabinet_base_bc_direction']),
            ('corner_cabinet_wall_bc', orm['home.DesignOrder:corner_cabinet_wall_bc']),
            ('corner_cabinet_wall_bc_direction', orm['home.DesignOrder:corner_cabinet_wall_bc_direction']),
            ('island_peninsula_option', orm['home.DesignOrder:island_peninsula_option']),
            ('countertop_option', orm['home.DesignOrder:countertop_option']),
            ('backsplash', orm['home.DesignOrder:backsplash']),
            ('toekick', orm['home.DesignOrder:toekick']),
            ('lazy_susan', orm['home.DesignOrder:lazy_susan']),
            ('slide_out_trays', orm['home.DesignOrder:slide_out_trays']),
            ('waste_bin', orm['home.DesignOrder:waste_bin']),
            ('wine_rack', orm['home.DesignOrder:wine_rack']),
            ('plate_rack', orm['home.DesignOrder:plate_rack']),
            ('appliance_garage', orm['home.DesignOrder:appliance_garage']),
            ('corbels_brackets', orm['home.DesignOrder:corbels_brackets']),
            ('valance', orm['home.DesignOrder:valance']),
            ('legs_feet', orm['home.DesignOrder:legs_feet']),
            ('glass_doors', orm['home.DesignOrder:glass_doors']),
            ('range_hood', orm['home.DesignOrder:range_hood']),
            ('posts', orm['home.DesignOrder:posts']),
            ('miscellaneous_notes', orm['home.DesignOrder:miscellaneous_notes']),
            ('client_diagram', orm['home.DesignOrder:client_diagram']),
            ('client_diagram_source', orm['home.DesignOrder:client_diagram_source']),
            ('client_diagram_notes', orm['home.DesignOrder:client_diagram_notes']),
            ('designer_package', orm['home.DesignOrder:designer_package']),
            ('designer_package_notes', orm['home.DesignOrder:designer_package_notes']),
            ('client_review_rating', orm['home.DesignOrder:client_review_rating']),
            ('client_review_notes', orm['home.DesignOrder:client_review_notes']),
            ('client_notes', orm['home.DesignOrder:client_notes']),
            ('designer_notes', orm['home.DesignOrder:designer_notes']),
            ('created', orm['home.DesignOrder:created']),
            ('modified', orm['home.DesignOrder:modified']),
            ('modified_by', orm['home.DesignOrder:modified_by']),
            ('visited_status', orm['home.DesignOrder:visited_status']),
            ('valid_status', orm['home.DesignOrder:valid_status']),
            ('desired', orm['home.DesignOrder:desired']),
            ('submitted', orm['home.DesignOrder:submitted']),
            ('assigned', orm['home.DesignOrder:assigned']),
            ('projected', orm['home.DesignOrder:projected']),
            ('completed', orm['home.DesignOrder:completed']),
            ('closed', orm['home.DesignOrder:closed']),
            ('tracking_notes', orm['home.DesignOrder:tracking_notes']),
        ))
        db.send_create_signal('home', ['DesignOrder'])
        
        # Adding model 'Transaction'
        db.create_table('home_transaction', (
            ('id', orm['home.Transaction:id']),
            ('trace_id', orm['home.Transaction:trace_id']),
            ('account', orm['home.Transaction:account']),
            ('debit_or_credit', orm['home.Transaction:debit_or_credit']),
            ('trans_type', orm['home.Transaction:trans_type']),
            ('amount', orm['home.Transaction:amount']),
            ('description', orm['home.Transaction:description']),
            ('timestamp', orm['home.Transaction:timestamp']),
        ))
        db.send_create_signal('home', ['Transaction'])
        
        # Adding model 'OrderAttachment'
        db.create_table('home_orderattachment', (
            ('id', orm['home.OrderAttachment:id']),
            ('document_id', orm['home.OrderAttachment:document_id']),
            ('document', orm['home.OrderAttachment:document']),
            ('order', orm['home.OrderAttachment:order']),
            ('source', orm['home.OrderAttachment:source']),
            ('doctype', orm['home.OrderAttachment:doctype']),
            ('method', orm['home.OrderAttachment:method']),
            ('user', orm['home.OrderAttachment:user']),
            ('org', orm['home.OrderAttachment:org']),
            ('timestamp', orm['home.OrderAttachment:timestamp']),
        ))
        db.send_create_signal('home', ['OrderAttachment'])
        
        # Adding model 'Organization'
        db.create_table('home_organization', (
            ('id', orm['home.Organization:id']),
            ('status', orm['home.Organization:status']),
            ('company_name', orm['home.Organization:company_name']),
            ('company_address_1', orm['home.Organization:company_address_1']),
            ('company_address_2', orm['home.Organization:company_address_2']),
            ('company_city', orm['home.Organization:company_city']),
            ('company_state', orm['home.Organization:company_state']),
            ('company_zip4', orm['home.Organization:company_zip4']),
            ('company_phone', orm['home.Organization:company_phone']),
            ('company_fax', orm['home.Organization:company_fax']),
            ('company_email', orm['home.Organization:company_email']),
        ))
        db.send_create_signal('home', ['Organization'])
        
        # Adding model 'OrderAppliance'
        db.create_table('home_orderappliance', (
            ('id', orm['home.OrderAppliance:id']),
            ('order', orm['home.OrderAppliance:order']),
            ('appliance_type', orm['home.OrderAppliance:appliance_type']),
            ('description', orm['home.OrderAppliance:description']),
            ('height', orm['home.OrderAppliance:height']),
            ('width', orm['home.OrderAppliance:width']),
            ('depth', orm['home.OrderAppliance:depth']),
            ('options', orm['home.OrderAppliance:options']),
        ))
        db.send_create_signal('home', ['OrderAppliance'])
        
        # Adding model 'DealerOrganization'
        db.create_table('home_dealerorganization', (
            ('organization_ptr', orm['home.DealerOrganization:organization_ptr']),
            ('default_measure_units', orm['home.DealerOrganization:default_measure_units']),
            ('credit_balance', orm['home.DealerOrganization:credit_balance']),
        ))
        db.send_create_signal('home', ['DealerOrganization'])
        
        # Adding model 'UserProfile'
        db.create_table('home_userprofile', (
            ('id', orm['home.UserProfile:id']),
            ('user', orm['home.UserProfile:user']),
            ('account', orm['home.UserProfile:account']),
            ('usertype', orm['home.UserProfile:usertype']),
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
        'home.dealerorganization': {
            'credit_balance': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            'default_measure_units': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'organization_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['home.Organization']", 'unique': 'True', 'primary_key': 'True'})
        },
        'home.designorder': {
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
            'client_account': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'created_orders'", 'to': "orm['home.Organization']"}),
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
        'home.orderappliance': {
            'appliance_type': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'depth': ('django.db.models.fields.IntegerField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'height': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'options': ('django.db.models.fields.CharField', [], {'max_length': '240', 'blank': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['home.DesignOrder']"}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        },
        'home.orderattachment': {
            'doctype': ('django.db.models.fields.SmallIntegerField', [], {}),
            'document': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'document_id': ('django.db.models.fields.CharField', [], {'max_length': '24', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.SmallIntegerField', [], {}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['home.DesignOrder']", 'null': 'True', 'blank': 'True'}),
            'org': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['home.Organization']", 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.SmallIntegerField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        'home.ordernotes': {
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['home.DesignOrder']"}),
            'sequence': ('django.db.models.fields.IntegerField', [], {})
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
        'home.transaction': {
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['home.DealerOrganization']"}),
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'debit_or_credit': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'trace_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'trans_type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'home.userprofile': {
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['home.Organization']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'usertype': ('django.db.models.fields.CharField', [], {'default': "'dealer'", 'max_length': '10'})
        }
    }
    
    complete_apps = ['home']
