import requests

city = 'Mohammadpur'  

geocode_url = f'https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1'  
geocode_response = requests.get(geocode_url)

if geocode_response.status_code == 200:
    geocode_data = geocode_response.json()
    if 'results' in geocode_data and geocode_data['results']:
        lat = geocode_data['results'][0]['latitude']
        lon = geocode_data['results'][0]['longitude']
        country = geocode_data['results'][0].get('country', 'Unknown') 
       
        weather_url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code'
        weather_response = requests.get(weather_url)
        
        if weather_response.status_code == 200:
            weather_data = weather_response.json()
            current = weather_data['current']
            
            temp = current['temperature_2m']
            humidity = current['relative_humidity_2m']
            wind_speed = current['wind_speed_10m']
            weather_code = current['weather_code'] 
          
            weather_desc = {
                0: 'Clear sky',
                1: 'Mainly clear',
                2: 'Partly cloudy',
                3: 'Overcast',
                45: 'Fog',
                51: 'Light drizzle',
                61: 'Light rain',
                71: 'Light snow',
                80: 'Rain showers',
                95: 'Thunderstorm',
            }.get(weather_code, 'Unknown')
            
            print(f"Current weather in {city}, {country}:")
            print(f"Temperature: {temp}°C")
            print(f"Description: {weather_desc}")
            print(f"Humidity: {humidity}%")
            print(f"Wind Speed: {wind_speed} km/h")
        else:
            print("Error: Could not fetch weather data.")
    else:
        print("Error: City not found. Try a different name or add country (e.g., 'London,UK').")
else:
    print("Error: Could not fetch location data.")