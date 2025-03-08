from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from opencage.geocoder import OpenCageGeocode
from opencage.geocoder import RateLimitExceededError, InvalidInputError, UnknownError

from django.core.cache import cache
from django.conf import settings


# Initialize OpenCageGeocode with your API key
geocoder = OpenCageGeocode(settings.OPENCAGE_API_KEY)

# Create your views here.

def home(request): 
    return render(request, "routes.html")

def directions(request):
    return render(request, "directions.html")


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
    
@csrf_exempt
def optimization(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)

            # Validate required fields
            if 'vehicles' not in data or 'jobs' not in data:
                return JsonResponse({'error': 'Missing "vehicles" or "jobs" in request body'}, status=400)


            vroom_url = 'http://vroom-api-url/optimize' 
            headers = {
                'Authorization': request.headers.get('Authorization', ''),  
                'Content-Type': 'application/json',
            }
            response = requests.post(vroom_url, json=data, headers=headers)

            # Check if the VROOM API call was successful
            if response.status_code == 200:
                return JsonResponse(response.json(), status=200)
            else:
                return JsonResponse({'error': 'VROOM API error', 'details': response.text}, status=response.status_code)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

