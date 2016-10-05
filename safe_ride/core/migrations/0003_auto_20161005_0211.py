# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20161002_2322'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteuser',
            name='first_name',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='siteuser',
            name='last_name',
            field=models.TextField(null=True, blank=True),
        ),
    ]
