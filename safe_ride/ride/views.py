from core.models import Client
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from pyfcm import FCMNotification
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response

from .models import Ride, DriverLocation, calculate_route
from .serializers import RideSerializer

CLIENT_PUSH_SERVICE = FCMNotification(api_key=settings.FIREBASE_CLIENT_KEY)


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


@api_view(['POST'])
@authentication_classes((CsrfExemptSessionAuthentication, BasicAuthentication, TokenAuthentication))
def request_ride(request):
    client = request.user.client
    if len(client.rides.filter(active=True, deleted=False)) > 0:
        ride_serialized = RideSerializer(client.rides.filter(active=True, deleted=False)[0])
        return Response({
            "error": True,
            "message": "You have an active ride!",
            "ride": ride_serialized.data
        })
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
    route, eta_for_client = calculate_route(client.id)
    print route
    print eta_for_client
    ride.initial_eta = eta_for_client
    ride.save()
    ride_serialized = RideSerializer(ride)
    return Response({
        "success": True,
        "route": route,
        "ride": ride_serialized.data,
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
        route = calculate_route()
        '''
            TO DO: Send Push notifications to clients with new route
        '''
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
@authentication_classes((TokenAuthentication, CsrfExemptSessionAuthentication))
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


@api_view(['POST'])
@authentication_classes((CsrfExemptSessionAuthentication, TokenAuthentication))
def update_client_location(request):
    client = request.user.client
    latest_location = DriverLocation.objects.filter(latest=True)[:1]
    client.latitude = request.data.get("latitude")
    client.longitude = request.data.get("longitude")
    client.save()
    return Response({
        "success": True,
        "driver_latitude": latest_location.latitude,
        "driver_longitude": latest_location.longitude
    }, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@authentication_classes((CsrfExemptSessionAuthentication, TokenAuthentication))
def pickup_client(request):
    sjsu_id = request.data.get("sjsu_id", None)
    try:
        if sjsu_id:
            client = Client.objects.get(sjsu_id=sjsu_id)
            ride = client.rides.filter(active=True, deleted=False, serviced_by=None)
            if len(ride) > 0:
                ride = ride[0]
                ride.serviced_by = request.user.driver
                ride.pickup_at = timezone.now()
                ride.save()
                route = calculate_route()
                if ride.client.push_notification_token:
                    result = CLIENT_PUSH_SERVICE.notify_single_device(
                        registration_id=ride.client.push_notification_token,
                        data_message={"info": "pickup", "route": route},
                        message_body={"info": "pickup", "route": route})
                    print result
                return Response({
                    "route": route,
                    "success": True,
                    "message": "Pickup Successful. Route updated."
                })
            else:
                return Response({
                    "error": True,
                    "message": "Client does not have a ride scheduled"
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({
                "error": True,
                "message": "Invalid id"
            }, status=status.HTTP_404_NOT_FOUND)
    except ObjectDoesNotExist:
        return Response({
            "error": True,
            "message": "Invalid id"
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@authentication_classes((CsrfExemptSessionAuthentication, TokenAuthentication))
def drop_client(request):
    sjsu_id = request.data.get("sjsu_id", None)
    try:
        if sjsu_id:
            client = Client.objects.get(sjsu_id=sjsu_id)
            ride = client.rides.filter(active=True, deleted=False)
            if len(ride) > 0:
                ride = ride[0]
                ride.active = False
                ride.drop_at = timezone.now()
                ride.save()
                route = calculate_route()
                if ride.client.push_notification_token:
                    result = CLIENT_PUSH_SERVICE.notify_single_device(
                        registration_id=ride.client.push_notification_token,
                        data_message={"info": "drop"},
                        message_body={"info": "drop"})
                    print result
                return Response({
                    "route": route,
                    "success": True,
                    "message": "Drop Successful. Route updated."
                })
            else:
                return Response({
                    "error": True,
                    "message": "Client does not have a ride scheduled"
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({
                "error": True,
                "message": "Invalid id"
            }, status=status.HTTP_404_NOT_FOUND)
    except ObjectDoesNotExist:
        return Response({
            "error": True,
            "message": "Invalid id"
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes((CsrfExemptSessionAuthentication, TokenAuthentication))
def get_driver_location(request):
    driver_location = DriverLocation.objects.filter(latest=True)
    try:
        driver_location = driver_location[0]
        return Response({
            "latitude": driver_location.latitude,
            "longitude": driver_location.longitude,
            "last_updated": driver_location.timestamp,
            "driver": "%s %s" % (driver_location.driver.user.first_name, driver_location.driver.user.last_name)
        })
    except:
        return Response({"error": True, "message": "Location not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes((CsrfExemptSessionAuthentication, TokenAuthentication))
def get_current_route(request):
    route = calculate_route()
    return Response(route)


@api_view(['POST'])
@authentication_classes((CsrfExemptSessionAuthentication, TokenAuthentication))
def update_client_token(request):
    if hasattr(request.user, "client"):
        token = request.data.get("token")
        request.user.client.push_notification_token = token
        request.user.client.save()
        return Response({}, status=status.HTTP_201_CREATED)
    else:
        return Response({
            "error": True,
            "message": "Client not found."
        }, status=status.HTTP_400_BAD_REQUEST)
