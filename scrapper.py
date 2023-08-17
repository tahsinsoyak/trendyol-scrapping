import time
from selenium import webdriver
import os
import requests
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# Set the path to the ChromeDriver executable
chrome_driver_path = r"C:\Users\Tahsin\Desktop\Proje\trendyol-scrapping\venv\chromedriver.exe"

# Create a Service object with the ChromeDriver path
service = Service(chrome_driver_path)

# Start the ChromeDriver service
service.start()

# Create a WebDriver instance
driver = webdriver.Chrome(service=service)

driver.get('https://www.trendyol.com/magaza/bilsen-store-m-207964?sst=0')
time.sleep(2)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

div_element = driver.find_element(by=By.XPATH, value='//*[@id="seller-store"]/div/div[2]/div/div[4]')

# Find all the anchor tags within the div element
link_elements = div_element.find_elements(By.TAG_NAME, 'a')

# Extract the href attribute from each anchor tag and store them in a list
links = [link.get_attribute('href') for link in link_elements]
time.sleep(2)
# Visit each link
folder_counter = 0
# Visit each link
for link in links:
    driver.get(link)
    
    time.sleep(2)
    # Extract the product ID from the link
    product_id = str(folder_counter)

    # Create a folder for the product ID
    folder_path = f"./{product_id}"
    os.makedirs(folder_path, exist_ok=True)

    # Get product name
    name_element = driver.find_element(By.XPATH, '//*[@id="product-detail-app"]/div/div[2]/div[1]/div[2]/div[2]/div[1]/div/div/div[1]/h1')
    product_name = name_element.text
    
    # Increment the folder counter
    folder_counter += 1
    
    # Get product price
    try:
        price_element = driver.find_element(By.XPATH, '//*[@id="product-detail-app"]/div/div[2]/div[1]/div[2]/div[2]/div[1]/div/div/div[4]/div/div/span')
        price = price_element.text
        # Process the price value here
    except NoSuchElementException:
        price = "Price not available"
    time.sleep(2)
    try:
        discount_element = driver.find_element(By.XPATH, '//*[@id="product-detail-app"]/div/div[2]/div[1]/div[2]/div[2]/div[1]/div/div/div[4]/div/div/div/div[2]/span[2]')
        discount = discount_element.text
        # Process the discount value here
    except NoSuchElementException:
        discount = "Discount not available"
        # Handle the case when discount is not found

    time.sleep(2)
    # Get product details
    details_element = driver.find_element(By.XPATH, '//section[1]/div[1]/div[1]/div[1]/ul[1]')
    product_details = details_element.text

    # Save product details to a text file
    txt_file_path = f"{folder_path}/{product_id}.txt"
    with open(txt_file_path, 'w', encoding='utf-8') as f:
        f.write(f"Name: {product_name}\n")
        f.write(f"Price: {price}\n")
        f.write(f"if discount: {discount}\n")
        f.write(f"Link: {link}\n")
        f.write(f"Details:\n{product_details}\n")
    time.sleep(2)
    # Get product photos
    try:
        # Find the parent div element
        parent_div = driver.find_element(By.CLASS_NAME, 'styles-module_slider__o0fqa')

        # Find all the child div elements
        child_divs = parent_div.find_elements(By.TAG_NAME, 'div')

        # Click each child div
        for index, div in enumerate(child_divs):
            div.click()
            time.sleep(0.25)
            try:
                # Find the photo element
                photo_element = driver.find_element(By.XPATH, '//*[@id="product-detail-app"]/div/div/div/div/div/div/div/div/img[1]')
                photo_url = photo_element.get_attribute("src")

                # Set the file path to save the photo with an incremented name
                photo_file_path = f"{folder_path}/{product_id}_photo{index+1}.jpg"

                # Download the photo
                response = requests.get(photo_url)
                with open(photo_file_path, 'wb') as f:
                    f.write(response.content)

                print("Photo downloaded successfully.")
            except NoSuchElementException:
                print("Photo element not found.")
            # Add your desired actions after clicking each div

        print("Divs clicked successfully.")
    except NoSuchElementException:
        print("Parent div element not found.")
    time.sleep(2)
driver.quit()

