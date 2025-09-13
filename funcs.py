import time
import consts
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd

# output data
data = {
    'item_name': [],
    'category': [],
    'price': []
}


def load_site(driver, link):
    driver.get(link)

    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                ('xpath', '//ul[contains(@class, "secondary-menu")]//li'))
        )
    except TimeoutException as e:
        driver.quit()
        raise e


def save_data(name, price, category):
    data['item_name'].append(name)
    data['category'].append(category)
    data['price'].append(price)


def fetch_categories(driver, indices: list[int]):
    """
    Fetch products in each category.
    """
    for i in indices:
        cats = driver.find_elements(
            # categories like beef, chicken, sides
            by='xpath', value='//ul[contains(@class, "secondary-menu")]//li')
        cats[i].click()
        time.sleep(1)  # to be changed
        prods = driver.find_elements(
            by='xpath', value='//div[contains(@class, "panel-default")]')
        fetch_products(driver, prods)


def fetch_products(driver, products: list):
    """
    Extract information about each product.\n
    category - The name of the parent category.\n
    name - The name of the product.\n
    price - The price of the product in EGP.
    """
    for product in products:
        cat_name = driver.find_element(
            'xpath', '//li[contains(@class, "secondary-menu-item selected")]//span').text
        name = product.find_element('xpath', './/h5').text
        price = product.find_element(
            'xpath', './/div[contains(@class, "product-cost")]').text
        save_data(name, price, cat_name)


def export_data(data):
    modified = pd.DataFrame(data)
    modified.to_csv(f'data/macdonalds_menu.csv')


def run_app(driver, link):
    """
    <b>Scraping Hierarchy:</b>\n
    1. Load the site and ensure elements are loaded successfully.\n
    2. Fetch each category by order in the indices specified.\n
    3. Fetch each product in the category and extract information [name, category, price].\n
    4. Update the data with each product.\n
    5. Export the data in a CSV file.
    6. Turn off the driver (scraper)
    """
    load_site(driver, link)
    fetch_categories(driver, consts.CAT_INDICES)  # main function
    export_data(data)
    driver.quit()
