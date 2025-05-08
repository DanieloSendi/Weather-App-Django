from django.shortcuts import render

# Create your views here.
import os
import requests
from django_ratelimit.decorators import ratelimit
from .forms import WeatherQueryForm
from django.http import JsonResponse
from datetime import datetime


API_KEY = os.getenv("API_WEATHER_KEY")
BASE_URL = 'https://api.weatherapi.com/v1'


@ratelimit(key='ip', rate='6/min', method='POST', block=True)
def index_view(request):
    form = WeatherQueryForm()
    current_weather = {}
    forecast_days = []
    
    if request.method == "POST":
        form = WeatherQueryForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city'].strip()
            params = {"key": API_KEY, "q": city, "days": 3, "aqi": "yes"}
            
            try:
                response = requests.get(f'{BASE_URL}/forecast.json', params=params)
                # Convert the JSON data to a python dictionary
                data = response.json()

                if "error" in data:
                    error_message = data["error"].get("message", "Unknown error")
                    if "No matching location found" in error_message:
                        current_weather = {"error": "Sorry, no matching city was found. Please try again."}
                    else:
                        current_weather = {"error": f"Weather API Error: {error_message}"}
                else:
                    
                    # Checking for https errors
                    response.raise_for_status()
                    
                    epa_index = data['current']['air_quality']['us-epa-index']
                    epa_description = {
                        1: "Good",
                        2: "Moderate",
                        3: "Unhealthy for Sensitive Group",
                        4: "Unhealthy",
                        5: "Very Unhealthy",
                        6: "Hazardous"
                    }.get(epa_index, "Unknown")
                    
                    epa_color = {
                        "Good": "success",
                        "Moderate": "warning",
                        "Unhealthy for Sensitive Group": "orange",
                        "Unhealthy": "danger",
                        "Very Unhealthy": "danger",
                        "Hazardous": "dark"
                    }.get(epa_description, "secondary")
                    
                    # Current weather parameters map to the dictionary
                    current_weather = {
                        "city": str(data['location']['name']),
                        "country_code": str(data['location']['country']),
                        "coordinate": str(data['location']['lon']) + ', ' + str(data['location']['lat']),
                        "temp": str(data['current']['temp_c']) + ' °C',
                        "pressure": str(data['current']['pressure_mb']) + ' hPa',
                        "humidity": str(data['current']['humidity']) + ' %',
                        "main": str(data['current']['condition']['text']),
                        "icon": data['current']['condition']['icon'],
                        "epa_description": epa_description,
                        "epa_color": epa_color,
                    }

                    # Forecast (for the next days)
                    forecast_days = []
                    for day in data['forecast']['forecastday'][1:]:
                        date_object = datetime.strptime(day['date'], "%Y-%m-%d")
                        day_name = date_object.strftime("%A")
                        
                        forecast_days.append({
                            "date": day['date'],
                            "day_name": day_name,
                            "avg_temp": str(day['day']['avgtemp_c']) + ' °C',
                            "condition": day['day']['condition']['text'],
                            "icon": day['day']['condition']['icon'],
                        })
                
            except requests.exceptions.Timeout:
                current_weather = {"error": "The request timed out. Please try again later."}
            except requests.exceptions.ConnectionError:
                current_weather = {"error": "Could not connect to the weather service. Check your internet connection."}
            except requests.exceptions.RequestException:
                current_weather = {"error": "Unexpected error. Please try again later."}
            # except requests.exceptions.RequestException as e:
            #     current_weather = {"error": f"Unexpected error occurred: {str(e)}"}
            
    context = {
        "form": form,
        "current_weather": current_weather,
        "forecast_days": forecast_days
    }
    return render(request, 'index.html', context=context)


def autocomplete_view(request):
    query = request.GET.get('q', '').strip()
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
