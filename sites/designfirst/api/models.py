import logging
import re
from datetime import datetime

from django.core import serializers  
from django.core.serializers import xml_serializer 
from django.db import models
from django.utils.translation import ugettext_lazy as _


logger = logging.getLogger('api.models')

# Create your models here.
class Const(object):
    NEW_INBOUND, MANUAL_REPOST = ('New Inbound', 'Manual Repost')
    REQUEST_TYPE_CHOICES = [(a, a) for a in [NEW_INBOUND, MANUAL_REPOST]]
    
    PDF, TIF = ('pdf', 'tif')
    FILE_TYPE_CHOICES = [(a, a) for a in [NEW_INBOUND, MANUAL_REPOST]]
    
    TWO_DIMENSIONAL, LEFT_TO_RIGHT, TOP_TO_BOTTOM, RIGHT_TO_LEFT, BOTTOM_TO_TOP = (
        '2-Dimensional', 'Left/Right', 'Top/Bottom', 'Right/Left', 'Bottom/Top'
    )
    READ_DIRECTION_CHOICES = [(a, a) for a in [TWO_DIMENSIONAL, LEFT_TO_RIGHT, TOP_TO_BOTTOM, RIGHT_TO_LEFT, BOTTOM_TO_TOP]]
    
class FaxDateTimeField(models.DateTimeField):
    def to_python(self, value):
        month, day, year, hour, minute, seconds = [int(a) for a in re.split('/| |:', value)]      
        return super(FaxDateTimeField, self).to_python(
                        datetime(year,month,day,hour,minute,seconds))
                                                  
class Fax(models.Model):
    username = models.CharField(max_length=20,blank=True,null=True)
    password = models.CharField(max_length=20,blank=True,null=True)
    request_date = FaxDateTimeField()
    request_type = models.CharField(max_length=15, choices=Const.REQUEST_TYPE_CHOICES)
    account_id = models.CharField(max_length=10, help_text=_('eFax DeveloperTM account identifier.'))
    number_dialed = models.CharField(max_length=10, help_text=_('The fax number that was dialed.'))
    date_received = FaxDateTimeField()
    fax_name = models.CharField(_('The actual fax name given to this fax by eFax DeveloperTM as changed by the client.'), max_length=50)
    file_type = models.CharField(max_length=3, choices=Const.FILE_TYPE_CHOICES, help_text=_('The document type as stored based on the "Inbound File Format" setting.'))
    page_count = models.PositiveSmallIntegerField()
    split_pages = models.BooleanField()
    cs_id = models.CharField(_('station identifier'), max_length=50, 
                             help_text=_('The station identifier, when supplied by the receiving fax machine upon successful transmission.'))
    ani = models.CharField(max_length=25, help_text=_('The automatic number identification (caller id) contains the calling partys fax number.'))
    status = models.PositiveSmallIntegerField(help_text=_('Numeric field indicating the fax status. "0" indicates a successful transmission while all other values indicate an error code which can be cross- referenced with am eFax DeveloperTM supplied table.'))
    mcf_id = models.IntegerField(help_text=_('eFax DeveloperTM fax ID.'))
    file_contents = models.TextField(null=True, blank=True, help_text=_('Base64 encoded file contents.'))
    
    user_fields_read = models.PositiveSmallIntegerField(help_text=_('Count of associated user-defined fields for this document.'))
    barcodes_read = models.PositiveSmallIntegerField(help_text=_('Count of associated barcodes for this document.'))
    
    class XmlMapping:
        root = 'InboundPostRequest'
        fields = [
            ('AccessControl/UserName', 'username'),
            ('AccessControl/Password', 'password'),
            ('RequestControl/RequestDate', 'request_date'),
            ('RequestControl/RequestType', 'request_type'),
            ('FaxControl/AccountID', 'account_id'),
            ('FaxControl/NumberDialed', 'number_dialed'),
            ('FaxControl/DateReceived', 'date_received'),
            ('FaxControl/FaxName', 'fax_name'),
            ('FaxControl/FileType', 'file_type'),
            ('FaxControl/PageCount', 'page_count'),
            ('FaxControl/CSID', 'cs_id'),
            ('FaxControl/ANI', 'ani'),
            ('FaxControl/Status', 'status'),
            ('FaxControl/MCFID', 'mcf_id'),
            ('FaxControl/FileContents', 'file_contents'),
            
            ('FaxControl/UserFieldControl/UserFieldsRead', 'user_fields_read'),
            ('FaxControl/BarcodeControl/BarcodesRead', 'barcodes_read'),
        ]
        
        
class FaxProperty(models.Model):    
    fax = models.ForeignKey(Fax)
    field_name = models.CharField(max_length=100, help_text=_('Client defined field name'))
    field_value = models.CharField(max_length=100, help_text=_('Client defined field value'))
    
    class XmlMapping:
        root = 'FaxControl/UserFieldControl/UserFields/UserField'
        fields = [
            ('FieldName', 'field_name'),
            ('FieldValue', 'field_value'),
        ]
    
    
