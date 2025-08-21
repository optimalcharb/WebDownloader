from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import pandas as pd
import os
import logging

# Configure logging
logging.basicConfig(
    filename="webscrape.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Read site list from Excel
sites_df = pd.read_excel("sites.xlsx")

# Initialize the WebDriver
driver = webdriver.Chrome()

total_download_count = 0
site_count = 0

# Iterate over the rows of the DataFrame
for _, row in sites_df.iterrows():
    site_name = row["Site Name"]
    url = row["URL"]
    logging.info(f"Processing {site_name}...")

    try:
        # Open site
        driver.get(url)

        # Find PDF links
        driver.implicitly_wait(5)
        pdf_links = driver.find_elements(By.XPATH, "//a[contains(@href, '.pdf')]")
        pdf_urls = [link.get_attribute("href") for link in pdf_links]

        # Create output directory
        if not os.path.exists(site_name):
            os.makedirs(site_name)

        # Download each PDF
        download_count = 0
        for pdf_url in pdf_urls:
            try:
                response = requests.get(pdf_url, stream=True)
                if response.status_code == 200:
                    pdf_name = os.path.join(site_name, pdf_url.split("/")[-1])
                    with open(pdf_name, "wb") as pdf_file:
                        for chunk in response.iter_content(chunk_size=1024):
                            pdf_file.write(chunk)
                    download_count += 1
                else:
                    logging.warning(f"Failed to download {pdf_url}: Status code {response.status_code}")
            except Exception as e:
                logging.error(f"Error downloading {pdf_url}: {e}")
        
        site_count += 1
        total_download_count += download_count
        logging.info(f"Downloaded {download_count} PDFs for {site_name}")

    except Exception as e:
        logging.error(f"Error processing {site_name}: {e}")

logging.info(f"Downloaded {total_download_count} PDFs from {site_count} sites.")

driver.quit()
