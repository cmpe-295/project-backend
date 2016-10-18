from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response

from .models import Ride, DriverLocation


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


@api_view(['POST'])
@authentication_classes((CsrfExemptSessionAuthentication, BasicAuthentication, TokenAuthentication))
def request_ride(request):
    client = request.user.client
    ride = Ride(
        client=client,
        active=True,
        deleted=False,
        pickup_latitude=request.data.get("pickup_latitude"),
        pickup_longitude=request.data.get("pickup_longitude"),
        drop_latitude=request.data.get("drop_latitude"),
        drop_longitude=request.data.get("drop_longitude"),
        request_received_at=timezone.now(),
    )
    ride.save()
    # calculate the route/eta
    eta = 1
    return Response({
        "success": True,
        "eta": eta
    }, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@authentication_classes((CsrfExemptSessionAuthentication, BasicAuthentication, TokenAuthentication))
def cancel_ride(request):
    try:
        client = request.user.client
        ride = client.rides.filter(active=True, deleted=False)
        ride = ride[0]
        ride.deleted = True
        ride.active = False
        ride.save()
        return Response({
            "success": True,
            "message": "Ride request cancelled"
        }, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response({
            "error": True,
            "message": "Incorrect token or ride cancelled"
        })
    except IndexError:
        return Response({
            "error": True,
            "message": "Ride does not exist!"
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@authentication_classes((CsrfExemptSessionAuthentication, TokenAuthentication))
def update_driver_location(request):
    driver = request.user.driver
    locations = driver.location.filter(latest=True)
    for old_location in locations:
        old_location.latest = False
        old_location.save()

    location = DriverLocation(
        driver=driver,
        latitude=request.data.get("latitude"),
        longitude=request.data.get("longitude"),
        timestamp=timezone.now(),
        latest=True
    )
    location.save()
    return Response({
        "success": True
    }, status=status.HTTP_201_CREATED)
