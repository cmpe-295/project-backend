# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_client_activation_link_offset'),
        ('ride', '0004_auto_20161018_0045'),
    ]

    operations = [
        migrations.CreateModel(
            name='DriverLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('timestamp', models.DateTimeField()),
                ('latest', models.BooleanField(default=False)),
                ('driver', models.ForeignKey(related_name='location', to='core.Driver')),
            ],
        ),
    ]
