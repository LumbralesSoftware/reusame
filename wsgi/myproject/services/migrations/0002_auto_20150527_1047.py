# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='city',
        ),
        migrations.AddField(
            model_name='location',
            name='location',
            field=models.CharField(default=b'London', max_length=200, verbose_name=b'Location (Post Code/Street, City, Country)'),
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(max_length=300, verbose_name=b'Category description'),
        ),
    ]
