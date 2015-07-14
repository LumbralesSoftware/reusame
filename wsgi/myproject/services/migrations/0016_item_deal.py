# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0015_auto_20150612_0943'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='deal',
            field=models.TextField(max_length=1000, null=True, verbose_name='Deal Conditions', blank=True),
        ),
    ]
