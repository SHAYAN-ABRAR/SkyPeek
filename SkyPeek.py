import tkinter as tk
from tkinter import messagebox
import requests

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("400x300")

        # Create and configure the main frame
        self.frame = tk.Frame(self.root, padx=10, pady=10)
        self.frame.pack(expand=True, fill="both")

        # City input
        self.city_label = tk.Label(self.frame, text="Enter City:", font=("Arial", 12))
        self.city_label.pack(pady=5)

        self.city_entry = tk.Entry(self.frame, font=("Arial", 12))
        self.city_entry.pack(pady=5)
        self.city_entry.insert(0, "Ishwardi")

        # Get Weather button
        self.weather_button = tk.Button(self.frame, text="Get Weather", command=self.get_weather, font=("Arial", 12))
        self.weather_button.pack(pady=10)

        # Weather display
        self.result_label = tk.Label(self.frame, text="", font=("Arial", 12), wraplength=350, justify="left")
        self.result_label.pack(pady=10)

    def get_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showerror("Error", "Please enter a city name")
            return

        # Fetch coordinates
        geocode_url = f'https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1'
        try:
            geocode_response = requests.get(geocode_url)
            geocode_response.raise_for_status()
            geocode_data = geocode_response.json()

            if 'results' in geocode_data and geocode_data['results']:
                lat = geocode_data['results'][0]['latitude']
                lon = geocode_data['results'][0]['longitude']
                country = geocode_data['results'][0].get('country', 'Unknown')

                # Fetch weather
                weather_url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code'
                weather_response = requests.get(weather_url)
                weather_response.raise_for_status()
                weather_data = weather_response.json()
                current = weather_data['current']

                temp = current['temperature_2m']
                humidity = current['relative_humidity_2m']
                wind_speed = current['wind_speed_10m']
                weather_code = current['weather_code']

                # Weather description mapping
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

                # Display results
                result_text = (f"Current weather in {city}, {country}:\n"
                             f"Temperature: {temp}°C\n"
                             f"Description: {weather_desc}\n"
                             f"Humidity: {humidity}%\n"
                             f"Wind Speed: {wind_speed} km/h")
                self.result_label.config(text=result_text)

            else:
                messagebox.showerror("Error", "City not found. Try a different name or add country (e.g., 'London,UK').")
        except requests.RequestException:
            messagebox.showerror("Error", "Could not fetch data. Check your connection or try again.")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()