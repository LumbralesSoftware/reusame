# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings
from django.utils.timezone import utc
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('services', '0007_auto_20150529_1040'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='owner',
            field=models.ForeignKey(default=1, verbose_name=b'Owner', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
