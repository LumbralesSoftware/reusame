# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0014_userratings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userratings',
            name='punctuation',
            field=models.DecimalField(max_digits=4, decimal_places=1, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)]),
        ),
    ]
