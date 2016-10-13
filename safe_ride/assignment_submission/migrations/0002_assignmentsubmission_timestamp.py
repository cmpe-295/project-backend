# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('assignment_submission', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignmentsubmission',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 13, 2, 2, 31, 835599, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
