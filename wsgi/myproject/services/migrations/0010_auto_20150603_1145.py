# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0009_auto_20150603_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='active',
            field=models.BooleanField(default=False, verbose_name=b'Is this item available/active?'),
        ),
    ]
