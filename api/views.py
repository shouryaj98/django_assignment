from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
from .validators import validate_finite_values_entity, validate_numeric_entity

def index(request):
    return HttpResponse("Welcome. Accessible POST APIs are /finite_values_entity and /numeric_entity")

@csrf_exempt
def finite_values_entity(request):
    if request.method == 'POST':
        try:
            json_body = json.loads(request.body.decode(encoding='UTF-8'))
            validation_result = validate_finite_values_entity(**json_body)
            return JsonResponse({
                "filled": validation_result[0],
                "parially_filled": validation_result[1],
                "trigger": validation_result[2],
                "parameters": validation_result[3]
            })
        except Exception:
            return HttpResponseBadRequest("JSON format is invalid.")
    return HttpResponse("Send a POST request with the required JSON payload.")

@csrf_exempt
def numeric_entity(request):
    if request.method == 'POST':
        try:
            json_body = json.loads(request.body.decode(encoding='UTF-8'))
            validation_result = validate_numeric_entity(**json_body)
            return JsonResponse({
                "filled": validation_result[0],
                "parially_filled": validation_result[1],
                "trigger": validation_result[2],
                "parameters": validation_result[3]
            })
        except Exception:
            return HttpResponseBadRequest("JSON format is invalid.")
    return HttpResponse("Send a POST request with the required JSON payload.")