# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_driver_push_notification_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='push_notification_token',
            field=models.TextField(null=True, blank=True),
        ),
    ]
