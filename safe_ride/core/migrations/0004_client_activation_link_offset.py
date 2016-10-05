# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20161005_0211'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='activation_link_offset',
            field=models.TextField(null=True, blank=True),
        ),
    ]
