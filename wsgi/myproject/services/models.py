from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core import serializers
from django.utils.translation import ugettext_lazy as _
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

import base64
import json
from PIL import Image


from .utils import get_coords

MAX_IMG_SIZE = 1024

# Create your models here.
class Item(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, verbose_name=_("Item name"))
    description = models.TextField(max_length=1000, verbose_name=_("Item Description"))
    deal = models.TextField(max_length=1000, verbose_name=_("Deal Conditions"), blank=True, null=True)
    image = models.ImageField(upload_to='items/%Y/%m/%d', verbose_name=_("Image"))
    created = models.DateTimeField(verbose_name=_("Created date"), null=True, blank=True, auto_now_add=True)
    last_updated = models.DateTimeField(editable=False, verbose_name=_("Last Updated Date"), null=True, blank=True)
    expires_on = models.DateTimeField(verbose_name=_("When does the item expires?"), null=True, blank=True)
    active = models.BooleanField(verbose_name=_("Is this item available/active?"), default=False)
    category = models.ForeignKey('Category', verbose_name=_("Category"))
    location = models.ForeignKey('Location', verbose_name=_("Location"))
    owner = models.ForeignKey(User, verbose_name=_('Owner'))
    language = models.CharField(max_length=7, choices=settings.LANGUAGES, default="en")

    def to_json(self):
        from .serializers import ItemSerializer
        item = ItemSerializer(self)
        return base64.urlsafe_b64encode(json.dumps(item.data))

    def save(self, *args, **kwargs):

        super(Item, self).save(*args, **kwargs)

        if not self.id and not self.image:
            return

        image = Image.open(self.image)
        size = (MAX_IMG_SIZE, MAX_IMG_SIZE)
        image.thumbnail(size, Image.ANTIALIAS)
        image.save(self.image.path)


    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return self.name

@receiver(pre_save, sender=Item)
def update_edit_date(sender, instance, *args, **kwargs):
    instance.last_updated = timezone.now()

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, verbose_name=_("Category name"), unique=True)
    description = models.TextField(max_length=300, verbose_name=_("Category description"))
    language = models.CharField(max_length=7, choices=settings.LANGUAGES, default="en")

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return self.name

class Location(models.Model):
    id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=200, verbose_name=_("Location/Address (Post Code/Street, City, Country)"), default='London')
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

class UserRating(models.Model):
    id = models.AutoField(primary_key=True)
    voted_user = models.ForeignKey(User, verbose_name='User voted', related_name="voted_user")
    voting_user = models.ForeignKey(User, verbose_name='User voting', related_name="voting_user")
    punctuation = models.DecimalField(max_digits=4, decimal_places=1, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])

class UserRequest(models.Model):
    id = models.AutoField(primary_key=True)
    requester = models.ForeignKey(User, verbose_name='User requesting')
    item = models.ForeignKey(Item, verbose_name='Item requested')
    created = models.DateTimeField(verbose_name=_("Created date"), null=True, blank=True, auto_now_add=True)
    message = models.TextField(max_length=1000, verbose_name=_("message"), blank=True, null=True)

    def request(self):
        msg_html = render_to_string(
                'email/request.html',
                {
                    'item': self.item.name,
                    'location': self.item.location.location,
                    'name': self.requester.first_name,
                    'image': self.item.image.url,
                    'message': self.message,
                    'email': self.requester.email,
                    'owner': self.item.owner.first_name
                }
        )

        headers = {'Reply-To': self.requester.email}
        email = EmailMessage(
            self.requester.first_name + ' ' + _('is interested in') + ' ' + self.item.name,
            msg_html,
            from_email='REUSAME ' + '<' + self.requester.email + '>',
            to=[self.item.owner.email],
            headers=headers
        )
        email.content_subtype = "html"
        email.send()

        return True

