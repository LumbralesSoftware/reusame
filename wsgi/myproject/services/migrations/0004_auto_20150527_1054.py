# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_auto_20150527_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='lat_position',
            field=models.DecimalField(null=True, max_digits=8, decimal_places=3),
        ),
        migrations.AlterField(
            model_name='location',
            name='long_position',
            field=models.DecimalField(null=True, max_digits=8, decimal_places=3),
        ),
    ]
