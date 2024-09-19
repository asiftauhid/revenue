from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import csv

driver = webdriver.Chrome()

driver.get("https://www.pvrcinemas.lk")

title = driver.title

driver.implicitly_wait(4)

movie_actions = driver.find_elements(By.XPATH, '//a[text()="Book Tickets"]')

links = []
for action in movie_actions:
    if(action.get_property("href").startswith("https://")):
        links.append(action.get_property("href"))

print(f"{len(links)} movies found")

movie_names = []
seat_counts = []
prices = []
times = []

for link in links:
    driver.get(link)
    driver.implicitly_wait(5)

    li_elements = driver.find_elements(By.CSS_SELECTOR, "span.slot.text-success")
    try:
        m_name = driver.find_element(By.CSS_SELECTOR, "h5.modal-title").text
    except:
        m_name = "N/A"
    print(f"Processing movie: {m_name}, Link: {link}, Number of slots: {len(li_elements)}")
    
    if len(li_elements) == 0:
        # If no time slots found, append N/A values
        movie_names.append(m_name)
        times.append("N/A")
        seat_counts.append("N/A")
        prices.append("N/A")
        print(f"No time slots found for movie: {m_name}")
        continue

    for li_count in range(len(li_elements)):
        try:
            driver.implicitly_wait(5)
            li = driver.find_elements(By.CSS_SELECTOR, "span.slot.text-success")[li_count]
            driver.execute_script("arguments[0].scrollIntoView(true);", li)
            driver.implicitly_wait(5) 

            target_slot = li.find_element(By.XPATH, "..")
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(target_slot))

            time_slot = li.text
            target_slot.click()

            driver.implicitly_wait(5)

            movie_names.append(m_name)
            times.append(time_slot)

            empty_seats = driver.find_elements(By.CSS_SELECTOR, "span.seat.current")
            seat_counts.append(len(empty_seats))

            try:
                price_data = driver.find_element(By.CSS_SELECTOR, "span.area").text
                get_num = re.search(r'\d+(\.\d+)?', price_data)
                prices.append(get_num.group() if get_num else "N/A")
            except:
                prices.append("N/A")

            print(f"Movie Name: {m_name}, Time: {time_slot}, Empty Seats: {seat_counts[-1]}, Price: {prices[-1]}")

            driver.back()

        except Exception as e:
            print(f"Error processing movie at {link}: {e}")
            # Append N/A values if an error occurs
            if len(movie_names) > len(times):
                times.append("N/A")
            if len(movie_names) > len(seat_counts):
                seat_counts.append("N/A")
            if len(movie_names) > len(prices):
                prices.append("N/A")

print(f"Lengths - movie_names: {len(movie_names)}, times: {len(times)}, seat_counts: {len(seat_counts)}, prices: {len(prices)}")

#exporting data to csv
csv_data = []
for i in range(len(movie_names)):
    csv_data.append([movie_names[i], times[i], seat_counts[i], prices[i]])

# Export data to CSV
csv_filename = 'movie_data.csv'
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    # Write header
    csv_writer.writerow(['Movie Names', 'Showtimes', 'Empty Seats', 'Ticket Pricing (LKR)'])
    # Write data
    csv_writer.writerows(csv_data)

print(f"Data has been exported to {csv_filename}")

driver.quit()