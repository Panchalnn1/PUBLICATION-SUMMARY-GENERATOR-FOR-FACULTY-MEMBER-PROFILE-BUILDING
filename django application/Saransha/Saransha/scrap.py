
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import requests # Changed 'Request' to 'requests'

headers_list = [
    # Chrome on Windows
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.123 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.112 Safari/537.36"},

    # Chrome on Mac
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.123 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.112 Safari/537.36"},

    # Chrome on Linux
    {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.123 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.112 Safari/537.36"},

    # Firefox on Windows
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:119.0) Gecko/20100101 Firefox/119.0"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:118.0) Gecko/20100101 Firefox/118.0"},

    # Firefox on Mac
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6_2; rv:119.0) Gecko/20100101 Firefox/119.0"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7; rv:118.0) Gecko/20100101 Firefox/118.0"},

    # Safari on Mac
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Safari/605.1.15"},

    # Edge on Windows
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.123 Safari/537.36 Edg/119.0.1108.69"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.112 Safari/537.36 Edg/118.0.2088.61"},

    # Opera on Windows
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.123 Safari/537.36 OPR/97.0.4719.56"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.112 Safari/537.36 OPR/96.0.4696.44"},

]


# Function to fetch the Google Scholar page
def fetch_scholar_data(url, max_retries=5):
    retry_count = 0

    while retry_count < max_retries:
        try:
            # Randomly select a user-agent
            headers = random.choice(headers_list)

            # Send the GET request
            response = requests.get(url, headers=headers)

            # Check the response status
            response.raise_for_status()  # Raise an error for bad status codes
            print(f"Request successful for {url}!")
            return response.text  # Return the page content

        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                print("429 Too Many Requests: Waiting before retrying...")
                time.sleep(10 + random.randint(1, 5))  # Wait 10-15 seconds
            else:
                print(f"HTTP error occurred: {e}")
                break

        except requests.exceptions.RequestException as e:
            print(f"Request exception occurred: {e}")
            break

        retry_count += 1
        print(f"Retrying... Attempt {retry_count}/{max_retries}")
        time.sleep(5)  # Wait 5 seconds before retrying

    print(f"Max retries reached for {url}. Could not fetch data.")
    return None
# Initialize the Selenium WebDriver
def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run Chrome in headless mode
    options.add_argument("--no-sandbox")  # Required in some environments
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource issues
    options.add_argument("--disable-gpu")  # Disable GPU usage
    options.add_argument("--window-size=1920,1080")  # Set window size

    # Setup WebDriver
    driver = webdriver.Chrome(options=options)
    return driver

# Load the page and handle the "Show More" button
def load_full_page(driver, url):
    driver.get(url)
    time.sleep(2)  # Allow page to load

    while True:
        try:
            # Wait and find the "Show More" button
            show_more_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "gsc_bpf_more"))
            )
            show_more_button.click()
            time.sleep(2)  # Allow content to load after the click
        except Exception:
            # Break the loop if no more "Show More" button is found
            print("No more 'Show More' button to click.")
            break

    # Return the full page source
    return driver.page_source


def link(html_content, base_url="https://scholar.google.com"):
    if html_content:
        full_link = base_url + html_content
        html_content = fetch_scholar_data(full_link)
        soup = BeautifulSoup(html_content, "html.parser")
        div_tag = soup.find("div", id="gsc_oci_title_gg")
        if div_tag:
            link_tag = div_tag.find("a", href=True)
            if link_tag:
                return link_tag["href"]
    return None

# Scrape the data
def scrape_table(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    profile_name = soup.find('div', {'id': 'gsc_prf_in'}).get_text(strip=True)
    domain_elements = soup.select("#gsc_prf_int .gsc_prf_inta")
    domains = [domain.text.strip() for domain in domain_elements]

    # Find the table containing publication data
    table = soup.find("table", {"id": "gsc_a_t"})
    if not table:
        print("Table not found!")
        return []

    # Extract table rows
    rows = table.find_all("tr", {"class": "gsc_a_tr"})
    data = []

    # Iterate over rows and extract columns
    for row in rows:
        title_cell = row.find("a", {"class": "gsc_a_at"})  # Title cell
        title = title_cell.text.strip() if title_cell else "N/A"
        relative_link = title_cell.get("href")
        pdf = link(relative_link)

        # Co-author and journal information
        gray_divs = row.find_all("div", {"class": "gs_gray"})
        co_authors = gray_divs[0].text.strip() if len(gray_divs) > 0 else "N/A"
        journal = gray_divs[1].text.strip() if len(gray_divs) > 1 else "N/A"

        # Year of publication
        year_cell = row.find("span", {"class": "gsc_a_h gsc_a_hc gs_ibl"})
        year = year_cell.text.strip() if year_cell else "N/A"

        # Citation count
        citation_cell = row.find("a", {"class": "gsc_a_ac gs_ibl"})
        citations = citation_cell.text.strip() if citation_cell else "0"

        # Append data to list
        data.append({
            "main_author": profile_name,
            "Title": title,
            "Co-Authors": co_authors,
            "Journal": journal,
            "Domains": domains,
            "Year": year,
            "Citations": citations,
            "Download": pdf,
        })

    return data


# Function to perform scraping and return DataFrame
def scrape_scholar_profiles(input_file_path):
    # Read the Excel sheet containing URLs
    df_urls = pd.read_excel(input_file_path)

    # Initialize WebDriver
    driver = init_driver()

    # Create an empty list to store all scraped data
    all_data = []

    # Iterate through each URL and scrape data
    for url in df_urls['Profile URL']:
        try:
            html_content = load_full_page(driver, url)
            if html_content:
                # Scrape the data from the page
                table_data = scrape_table(html_content)
                all_data.extend(table_data)
        except Exception as e:
            print(f"Error scraping {url}: {e}")

    # Close the WebDriver
    driver.quit()

    # Convert all scraped data to a DataFrame and return it
    if all_data:
        df = pd.DataFrame(all_data)
        return df
    else:
        print("No data was scraped.")
        return None