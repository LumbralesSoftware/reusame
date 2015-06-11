# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('services', '0013_item_expires_on'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRatings',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('punctuation', models.DecimalField(max_digits=4, decimal_places=1)),
                ('voted_user', models.ForeignKey(related_name='voted_user', verbose_name=b'User voted', to=settings.AUTH_USER_MODEL)),
                ('voting_user', models.ForeignKey(related_name='voting_user', verbose_name=b'User voting', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
