from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

# Create your models here.
class Item(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, verbose_name="Item name")
    text = models.TextField(max_length=1000, verbose_name="Item Description")
    image = models.FileField(upload_to='documents/%Y/%m/%d')
    created = models.DateTimeField(verbose_name="Created date", null=True, blank=True, auto_now_add=True)
    last_updated = models.DateTimeField(editable=False, verbose_name="Last Updated Date", null=True, blank=True)
    active = models.BooleanField(verbose_name="Is this item available/active?", default=True)
    category = models.ForeignKey('Category', verbose_name="Category")
    location = models.ForeignKey('Location', verbose_name="Location")

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return self.name

@receiver(pre_save, sender=Item)
def update_edit_date(sender, instance, *args, **kwargs):
    instance.last_updated = timezone.now()

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, verbose_name="Category name")
    description = models.CharField(max_length=30, verbose_name="Category description")

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return self.name

class Location(models.Model):
    id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=200, verbose_name="City")
    long_position   = models.DecimalField (max_digits=8, decimal_places=3)
    lat_position   = models.DecimalField (max_digits=8, decimal_places=3)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return self.city
