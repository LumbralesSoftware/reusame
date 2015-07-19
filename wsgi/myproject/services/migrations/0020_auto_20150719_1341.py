# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0019_auto_20150716_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='language',
            field=models.CharField(default=b'en', max_length=7, choices=[(b'es', b'Spanish'), (b'en', b'English')]),
        ),
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(upload_to=b'items/%Y/%m/%d', verbose_name='Image'),
        ),
    ]
