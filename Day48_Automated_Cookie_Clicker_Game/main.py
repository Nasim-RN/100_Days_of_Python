from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Keep the browser open
chrome_option = webdriver.ChromeOptions()
chrome_option.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_option)

driver.get("https://orteil.dashnet.org/cookieclicker/")

# Click on consent button
consent_button = driver.find_element(By.CLASS_NAME,"fc-button-label")
consent_button.click()

# Select language
lang_select_buttom = driver.find_element(By.ID,"langSelect-EN")
lang_select_buttom.click()

# Get cookie, grandma, cursor to click on
cookie = driver.find_element(By.ID,"bigCookie")
farm = driver.find_element(By.ID, "product2")
grandma = driver.find_element(By.ID, "product1")
cursor = driver.find_element(By.ID, "product0")

def purchase_if_possible():
    cookies_number = int(driver.find_element(By.ID, "cookies").text.replace(",", "").split()[0])
    farm_price = int(driver.find_element(By.ID, "productPrice2").text.replace(",", ""))
    grandma_price = int(driver.find_element(By.ID, "productPrice1").text.replace(",", ""))
    cursor_price = int(driver.find_element(By.ID, "productPrice0").text.replace(",", ""))

    if cookies_number >= farm_price:
        farm.click()
    elif cookies_number >= grandma_price:
        grandma.click()
    elif cookies_number >= cursor_price:
        cursor.click()
    else:
        cookie_clicker()


def cookie_clicker():
    timeout = time.time() + 5
    while time.time() < timeout:
        cookie.click()
    else:
        purchase_if_possible()

count = 0

while count < 60:
    cookie_clicker()
    count += 1
    print(count)


