from selenium import webdriver
from selenium.webdriver.common.by import By

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

#<li _ngcontent-cbs-c125="" class="ng-star-inserted"><span _ngcontent-cbs-c125="" class="slot text-success">4:45 PM</span><!----><!----><!----><!----><!----><!----></li>
for link in links:
    driver.get(link)
    li_elements = driver.find_elements(By.CSS_SELECTOR, "span.slot")
    for li in li_elements:
        li.click()
        input("Test")


driver.quit()
