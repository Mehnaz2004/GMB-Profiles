from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

# Set up Chrome to run in the background (headless mode)
chrome_options = Options()
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")

# Specify the path to the ChromeDriver and start the browser
webdriver_path = 'C:/Users/mehna/Downloads/chromedriver-win64/chromedriver.exe'
driver = webdriver.Chrome(service=Service(webdriver_path), options=chrome_options)

def extract_details(url):
    driver.get(url)  # Open the page
    
    wait = WebDriverWait(driver, 15)  # Wait up to 15 seconds for elements to load
    
    # Initialize dictionary to store the details
    details = {
        'name': None,
        'address': None,
        'phone_number': None,
        'hours_of_operation': [],
        'website': None,
        'review_score': None
    }
    
    try:
        # Extract the name, address, phone number, website, hours, and review score
        try:
            details['name'] = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'h1.DUwDvf.lfPIob'))).text.strip()
        except Exception as e:
            print(f"Error extracting name: {e}")
        
        try:
            details['address'] = driver.find_element(By.CSS_SELECTOR, 'button.CsEnBe[aria-label*="Address:"]').get_attribute('aria-label').replace('Address: ', '').strip()
        except Exception as e:
            print(f"Error extracting address: {e}")
        
        try:
            details['phone_number'] = driver.find_element(By.CSS_SELECTOR, 'button.CsEnBe[aria-label*="Phone:"]').get_attribute('aria-label').replace('Phone: ', '').strip()
        except Exception as e:
            print(f"Error extracting phone number: {e}")
        
        try:
            details['website'] = driver.find_element(By.CSS_SELECTOR, 'a.CsEnBe[aria-label*="Website:"]').get_attribute('href').strip()
        except Exception as e:
            print(f"Error extracting website URL: {e}")
        
        try:
            details['hours_of_operation'] = driver.find_element(By.CSS_SELECTOR, 'div.t39EBf.GUrTXd').get_attribute('aria-label').strip()
        except Exception as e:
            print(f"Error extracting hours of operation: {e}")
            
        try:
            details['review_score'] = driver.find_element(By.CSS_SELECTOR, 'div.YTkVxc.ikjxab').get_attribute('aria-label').strip()
        except Exception as e:
            print(f"Error extracting review score: {e}")
        
    except Exception as e:
        print(f"Error extracting details for {url}: {e}")
    
    return details  # Return the collected details

# List to hold all the data
data = []

try:
    # Open Google Maps search for escape rooms and scroll to load more results
    driver.get("https://www.google.com/maps/search/escape+rooms/@19.5810477,74.5619042,4z/data=!4m2!2m1!6e1?entry=ttu")
    wait = WebDriverWait(driver, 15)
    results_container = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.m6QErb.DxyBCb.kA9KIf.dS8AEf.XiKgde.ecceSd[aria-label='Results for escape rooms']")))

    for _ in range(30):  # Scroll through the results to load more
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", results_container)
        time.sleep(2)  # Wait for content to load

    # Get links to each result and extract details for each one
    a_tags = driver.find_elements(By.CLASS_NAME, "hfpxzc")
    hrefs = [tag.get_attribute('href') for tag in a_tags]
    for href in hrefs:
        details = extract_details(href)
        data.append(details)
finally:
    driver.quit()  # Close the browser when done

# Save the data to a JSON file
with open('escape_rooms_data.json', 'w') as f:
    json.dump(data, f, indent=4)

print("Data extraction complete. JSON file created.")
