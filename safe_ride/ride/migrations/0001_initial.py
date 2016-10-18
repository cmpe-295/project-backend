# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_client_activation_link_offset'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False)),
                ('pickup_latitude', models.FloatField()),
                ('pickup_longitude', models.FloatField()),
                ('drop_latitude', models.FloatField()),
                ('drop_longitude', models.FloatField()),
                ('request_received_at', models.DateTimeField(null=True, blank=True)),
                ('request_processed_at', models.DateTimeField(null=True, blank=True)),
                ('initial_eta', models.FloatField()),
                ('pickup_at', models.DateTimeField(null=True, blank=True)),
                ('drop_at', models.DateTimeField(null=True, blank=True)),
                ('client', models.ForeignKey(related_name='rides', to='core.Client')),
                ('serviced_by', models.ForeignKey(related_name='rides', to='core.Driver')),
            ],
        ),
    ]
