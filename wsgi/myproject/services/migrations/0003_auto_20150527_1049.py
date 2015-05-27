# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_auto_20150527_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.FileField(upload_to=b'items/%Y/%m/%d'),
        ),
    ]
