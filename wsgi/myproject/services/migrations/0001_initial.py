# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name=b'Category name')),
                ('description', models.CharField(max_length=30, verbose_name=b'Category description')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name=b'Item name')),
                ('text', models.TextField(max_length=1000, verbose_name=b'Item Description')),
                ('image', models.FileField(upload_to=b'documents/%Y/%m/%d')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'Created date', null=True)),
                ('last_updated', models.DateTimeField(verbose_name=b'Last Updated Date', null=True, editable=False, blank=True)),
                ('active', models.BooleanField(default=True, verbose_name=b'Is this item available/active?')),
                ('category', models.ForeignKey(verbose_name=b'Category', to='services.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('city', models.CharField(max_length=200, verbose_name=b'City')),
                ('long_position', models.DecimalField(max_digits=8, decimal_places=3)),
                ('lat_position', models.DecimalField(max_digits=8, decimal_places=3)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='location',
            field=models.ForeignKey(verbose_name=b'Location', to='services.Location'),
        ),
    ]