class FaxBarcode(models.Model):
    fax = models.ForeignKey(Fax)
    key = models.TextField(help_text=_('The interpreted barcode value.'))
    read_sequence = models.PositiveSmallIntegerField(help_text=_('A per-page sequence number given to each barcode as it is read on a given page.'))
    read_direction = models.CharField(max_length=50, choices=Const.READ_DIRECTION_CHOICES,
                                      help_text=_('The read direction used to interpret the barcode stored within this container.'))
    symbology = models.CharField(max_length=30, help_text=_('The symbology or protocol used to generate the barcode.'))
    page_number = models.PositiveSmallIntegerField(help_text=_('The physical page number this barcode is found on within the fax document.'))
    x_start_point_a = models.FloatField(help_text=_('Coordinate grid x-axis for ending edge point A.')) 
    y_start_point_a = models.FloatField(help_text=_('Coordinate grid y-axis for ending edge point A.')) 
    x_start_point_b = models.FloatField(help_text=_('Coordinate grid x-axis for ending edge point B.')) 
    y_start_point_b = models.FloatField(help_text=_('Coordinate grid y-axis for ending edge point B.')) 
    x_end_point_a = models.FloatField(help_text=_('Coordinate grid x-axis for ending edge point A.')) 
    y_end_point_a = models.FloatField(help_text=_('Coordinate grid y-axis for ending edge point A.')) 
    x_end_point_b = models.FloatField(help_text=_('Coordinate grid x-axis for ending edge point B.')) 
    y_end_point_b = models.FloatField(help_text=_('Coordinate grid y-axis for ending edge point B.')) 
    
    class XmlMapping:
        root = 'FaxControl/BarcodeControl/Barcodes/Barcode'
        fields = [
            ('Key', 'key'),
            ('AdditionalInfo/ReadSequence', 'read_sequence'),
            ('AdditionalInfo/ReadDirection', 'read_direction'),
            ('AdditionalInfo/Symbology', 'symbology'),
            ('AdditionalInfo/CodeLocation/PageNumber', 'page_number'),
            ('AdditionalInfo/CodeLocation/PageCoordinates/StartEdge/XStartPointA', 'x_start_point_a'),
            ('AdditionalInfo/CodeLocation/PageCoordinates/StartEdge/YStartPointA', 'y_start_point_a'),
            ('AdditionalInfo/CodeLocation/PageCoordinates/StartEdge/XStartPointB', 'x_start_point_b'),
            ('AdditionalInfo/CodeLocation/PageCoordinates/StartEdge/YStartPointB', 'y_start_point_b'),
            ('AdditionalInfo/CodeLocation/PageCoordinates/EndEdge/XEndPointA', 'x_end_point_a'),
            ('AdditionalInfo/CodeLocation/PageCoordinates/EndEdge/YEndPointA', 'y_end_point_a'),
            ('AdditionalInfo/CodeLocation/PageCoordinates/EndEdge/XEndPointB', 'x_end_point_b'),
            ('AdditionalInfo/CodeLocation/PageCoordinates/EndEdge/YEndPointB', 'y_end_point_b'),
        ]
    
    
class FaxPage(models.Model):
    fax = models.ForeignKey(Fax)
    page_number = models.PositiveSmallIntegerField(help_text=_('The physical page number within the fax document.'))
    page_contents = models.TextField(help_text=_('Base64 encoded file contents.'))
    
    class XmlMapping:
        root = 'FaxControl/PageContentControl/Pages/Page'
        fields = [
            ('PageNumber', 'page_number'),
            ('PageContents', 'page_contents'),        
        ]

        
class InboundFaxProcessor(xml_serializer.Deserializer):

    _object_mappings = {}
    
    def register_object_mapping(cls, model):
        #logger.debug('InboundFaxProcessor::register_object_mapping(<%s>)', model)
        model._root = model.XmlMapping.root.rsplit('/',1)[-1]
        model._fieldmap = dict([(name.rsplit('/',1)[-1], val) for (name, val) in model.XmlMapping.fields])        
        cls._object_mappings[model._root] = model
    register_object_mapping = classmethod(register_object_mapping)
        
    def __init__(self, stream):
        self._children = []
        return super(InboundFaxProcessor, self).__init__(stream)

    def process_message(self):
        root = None
        for event, node in self.event_stream:
            if event == "START_ELEMENT" and node.nodeName in self._object_mappings:
                root = self.process_element(node)
                break;
        if root:
            root.save()
            logger.debug('InboundFaxProcessor::process_message saved message (<%s>)', root.pk)
            for child in self._children:
                child.fax = root
                child.save()
                #logger.debug('InboundFaxProcessor::process_message saved child (<%s>, <%s>, <%s>)', root.pk, child.pk, child.__class__)
        return root
    
    def process_element(self, node, parent=None):
        #logger.debug('InboundFaxProcessor::process_element(<%s>, <%s>)', node, parent)
        model = self._object_mappings[node.nodeName]
        instance = model()
        for event, child_node in self.event_stream:
            if event == 'START_ELEMENT' and child_node.nodeName in model._fieldmap:
                self.event_stream.expandNode(child_node)
                field = instance._meta.get_field(model._fieldmap[child_node.nodeName])
                setattr(instance, field.name, xml_serializer.getInnerText(child_node))
            elif event == 'START_ELEMENT' and child_node.nodeName in self._object_mappings:
                child = self.process_element(child_node, node)
                self._children.append(child)
                #logger.debug('InboundFaxProcessor::_handle_object stashing child <%s>', child)
            elif event == 'END_ELEMENT' and child_node.nodeName == node.nodeName:
                break 
        return instance
            
            
InboundFaxProcessor.register_object_mapping(Fax)
InboundFaxProcessor.register_object_mapping(FaxProperty)
InboundFaxProcessor.register_object_mapping(FaxBarcode)
InboundFaxProcessor.register_object_mapping(FaxPage)
