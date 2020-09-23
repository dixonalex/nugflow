import inject
from pathlib import Path
from retrying import retry
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from nugflow.interfaces.db import Db


def init() -> webdriver.Chrome:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get(
        "https://www2.illinois.gov/ilcc/resources/Pages/Liquor-License-Lookup.aspx"
    )
    assert "Liquor License" in driver.title
    return driver


@retry(
    stop_max_attempt_number=7,
    wait_exponential_multiplier=1000,
    wait_exponential_max=10000,
)
def nav_to_detail_page(driver: webdriver.Chrome, link_id: str) -> None:
    link = driver.find_element_by_id(link_id)
    print(f"Navigating to detail page for {link.text}.")
    link.click()
    WebDriverWait(driver, 60).until(EC.staleness_of(link))
    print("Waiting for labels to show ...")
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "label.form-control"))
    )


@retry(
    stop_max_attempt_number=7,
    wait_exponential_multiplier=1000,
    wait_exponential_max=10000,
)
def nav_to_next_page(driver: webdriver.Chrome) -> bool:
    try:
        nav = driver.find_element_by_css_selector("a#PageLinkNext")
    except NoSuchElementException:
        print("Reached the end of the line- exiting!")
        return False
    nav.click()
    print("Waiting 60s for staleness of", nav)
    WebDriverWait(driver, 60).until(EC.staleness_of(nav))
    return True


@retry(
    stop_max_attempt_number=7,
    wait_exponential_multiplier=1000,
    wait_exponential_max=10000,
)
def nav_to_summary_page(driver: webdriver.Chrome) -> None:
    driver.back()
    print("Waiting for summary page to load ...")
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.ms-srch-item-body"))
    )


def scrape_page(driver: webdriver.Chrome) -> dict:
    """Parse detail page and return data as a dictionary"""
    labels = driver.find_elements_by_css_selector("label")
    data = [l.text for l in labels]
    # convert ordered list to dictionary
    it = iter(data)
    record = dict(zip(it, it))
    return record


@inject.autoparams()
def already_processed(db: Db, license_number: str) -> bool:
    print("Checking if already processed", license_number)
    return db.get_record_exists(
        "liquor_license_illinois_sat", {"license_number": license_number}
    )


def extract(dst_path: Path) -> None:
    driver = init()
    try:
        out_file = dst_path.joinpath(f"data.csv")
        page = 0
        while True:
            page += 1
            records = list()
            print(f"Processing page {page}.")
            data_divs = driver.find_elements_by_css_selector("div.ms-srch-item-body")
            for i in range(0, len(data_divs)):
                data_div = driver.find_elements_by_css_selector(
                    "div.ms-srch-item-body"
                )[i]
                license_number = (
                    data_div.find_element_by_css_selector("span.soi-license-number")
                    .text.replace("License No: ", "")
                    .strip()
                )
                if already_processed(license_number=license_number):
                    print("Already processed", license_number, "; skipping...")
                    continue
                link_id = data_div.find_element_by_css_selector(
                    "a.ms-srch-item-link"
                ).get_attribute("id")
                print("Link id", link_id)
                nav_to_detail_page(driver, link_id)
                record = scrape_page(driver)
                nav_to_summary_page(driver)
                records.append(record)
            with open(out_file, "a") as f:
                df = pd.DataFrame(records)
                df.to_csv(f, header=page == 1, index=None)
            if not nav_to_next_page(driver):
                return
    except Exception:
        print("Encountered error processing")
        raise
    finally:
        driver.close()


if __name__ == "__main__":
    extract(Path("/home/alexanderldixon/downloads/"))
