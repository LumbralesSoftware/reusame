from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from .utils import get_coords

# Create your models here.
class Item(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, verbose_name="Item name")
    text = models.TextField(max_length=1000, verbose_name="Item Description")
    image = models.FileField(upload_to='items/%Y/%m/%d')
    created = models.DateTimeField(verbose_name="Created date", null=True, blank=True, auto_now_add=True)
    last_updated = models.DateTimeField(editable=False, verbose_name="Last Updated Date", null=True, blank=True)
    active = models.BooleanField(verbose_name="Is this item available/active?", default=True)
    category = models.ForeignKey('Category', verbose_name="Category")
    location = models.ForeignKey('Location', verbose_name="Location")
    owner = models.ForeignKey(User, verbose_name='Owner')

    def requestedBy(self, user, body):
        headers = {'Reply-To': user.email}
        email = EmailMessage(
            user.first_name + ' wants ' + self.name,
            'User ' + user.first_name + ' is interested in your item ' + self.name + '. His message: ' + body,
            to=['javilumbrales@gmail.com'],
            headers=headers
        )
        email.content_subtype = "html"
        email.send()
        return True
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
    description = models.TextField(max_length=300, verbose_name="Category description")

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return self.name

class Location(models.Model):
    id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=200, verbose_name="Location/Address (Post Code/Street, City, Country)", default='London')
    long_position = models.DecimalField (max_digits=16, decimal_places=8, blank=True)
    lat_position = models.DecimalField (max_digits=16, decimal_places=8, blank=True)

    def save(self, **kwargs):
        #if self.id == None and self.coordinates == None:
        if not self.long_position or not self.lat_position:
            self.lat_position, self.long_position = get_coords(self.location)
        super(Location, self).save()

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return self.location
