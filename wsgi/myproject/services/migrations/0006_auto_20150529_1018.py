# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0005_auto_20150527_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='lat_position',
            field=models.DecimalField(max_digits=8, decimal_places=8, blank=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='long_position',
            field=models.DecimalField(max_digits=8, decimal_places=8, blank=True),
        ),
    ]
