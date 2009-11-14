"""
A flexible generic data model for cabinet industry.

   * provide for easy data entry from manufacturers catalogs   * present information in a way that minimizes erroneous selections
      * enumerate types of options for a particular artifact
      * enumerate all options of a particular type
      * show valid options based on context of current selections
   * validate selections
      * rules for 
      * constraints
   * model relationships?
Data Example
      * the kingston door comes in maple, cherry and lyptus
         * the cherry stain are chocolate, espresso and coffee
         * the maple stains are coffe, taupe and olive
         * the lyptus stains are all of the above
         * also support paint options of red white or blue
         * stained doors support glazes of X Y and Z
         * special   finishoptions include speckling, distressing and dodging    





"""
import os.path
import re
from django.db import models
from django.utils.translation import ugettext as _

# Create your models here.

def catalog_location(obj, file_name):
    root = "catalog"
    catalog = getattr(obj, 'catalog', None)
    if not catalog: catalog = obj     
    path = os.path.join('catalog', catalog.manufacturer, catalog.product_line, obj.__class__.__name__.lower(), obj.name, file_name)
        
    return path 
    

class CatalogManager(models.Manager):
    def add_product(self, product):
        pass

    def search(self, **kwargs):
        return None #TODO
    
        
class Catalog(models.Model):
    manufacturer = models.CharField(_("Manufacturer"), max_length=30)
    product_line = models.CharField(_("Product Line"), max_length=30)
    version = models.CharField(_("Issue"), max_length=10, default='00001')
    image = models.ImageField(_("Logo"), upload_to=catalog_location, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
    objects = CatalogManager()
    
    class Meta:
        unique_together = ('manufacturer', 'product_line', 'version')
        
    def __unicode__(self):
        return "%s by %s (%s)" % (self.product_line, self.manufacturer, self.version)    

    def file_path(self):
        return re.sub('[^\w\s-]', '', self.__unicode__()).strip().lower()
    
    
class Type(models.Model):
    """
    A type identifier - e.g. 'Door' or 'Stain'
    """
    catalog = models.ForeignKey(Catalog)
    name    = models.CharField(_("Attribute Type"), max_length=30)
    description = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('name', 'catalog')
        abstract = True

    def __unicode__(self):
        return self.name



class ItemType(Type):
    pass

class AttributeType(Type):
    pass
            
class Item(models.Model):
    catalog = models.ForeignKey(Catalog, editable=False)
    type = models.ForeignKey(ItemType)
    name = models.CharField(_("Name"), max_length=30)
    image = models.ImageField(_("Image"), upload_to=catalog_location, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ('name', 'type', 'catalog')
    
    def __unicode__(self):
        return self.name
    
class Attribute(models.Model):
    catalog = models.ForeignKey(Catalog, editable=False)
    type = models.ForeignKey(AttributeType) 
    name = models.CharField(_("Name"), max_length=30)
    image = models.ImageField(_("Sample"), upload_to=catalog_location, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ('name', 'type', 'catalog')
    
    def __unicode__(self):
        return self.name

class Entry(models.Model):
    catalog = models.ForeignKey(Catalog, editable=False)
    item = models.ForeignKey(Item)
   
class EntryAttributes(models.Model):
    catalog = models.ForeignKey(Catalog, editable=False)
    attribute = models.ForeignKey(Attribute)
 
     
##
## 
# 
class RelationshipType(Type):
    pass

class Relationship(models.Model):
    catalog = models.ForeignKey(Catalog)
    type = models.ForeignKey(RelationshipType) 
    item = models.ForeignKey(Item)
    attribute = models.ForeignKey(ItemType)
    description = models.TextField(blank=True, null=True)

