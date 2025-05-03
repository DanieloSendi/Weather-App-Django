from django.shortcuts import render

# Create your views here.
import os
import requests
from django_ratelimit.decorators import ratelimit
from .models import City
from .forms import WeatherQueryForm
from django.http import JsonResponse


API_KEY = os.getenv("API_WEATHER_KEY")
BASE_URL = 'https://api.weatherapi.com/v1'

@ratelimit(key='ip', rate='6/s', method='POST', block=True)
def index_view(request):
    
    form = WeatherQueryForm()
    data_dict = {} 
    
    if request.method == "POST":
        form = WeatherQueryForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city'].strip()
            params = {"key": API_KEY, "q": city, "aqi": "no",}
            
            try:
                response = requests.get(f'{BASE_URL}/current.json', params=params)
                # Checking for https errors
                response.raise_for_status()
                # Convert the JSON data to a Python dictionary
                list_data = response.json()

                if "error" in list_data and "message" in list_data["error"]:
                    data_dict = {"error": f"API error: {list_data['error']['message']}"}
                else:
                    # Map weather data to the dictionary
                    data_dict = {
                        "city": str(list_data['location']['name']),
                        "country_code": str(list_data['location']['country']),
                        "coordinate": str(list_data['location']['lon']) + ', ' + str(list_data['location']['lat']),
                        "temp": str(list_data['current']['temp_c']) + ' °C',
                        "pressure": str(list_data['current']['pressure_mb']) + ' hPa',
                        "humidity": str(list_data['current']['humidity']) + ' %',
                        "main": str(list_data['current']['condition']['text']),
                        "icon": list_data['current']['condition']['icon'],
                    }
                    print(data_dict)
                    
                    # Save the data to the database
                    City.objects.create(
                        city=city,
                        country_code=data_dict["country_code"],
                        temperature=data_dict["temp"],
                        pressure=data_dict["pressure"],
                        humidity=data_dict["humidity"],
                        main=data_dict["main"],
                        icon=data_dict["icon"],
                    )
                
            except requests.exceptions.Timeout:
                data_dict = {"error": "The request timed out. Please try again later."}
            except requests.exceptions.ConnectionError:
                data_dict = {"error": "Could not connect to the weather service. Check your internet connection."}
            except requests.exceptions.RequestException:
                data_dict = {"error": "Unexpected error. Please try again later."}
            # except requests.exceptions.RequestException as e:
            #     data_dict = {"error": f"Data fetch error: {e}"}    
                
    context = {"form": form, "data_dict": data_dict}
    return render(request, 'index.html', context=context)


@ratelimit(key='ip', rate='6/s', method='GET', block=True)
def autocomplete_view(request):
    query = request.GET.get('q', '')
    if not query:
        return JsonResponse([], safe=False)
    
    params = {"key": API_KEY, "q": query, "aqi": "no"}
    try:
        response = requests.get(f'{BASE_URL}/search.json', params=params)
        response.raise_for_status()
        cities = response.json()
        return JsonResponse(cities, safe=False)
    except requests.RequestException:
        return JsonResponse([], safe=False)