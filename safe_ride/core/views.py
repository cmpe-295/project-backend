# Create your views here.
import json

from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view
from rest_framework.response import Response

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
            # send email
            return HttpResponse("Email has been sent. Please click on the link to activate your account")
        else:
            return HttpResponseBadRequest("One or more field(s) are empty.")
    else:
        return HttpResponseNotAllowed(['POST'])
