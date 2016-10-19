import json
import sys

import numpy as np
import requests
from django.conf import settings
from django.db import models

# Create your models here.
from core.models import Client, Driver

from core.serializers import ClientSerializer
from django.utils import timezone


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
    initial_eta = models.FloatField(null=True, blank=True)
    pickup_at = models.DateTimeField(null=True, blank=True)
    drop_at = models.DateTimeField(null=True, blank=True)
    serviced_by = models.ForeignKey(Driver, related_name='rides', null=True, blank=True)
    deleted = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s - %s" % (self.client, self.created_on)


class DriverLocation(models.Model):
    driver = models.ForeignKey(Driver, related_name="location")
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField()
    latest = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s %s" % (self.driver, self.timestamp.strftime("%H:%M:%S"))


def dijkstra(matrix, m=None, n=None):
    m = n = len(matrix)
    k = 0
    cost = [[0 for x in range(m)] for x in range(1)]
    offsets = [k]
    elepos = 0
    for j in range(m):
        cost[0][j] = matrix[k][j]
    mini = 999
    for x in range(m - 1):
        mini = 999
        for j in range(m):
            if cost[0][j] <= mini and j not in offsets:
                mini = cost[0][j]
                elepos = j
        offsets.append(elepos)
        for j in range(m):
            if cost[0][j] > cost[0][elepos] + matrix[elepos][j]:
                cost[0][j] = cost[0][elepos] + matrix[elepos][j]
    return offsets, cost[0]


def calculate_route(client_id=None):
    mapquest_url = "http://www.mapquestapi.com/directions/v2/routematrix?key=%s" % settings.MAPQUEST_KEY
    request_body = {
        "options": {
            "allToAll": True
        }
    }
    locations = []
    current_driver_location = DriverLocation.objects.filter(latest=True).order_by("-timestamp")
    current_driver_location = current_driver_location[0]
    locations.append({
        "latLng": {
            "lat": current_driver_location.latitude,
            "lng": current_driver_location.longitude,

        },
        "user": "Driver",
        "custom_type": "start"
    })
    for location in Ride.objects.filter(active=True, deleted=False).order_by("request_received_at")[:8]:
        if location.serviced_by:
            locations.append({
                "latLng": {
                    "lat": location.drop_latitude,
                    "lng": location.drop_longitude
                },
                "user": ClientSerializer(location.client).data,
                "custom_type": "drop",
                "ride_id": location.pk
            })
        else:
            locations.append({
                "latLng": {
                    "lat": location.pickup_latitude,
                    "lng": location.pickup_longitude
                },
                "user": ClientSerializer(location.client).data,
                "custom_type": "pick",
                "ride_id": location.pk
            })
        location.request_processed_at = timezone.now()
    request_body['locations'] = locations
    if len(locations) > 0:
        response = requests.post(mapquest_url, data=json.dumps(request_body))
        if response.status_code == 200:
            time_matrix = json.loads(response.content)['time']
            path, cost_matrix = dijkstra(time_matrix)
            eta = 0
            path_in_co_ordinates = [{
                "latLng": locations[0]['latLng'],
                "user": "driver",
                "eta": eta
            }]
            for index in range(1, len(path)):
                eta += cost_matrix[index]
                path_in_co_ordinates.append({
                    "latLng": locations[path[index]]['latLng'],
                    "user": locations[path[index]]['user'],
                    "type": locations[path[index]]['custom_type'],
                    "eta": eta,
                    "ride_id": locations[path[index]]['ride_id']
                })
            if client_id:
                eta_for_client = 0
                for i in range(1, len(path_in_co_ordinates)):
                    if path_in_co_ordinates[i]["user"]["id"] == client_id:
                        eta_for_client = path_in_co_ordinates[i]["eta"]
                return path_in_co_ordinates, eta_for_client
            return path_in_co_ordinates
        else:
            print "error"
    else:
        return None
