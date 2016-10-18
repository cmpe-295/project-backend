# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ride', '0002_auto_20161018_0043'),
    ]

    operations = [
        migrations.AddField(
            model_name='ride',
            name='deleted',
            field=models.BooleanField(default=True),
        ),
    ]
