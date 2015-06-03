# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0008_item_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(unique=True, max_length=200, verbose_name=b'Category name'),
        ),
        migrations.AlterField(
            model_name='location',
            name='location',
            field=models.CharField(default=b'London', max_length=200, verbose_name=b'Location/Address (Post Code/Street, City, Country)'),
        ),
    ]
