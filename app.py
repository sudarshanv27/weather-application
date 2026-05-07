from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Your OpenWeatherMap API key
API_KEY = '4c108f2458202a2bc4038130ca9d350e'

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
                error_message = f"City '{city}' not found. Please check the spelling and try again."
    
    return render_template('weather.html', weather=weather_data, error=error_message)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)