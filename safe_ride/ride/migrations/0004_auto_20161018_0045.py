# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ride', '0003_ride_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='initial_eta',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
