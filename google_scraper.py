from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

def scrape_google(source, destination, travel_date):
    try:
        date_str = travel_date.strftime("%Y-%m-%d")
        url = f"https://www.google.com/travel/flights?q=flights+from+{source}+to+{destination}+on+{date_str}"

        options = Options()
        # options.add_argument("--headless")  # disable headless for debugging
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        driver = webdriver.Chrome(options=options)
        driver.get(url)
        wait = WebDriverWait(driver, 30)

        # First, try a more specific xpath for fare price (the container with itinerary-price)
        price_elem = None
        try:
            price_elem = wait.until(EC.presence_of_element_located((
                By.XPATH, "//div[contains(@class,'gws-flights-results__itinerary-price')]"
            )))
        except:
            # Fallback to the previous selector
            price_elem = wait.until(EC.presence_of_element_located((
                By.XPATH, "//div[contains(@class,'YMlIz')]"
            )))

        # Wait for the airline element
        airline_elem = wait.until(EC.presence_of_element_located((
            By.XPATH, "//span[contains(@class,'sSHqwe')]"
        )))

        price_text = price_elem.text.strip().replace("₹", "").replace(",", "")
        # If price_text contains time indicators, then it’s not a fare price.
        if "AM" in price_text or "PM" in price_text:
            driver.quit()
            return None, "GoogleScraperNoData"
        
        try:
            price = float(price_text)
        except ValueError:
            driver.quit()
            return None, "GoogleScraperInvalidPrice"

        airline = airline_elem.text.strip()
        driver.quit()
        return price, airline

    except Exception as e:
        print("Google scraper error:", e)
        try:
            driver.quit()
        except Exception:
            pass
        return None, "GoogleScraperError"
