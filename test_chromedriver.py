from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("--headless")  # Keeps the browser hidden (no popup)

try:
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.google.com")
    time.sleep(3)
    print("ChromeDriver is working correctly!")
    driver.quit()
except Exception as e:
    print("ChromeDriver failed to launch.")
    print(e)
