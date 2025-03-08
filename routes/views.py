from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from django.core.cache import cache
from django.conf import settings

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
                'Authorization': request.headers.get('Authorization', ''),  # Pass the Authorization header
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


@csrf_exempt
def geocode(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            place_name = data.get('place_name')

            if not place_name:
                return JsonResponse({'error': 'Missing "place_name" in request body'}, status=400)

            # Check if the result is already cached
            cache_key = f'geocode_{place_name}'
            cached_result = cache.get(cache_key)
            if cached_result:
                return JsonResponse(cached_result)

            # Call the OpenCage API
            url = f'https://api.opencagedata.com/geocode/v1/json?q={place_name}&key={OPENCAGE_API_KEY}'
            response = requests.get(url)

            if response.status_code == 200:
                results = response.json().get('results', [])
                if results:
                    first_result = results[0]
                    geometry = first_result.get('geometry', {})
                    lat = geometry.get('lat')
                    lng = geometry.get('lng')
                    formatted_address = first_result.get('formatted')

                    result = {
                        'place_name': place_name,
                        'formatted_address': formatted_address,
                        'latitude': lat,
                        'longitude': lng,
                    }

                    # Cache the result for 1 hour
                    cache.set(cache_key, result, timeout=3600)

                    return JsonResponse(result)
                else:
                    return JsonResponse({'error': 'No results found'}, status=404)
            else:
                return JsonResponse({'error': 'OpenCage API error', 'details': response.text}, status=response.status_code)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)