# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('services', '0017_userrequests'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRequest',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created date', null=True)),
                ('message', models.TextField(max_length=1000, null=True, verbose_name='message', blank=True)),
                ('item', models.ForeignKey(verbose_name=b'Item requested', to='services.Item')),
                ('requester', models.ForeignKey(verbose_name=b'User requesting', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='userrequests',
            name='item',
        ),
        migrations.RemoveField(
            model_name='userrequests',
            name='requester',
        ),
        migrations.DeleteModel(
            name='UserRequests',
        ),
    ]
