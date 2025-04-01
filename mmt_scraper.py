from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_mmt(source, destination, travel_date):
    try:
        options = Options()
        # options.add_argument("--headless")  # disable headless for debugging
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        driver = webdriver.Chrome(options=options)
        driver.get("https://www.makemytrip.com/flights/")
        wait = WebDriverWait(driver, 30)

        # Attempt to close the login popup if present
        try:
            close_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='commonModal__close']")))
            close_btn.click()
        except:
            pass

        # FROM city: click the label, then send keys, then wait for suggestion list and click first suggestion.
        from_label = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@for='fromCity']")))
        from_label.click()

        from_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='From']")))
        from_input.clear()
        from_input.send_keys(source)
        time.sleep(3)  # give extra time for suggestions to load

        try:
            # Click the first suggestion in the dropdown list
            suggestion = wait.until(EC.element_to_be_clickable((By.XPATH, "//ul[contains(@class,'react-autosuggest__suggestions-list')]/li[1]")))
            suggestion.click()
        except Exception as e:
            print(f"Could not select source airport: {source}")
            driver.quit()
            return None, "MMT_NoSourceAirport"

        # TO city: same procedure
        to_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='To']")))
        to_input.clear()
        to_input.send_keys(destination)
        time.sleep(3)
        try:
            suggestion = wait.until(EC.element_to_be_clickable((By.XPATH, "//ul[contains(@class,'react-autosuggest__suggestions-list')]/li[1]")))
            suggestion.click()
        except Exception as e:
            print(f"Could not select destination airport: {destination}")
            driver.quit()
            return None, "MMT_NoDestAirport"

        # Click Search button
        search_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Search')]")))
        search_btn.click()
        time.sleep(10)  # wait for results to load

        # Extract the price and airline from the first flight result
        price_elem = wait.until(EC.presence_of_element_located((
            By.XPATH, "//div[@class='blackText fontSize18 blackFont white-space-no-wrap clusterViewPrice']"
        )))
        airline_elem = wait.until(EC.presence_of_element_located((
            By.XPATH, "//span[@class='boldFont blackText airlineName']"
        )))

        price = float(price_elem.text.replace("₹", "").replace(",", "").strip())
        airline = airline_elem.text.strip()

        driver.quit()
        return price, airline

    except Exception as e:
        print("MMT scraper error:", e)
        try:
            driver.quit()
        except Exception:
            pass
        return None, "MMTScraperError"
