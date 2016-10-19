# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_client_activation_link_offset'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='latitude',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='client',
            name='longitude',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
