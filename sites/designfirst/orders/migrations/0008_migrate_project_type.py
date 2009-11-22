
from south.db import db
from django.db import models
from designfirst.orders.models import *

class Migration:
    
    def forwards(self, orm):
        for order in orm.WorkingOrder.objects.all():
            try:
                order.project_type = order.type
            except ValueError:
                order.project_type = '*' # 'other' value..
            order.save()
    
    
    def backwards(self, orm):
        for order in orm.WorkingOrder.objects.all():
            try:
                order.type = order.project_type
            except ValueError:
                order.type = '*' # 'other' value..
            order.save()
    
    
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
        'orders.appliance': {
            'depth': ('DimensionField', ["_('')"], {'null': 'True', 'blank': 'True'}),
            'height': ('DimensionField', ["_('')"], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'options': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'appliances'", 'to': "orm['orders.WorkingOrder']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'width': ('DimensionField', ["_('')"], {'null': 'True', 'blank': 'True'})
        },
        'orders.attachment': {
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attachments'", 'to': "orm['orders.WorkingOrder']"}),
            'page_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'source': ('django.db.models.fields.CharField', [], {'default': "'F'", 'max_length': '1'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'})
        },
        'orders.attachmentpage': {
            'attachment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['orders.Attachment']"}),
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '180'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'thumb': ('django.db.models.fields.files.ImageField', [], {'max_length': '180', 'null': 'True'})
        },
        'orders.moulding': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'num': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mouldings'", 'to': "orm['orders.WorkingOrder']"}),
            'type': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'orders.workingorder': {
            'account_code': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'appliance_garage': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'base_cabinet_depth': ('DimensionField', ["_('Depth')"], {'null': 'True', 'blank': 'True'}),
            'base_cabinet_height': ('DimensionField', ["_('Vanity Cabinet Height')"], {'null': 'True', 'blank': 'True'}),
            'brackets': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'cabinet_material': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'client_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'color_views': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'corbels': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'degree90_corner_base': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'degree90_corner_base_shelv': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'degree90_corner_wall': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'desired': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'diagonal_corner_base': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'diagonal_corner_base_shelv': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'diagonal_corner_wall': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'diagonal_corner_wall_shelv': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'dimension_style': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'door_handle_model': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'door_handle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'door_style': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'drawer_front_style': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'drawer_handle_model': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'drawer_handle_type': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'elevations': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'finish_color': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'finish_options': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'finish_type': ('django.db.models.fields.CharField', [], {'default': "'S'", 'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'glass_doors': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'has_soffits': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legs_feet': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'manufacturer': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'plate_rack': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'posts': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'product_line': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'project_name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'project_type': ('django.db.models.fields.CharField', [], {'default': "'K'", 'max_length': '1'}),
            'quoted_cabinet_list': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'range_hood': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'rush': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'slide_out_trays': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'soffit_depth': ('DimensionField', ["_('Depth')"], {'null': 'True', 'blank': 'True'}),
            'soffit_height': ('DimensionField', ["_('Height')"], {'null': 'True', 'blank': 'True'}),
            'soffit_width': ('DimensionField', ["_('Width')"], {'null': 'True', 'blank': 'True'}),
            'standard_sizes': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'status': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'submitted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'tracking_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'K'", 'max_length': '1'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'valance': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'vanity_cabinet_depth': ('DimensionField', ["_('Depth')"], {'null': 'True', 'blank': 'True'}),
            'vanity_cabinet_height': ('DimensionField', ["_('Vanity Cabinet Height')"], {'null': 'True', 'blank': 'True'}),
            'wall_cabinet_depth': ('DimensionField', ["_('Wall Cabinet Height')"], {'null': 'True', 'blank': 'True'}),
            'wall_cabinet_height': ('DimensionField', ["_('Wall Cabinet Height')"], {'null': 'True', 'blank': 'True'}),
            'waste_bin': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'wine_rack': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'})
        }
    }
    
    complete_apps = ['orders']
