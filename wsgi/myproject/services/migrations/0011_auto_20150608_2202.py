# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0010_auto_20150603_1145'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='text',
            new_name='description',
        ),
    ]
