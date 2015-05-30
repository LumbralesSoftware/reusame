# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0006_auto_20150529_1018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='lat_position',
            field=models.DecimalField(max_digits=16, decimal_places=8, blank=True),
        ),
        migrations.AlterField(
            model_name='location',
            name='long_position',
            field=models.DecimalField(max_digits=16, decimal_places=8, blank=True),
        ),
    ]
