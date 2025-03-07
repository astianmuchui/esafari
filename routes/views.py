from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

def home(request):
    return render(request, "home.html")

@csrf_exempt
def streetmap_api(request):
    if request.method == 'GET':
        data = {
            'message': 'Hello, this is a GET request!',
            'status': 'success',
        }
        return JsonResponse(data)
    elif request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            response_data = {
                'message': 'Hello, this is a POST request!',
                'received_data': data,
                'status': 'success',
            }
            return JsonResponse(response_data)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

