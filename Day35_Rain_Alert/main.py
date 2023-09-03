import requests
import os
from twilio.rest import Client


account_sid = os.environ['TWILIO_ACCOUNT_SID'] = "AC5e6941ed7df36d686154dba462c5626d"
auth_token = os.environ['TWILIO_AUTH_TOKEN'] = "9e6ae4e8daf4e5c065c9eea0552a9b1b"

OWM_Endpoint = "https://api.weatherapi.com/v1/forecast.json?"
app_key = "5cc89e99660549a584a154852230309"

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

if int(is_day) == 1 and will_it_rain == 1:
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
            body="It's going to rain today. Remember to bring an Umbrella!",
            from_='+15075449355',
            to='+4915754413840'
        )

    print(message.sid)
    print(message.status)
