import requests
import os
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"


STOCK_API_KEY = os.environ.get('ALPHAVANTAGE')
NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
TWILIO_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')

VIRTUAL_NUMBER = os.environ.get('TWILIO_VIRTUAL_NUMBER')
VERIFIED_NUMBER = os.environ.get('VERIFIED_REAL_NUMBER')


# Get yesterday's closing stock price
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}
response = requests.get(STOCK_ENDPOINT, params=stock_params)
data = response.json()['Time Series (Daily)']
print(data)
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = float(yesterday_data["4. close"])
print(yesterday_closing_price)


# Get the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = float(day_before_yesterday_data["4. close"])
print(day_before_yesterday_closing_price)


# Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20.
difference = yesterday_closing_price - day_before_yesterday_closing_price
print(difference)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

# Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday
diff_percent = round((difference / yesterday_closing_price) * 100)
print(diff_percent)

# If difference percentage is greater than 5 then use the News API to get the first 3 news pieces for the COMPANY_NAME.
if abs(diff_percent) >= 5:
    news_params = {
        "apikey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    news_responce = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_responce.json()["articles"]
    print(articles)
# Use Python slice operator to create a list that contains the first 3 articles.
    three_articles = articles[:3]
    print(three_articles)


# Create a new list of the first 3 article's headline and description using list comprehension.
    formatted_articles = [(f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}\n"
                           f"Brief: {article['description']}") for article in three_articles]
    print(formatted_articles)

# Send each article as a separate message via Twilio.
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=VIRTUAL_NUMBER,
            to=VERIFIED_NUMBER,
        )
        print(message.sid)
        print(message.status)
