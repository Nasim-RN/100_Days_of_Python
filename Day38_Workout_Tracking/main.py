import os
import requests
from datetime import datetime

GENDER = "female"
WEIGHT_KG = 60
HEIGHT_CM = 160
AGE = 28


APP_ID = os.environ['NUTRITION_APP_ID']
API_KEY = os.environ['NUTRITION_API_KEY']

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = os.environ['SHEET_ENDPOINT']

exercise_text = input("Tell me which exercises you did: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}


user_params = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(exercise_endpoint, json=user_params, headers=headers)
result = response.json()
print(f"Nutritionix API call: \n {result} \n")


# Adding date and time
today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

# Sheety API Call & Authentication
for exercise in result["exercises"]:
    sheet_inputs = {
        "sheet1": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }
    print(sheet_inputs)

    sheet_response = requests.post(url=sheet_endpoint, json=sheet_inputs)
    print(f"Sheety Response: \n {sheet_response.text}")