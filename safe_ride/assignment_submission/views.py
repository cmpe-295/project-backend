import json

from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from django.shortcuts import render


# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from .models import AssignmentSubmission


@csrf_exempt
def store_lab_2(request):
    if request.method == 'POST':
        request_as_json = json.loads(request.body)
        email_id = request_as_json.get("email_id", None)
        script_hash = request_as_json.get("script_hash", None)
        first_name = request_as_json.get("first_name", None)
        last_name = request_as_json.get("last_name", None)
        student_id = request_as_json.get("sjsu_id", None)
        output = request_as_json.get("output", None)
        total_points = request_as_json.get("total_points", None)
        assignment_name = request_as_json.get("assignment_name", None)
        obj = AssignmentSubmission.objects.create(
            email_id=email_id,
            assignment_name=assignment_name,
            output=output,
            script_hash=script_hash,
            first_name=first_name,
            last_name=last_name,
            student_id=student_id,
            total_points=total_points
        )
        return HttpResponse("Success")
    else:
        return HttpResponseNotAllowed(['POST'])
