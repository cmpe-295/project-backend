# Create your views here.
import json
import uuid

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseNotAllowed
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response

from .serializers import ClientSerializer
from .helpers import send_activation_email
from .api import DriverSerializer
from .models import Driver, SiteUser, Client


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


@api_view(['GET'])
def list_drivers(request):
    drivers = Driver.objects.all()
    serialized = DriverSerializer(drivers, many=True)
    return Response(serialized.data)


@csrf_exempt
def client_sign_up(request):
    if request.method == 'POST':
        request_as_json = json.loads(request.body)
        email = request_as_json.get("email", None)
        password = request_as_json.get("password", None)
        first_name = request_as_json.get("first_name", None)
        last_name = request_as_json.get("last_name", None)
        sjsu_id = request_as_json.get("sjsu_id", None)
        if email and password and first_name and last_name and sjsu_id:

            existing_user_email = SiteUser.objects.filter(email=email)
            existing_user_sjsu_id = Client.objects.filter(sjsu_id=sjsu_id)
            if len(existing_user_email) > 0 or len(existing_user_sjsu_id) > 0:
                return HttpResponseBadRequest("User with similar email or SJSU ID exists")
            link = str(uuid.uuid4())
            user = SiteUser(email=email, is_active=False, first_name=first_name, last_name=last_name)
            user.set_password(password)
            user.save()
            client = Client(user=user, sjsu_id=sjsu_id, activation_link_offset=link)
            client.save()
            link = "%sactivate_app/%s/" % (settings.API_URL, link)
            send_activation_email(user.email, link)
            return JsonResponse(
                {"success": True, "message": "Email has been sent. Please click on the link to activate your account"})
        else:
            return JsonResponse({"error": True, "message": "One or more field(s) are empty."})
    else:
        return HttpResponseNotAllowed(['POST'])


def activate_app(request, activation_string):
    try:
        client = Client.objects.get(activation_link_offset=activation_string)
        client.email_verified = True
        client.activation_link_offset = ""
        client.save()
        client.user.is_active = True
        client.user.save()
        return HttpResponse("Your account is now active!")
    except (ObjectDoesNotExist, MultipleObjectsReturned) as e:
        return HttpResponseBadRequest("Invalid Activation URL")


def home(request):
    return HttpResponse("Spartan safe ride project site")


@api_view(['GET'])
@authentication_classes((CsrfExemptSessionAuthentication, BasicAuthentication, TokenAuthentication))
def get_info(request):
    if hasattr(request.user, "client"):
        serialized = ClientSerializer(request.user.client)
        return Response(serialized.data, status=status.HTTP_200_OK)
    else:
        return Response({
            "error": True,
            "message": "Client not found or wrong auth token"
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@authentication_classes((CsrfExemptSessionAuthentication, BasicAuthentication, TokenAuthentication))
def update_device_token(request):
    if hasattr(request.user, "driver"):
        token = request.POST.get("token")
        request.user.driver.push_notification_token = token
        request.user.driver.save()
        return Response({}, status=status.HTTP_201_CREATED)
    else:
        return Response({
            "error": True,
            "message": "Driver not found."
        }, status=status.HTTP_400_BAD_REQUEST)
