import json
import os
import time
from urllib.parse import urljoin, urlparse

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to set up WebDriver
def setup_webdriver(driver_path, headless):
    options = Options()
    options.use_chromium = True
    if headless:
        options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    service = Service(driver_path)
    driver = webdriver.Edge(service=service, options=options)
    return driver

# Function to scrape data from a single page based on selectors
def scrape_page(driver, url, selectors):
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    
    page_data = {"source_link": url}

    for section, selector in selectors.items():
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            page_data[section] = [elem.text.strip() for elem in elements]
        except:
            page_data[section] = []

    return page_data

# Function to collect all internal links
def get_all_links(driver, base_url):
    links = set()
    elements = driver.find_elements(By.CSS_SELECTOR, 'a')
    for elem in elements:
        href = elem.get_attribute('href')
        if href and urlparse(href).netloc == urlparse(base_url).netloc:
            full_url = urljoin(base_url, href)
            links.add(full_url)
    return links

# Function to perform scraping with fallback selectors
def scrape_with_fallbacks(driver, url):
    selectors = {
        "about_me": "p",
        "education": "ul",
        "work_experience": "div",
        "skills": "ul"
    }

    return scrape_page(driver, url, selectors)

# Function to clean scraped data
def clean_data(website_data):
    cleaned_data = {}
    for link, data in website_data.items():
        cleaned_data[link] = {"source_link": data["source_link"]}
        for section, texts in data.items():
            if section != "source_link":
                cleaned_texts = []
                seen_texts = set()
                for text in texts:
                    clean_text = text.strip().replace('\n', ' ').replace('\r', '').replace(u'\xa0', ' ')
                    # Add any other cleaning steps here, like removing special characters, etc.
                    if clean_text and clean_text not in seen_texts:
                        cleaned_texts.append(clean_text)
                        seen_texts.add(clean_text)
                cleaned_data[link][section] = cleaned_texts
    return cleaned_data

# Main function to perform the scraping
def main(output_file, base_url, driver_path, headless, delay):
    driver = setup_webdriver(driver_path, headless)

    try:
        driver.get(base_url)
        all_links = get_all_links(driver, base_url)
        website_data = {}

        for link in all_links:
            print(f"Scraping {link}")
            page_data = scrape_with_fallbacks(driver, link)
            website_data[link] = page_data
            time.sleep(delay)

        # Clean the scraped data
        cleaned_data = clean_data(website_data)

        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(cleaned_data, file, ensure_ascii=False, indent=4)

        print(f"Data successfully scraped, cleaned, and saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()

# Script execution starts here
if __name__ == "__main__":
    # Path to save the output JSON file
    output_file = "output.json"
    # Base URL to start scraping
    base_url = "Your url"
    # Path to driver executable
    driver_path = "Path toyour driver.exe"
    # Headless mode
    headless = True
    # Delay between requests in seconds
    delay = 2.0

    main(output_file, base_url, driver_path, headless, delay)
