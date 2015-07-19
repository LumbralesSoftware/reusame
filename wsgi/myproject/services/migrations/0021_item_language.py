# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0020_auto_20150719_1341'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='language',
            field=models.CharField(default=b'en', max_length=7, choices=[(b'es', b'Spanish'), (b'en', b'English')]),
        ),
    ]
