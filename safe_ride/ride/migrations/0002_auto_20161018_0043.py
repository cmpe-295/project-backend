# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ride', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='serviced_by',
            field=models.ForeignKey(related_name='rides', blank=True, to='core.Driver', null=True),
        ),
    ]
