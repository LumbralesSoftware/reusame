# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_auto_20150527_1054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='lat_position',
            field=models.DecimalField(default=1, max_digits=8, decimal_places=3, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='location',
            name='long_position',
            field=models.DecimalField(default=1.0, max_digits=8, decimal_places=3, blank=True),
            preserve_default=False,
        ),
    ]
