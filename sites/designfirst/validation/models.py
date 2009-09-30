from django.db import models
from django.utils.translation import ugettext as _

# Create your models here.

class Manufacturer(models.Model):
    name = models.CharField(_("Manufacturer Name"), primary_key=True, max_length=30)
    small_logo = models.ImageField(_("Small Logo"), upload_to='data/logos', blank=True)
    large_logo = models.ImageField(_("Logo"), upload_to='data/logos', blank=True, null=True)
    
    def __unicode__(self):
        return self.name
    
    def json_dict(self):
        return {
            'name': self.name,
            'small_logo': self.small_logo and self.small_logo.url or None,
        }
    
class ProductLine(models.Model):
    name = models.CharField(_("Product Line"), primary_key=True, max_length=30)
    manufacturer = models.ForeignKey(Manufacturer)
    
    def __unicode__(self):
        return '%s - %s' % (self.manufacturer, self.name)

class DoorStyle(models.Model):
    name = models.CharField(_("Door Style"), primary_key=True, max_length=30)
    manufacturer = models.ForeignKey(Manufacturer, blank=True, null=True)
    product_line = models.ForeignKey(ProductLine, blank=True, null=True)
    thumbnail = models.ImageField(_("Small Image"), upload_to='data/doors', blank=True, null=True)
    image = models.ImageField(_("Large Image"), upload_to='data/doors', blank=True, null=True)
    
    def __unicode__(self):
        return self.name

class WoodOption(models.Model):
    name = models.CharField(_("Wood"), primary_key=True, max_length=30)
    manufacturer = models.ForeignKey(Manufacturer, blank=True, null=True)
    product_line = models.ForeignKey(ProductLine, blank=True, null=True)
    image = models.ImageField(_("Sample"), upload_to='data/woods', blank=True, null=True)
    
    def __unicode__(self):
        return self.name

class FinishOption(models.Model):
    name = models.CharField(_("Finish Option"), primary_key=True, max_length=30)
    manufacturer = models.ForeignKey(Manufacturer, blank=True, null=True)
    product_line = models.ForeignKey(ProductLine, blank=True, null=True)
    image = models.ImageField(_("Sample"), upload_to='data/finishes', blank=True, null=True)
    
    def __unicode__(self):
        return self.name

class GeneralOption(models.Model):
    """
    Manufacturer (or product line) specific option.
    
    
    """
    name = models.CharField(_("Finish Option"), primary_key=True, max_length=30)
    type = models.CharField(_("Option Type"), max_length=10)
    description = models.TextField(_("Description"), max_length=30)
    manufacturer = models.ForeignKey(Manufacturer, blank=True, null=True)
    product_line = models.ForeignKey(ProductLine, blank=True, null=True)
    image = models.ImageField(_("Sample"), upload_to='data/options', null=True)
    
    def __unicode__(self):
        return self.name