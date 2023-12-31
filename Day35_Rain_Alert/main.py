import requests
import os
from twilio.rest import Client


account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')

virtual_number = os.environ.get('TWILIO_VIRTUAL_NUMBER')
verified_number = os.environ.get('VERIFIED_REAL_NUMBER')

OWM_Endpoint = "https://api.weatherapi.com/v1/forecast.json?"
app_key = os.environ.get('APP_KEY')

weather_params = {
    "key": app_key,
    "q": "Stuttgart",
    "days": 1,
}

responce = requests.get(OWM_Endpoint, params=weather_params)
responce.raise_for_status()
weather_data = responce.json()
is_day = weather_data["current"]["is_day"]
will_it_rain = weather_data["forecast"]["forecastday"][0]["day"]["daily_will_it_rain"]

if int(is_day) == 1 and will_it_rain == 0:
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
            body="It's going to rain today. Remember to bring an Umbrella!",
            from_=virtual_number,
            to=verified_number,
        )

    print(message.sid)
    print(message.status)
