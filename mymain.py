from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time

driver = webdriver.Chrome()

driver.get("https://www.pvrcinemas.lk")

title = driver.title

driver.implicitly_wait(4)

movie_actions = driver.find_elements(By.XPATH, '//a[text()="Book Tickets"]')

#<li _ngcontent-cbs-c125="" class="ng-star-inserted"><span _ngcontent-cbs-c125="" class="slot text-success">4:45 PM</span><!----><!----><!----><!----><!----><!----></li>
links = []
for action in movie_actions:
    if(action.get_property("href").startswith("https://")):
        links.append(action.get_property("href"))

print(f"{len(links)} movies found")

movie_names = []
seat_counts = []
prices = []


for link in links:
    driver.get(link)
    time.sleep(2)  

    li_elements = driver.find_elements(By.CSS_SELECTOR, "span.slot")
    for li in li_elements:
        try:
            # Scroll element into view
            driver.execute_script("arguments[0].scrollIntoView(true);", li)
            time.sleep(1)  

            # Wait for the element to be clickable
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span.slot")))

            li.click()

            time.sleep(2)

            # Get movie name
            m_name = driver.find_element(By.CSS_SELECTOR, "h4.modal-title").text
            movie_names.append(m_name)

            # Find all empty seats
            empty_seats = driver.find_elements(By.CSS_SELECTOR, "span.seat.current")
            seat_counts.append(len(empty_seats))  # Number of available seats

            # Get the price data
            price_data = driver.find_element(By.CSS_SELECTOR, "span.area").text
            get_num = re.search(r'\d+(\.\d+)?', price_data)  # Getting the price using regex
            if get_num:
                prices.append(get_num.group())
            else:
                prices.append("N/A")  # If price not found

        except Exception as e:
            print(f"Error processing movie at {link}: {e}")


for i in range(len(movie_names)):
    print(f"Movie Name: {movie_names[i]}")
    print(f"Empty Seats: {seat_counts[i]}")
    print(f"Price: {prices[i]}")
    print("-" * 30)


driver.quit()