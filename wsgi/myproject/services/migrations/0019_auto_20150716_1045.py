# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('services', '0018_auto_20150716_1024'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRating',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('punctuation', models.DecimalField(max_digits=4, decimal_places=1, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)])),
                ('voted_user', models.ForeignKey(related_name='voted_user', verbose_name=b'User voted', to=settings.AUTH_USER_MODEL)),
                ('voting_user', models.ForeignKey(related_name='voting_user', verbose_name=b'User voting', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='userratings',
            name='voted_user',
        ),
        migrations.RemoveField(
            model_name='userratings',
            name='voting_user',
        ),
        migrations.DeleteModel(
            name='UserRatings',
        ),
    ]
