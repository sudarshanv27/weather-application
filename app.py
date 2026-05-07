from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get API key from environment variable (SECURE!)
API_KEY = os.getenv('OPENWEATHER_API_KEY')

# Fallback for development (remove in production)
if not API_KEY:
    print("⚠️ Warning: OPENWEATHER_API_KEY not found in .env file")
    API_KEY = 'your-api-key-here'  # Only for testing

@app.route('/', methods=['GET', 'POST'])
def home():
    weather_data = None
    error_message = None
    
    if request.method == 'POST':
        city = request.form.get('city')
        
        if city:
            # Make API request to OpenWeatherMap
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=imperial"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                weather_data = {
                    'city': city.title(),
                    'temperature': round(data['main']['temp']),
                    'description': data['weather'][0]['description'].title(),
                    'humidity': data['main']['humidity'],
                    'wind_speed': data['wind']['speed'],
                    'condition': data['weather'][0]['main']
                }
            else:
                error_message = f"City '{city}' not found. Please check spelling."
    
    return render_template('weather.html', weather=weather_data, error=error_message)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)