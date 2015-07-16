# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('services', '0016_item_deal'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRequests',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created date', null=True)),
                ('message', models.TextField(max_length=1000, null=True, verbose_name='message', blank=True)),
                ('item', models.ForeignKey(verbose_name=b'Item requested', to='services.Item')),
                ('requester', models.ForeignKey(verbose_name=b'User requesting', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
