import requests
from bs4 import BeautifulSoup
import smtplib
import os

MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")

URL = "https://www.amazon.com/2021-Apple-10-2-inch-iPad-Wi-Fi/dp/B09G9FPHY6/ref=lp_16225009011_1_7?sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

BUY_PRICE = 270
title = "Apple iPad (9th Generation):"


response = requests.get(URL, headers=headers)
response.raise_for_status()
data = response.text

soup = BeautifulSoup(data, "html.parser")
price = float(soup.find(name="span",class_= "a-offscreen").get_text().split("$")[1])
print(price)

if price < BUY_PRICE:
    message = f"{title} is now {price}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=MY_EMAIL,
                            msg=f"Subject:Amazon Price Alert!\n\n{message}\n{URL}".encode("utf-8"))



