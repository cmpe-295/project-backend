from django.db import models

# Create your models here.
from core.models import Client, Driver


class Ride(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    drop_latitude = models.FloatField()
    drop_longitude = models.FloatField()
    client = models.ForeignKey(Client, related_name='rides')
    request_received_at = models.DateTimeField(null=True, blank=True)
    request_processed_at = models.DateTimeField(null=True, blank=True)
    initial_eta = models.FloatField()
    pickup_at = models.DateTimeField(null=True, blank=True)
    drop_at = models.DateTimeField(null=True, blank=True)
    serviced_by = models.ForeignKey(Driver, related_name='rides')

    def __unicode__(self):
        return "%s - %s" % (self.client, self.created_on)
