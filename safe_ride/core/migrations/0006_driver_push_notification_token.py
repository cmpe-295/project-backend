# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20161018_1843'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='push_notification_token',
            field=models.TextField(null=True, blank=True),
        ),
    ]
