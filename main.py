import csv
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


def scrape_products(url,slug, id):
    id = id 
    slug = slug
    url = url
    product_list = []
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    next_page = 1

    while 1:
        time.sleep(2)

        next_page = next_page + 1

        try:
            
            button_xpath = f"//button[contains(text(), '{next_page}') and contains(@class, 'MuiPaginationItem-rounded')]"
            button = driver.find_element(By.XPATH, button_xpath)


            # # Get products
            time.sleep(3)
            # Get the updated content
            updated_content = driver.page_source
            # Parse the updated content using Beautiful Soup
            soup = BeautifulSoup(updated_content, 'html.parser')
            all_product_container = soup.find_all('div', class_="product-one")
            for single_product_container in all_product_container:
                a_element = single_product_container.find('a')
                product_link = a_element['href']

                product_one__single = a_element.find('div', class_="product-one__single")
                product_one__single__inner = product_one__single.find('div', class_="product-one__single__inner")

                # img title price offer

                img_div = product_one__single__inner.find('div', class_="product-one__single__inner__img")
                content_div = product_one__single__inner.find('div', class_="product-one__single__inner__content")

                offer_div = product_one__single__inner.find('div', class_="product-offer")

                if offer_div is not None:
                    offer = offer_div.find('p').text.strip()
                else:
                    offer = '-0%'   

                title_tag = content_div.find('p')

                if title_tag is not None:
                    title = content_div.find('p').text.strip()
                else:
                    title = ""
                
                price_tag = content_div.find('span')
                
                if price_tag is not None:
                    price = content_div.find('span').text.strip()
                else:
                    price = ""
                
                id = id + 1
                product = {
                    'position': id,
                    'title': title,
                    'slug': slug,
                    'price': price.replace("\u09f3", ""),
                    'offer': offer,
                    'product_link': "https://www.pickaboo.com"+product_link,
                }

                product_list.append(product)
                


            if driver.find_element(By.XPATH, button_xpath) is not None:
                if button.is_displayed() and button.is_enabled():
                    driver.execute_script("arguments[0].click();", button)
        
        except NoSuchElementException:
            # Get the updated content
            updated_content = driver.page_source
            # Parse the updated content using Beautiful Soup
            soup = BeautifulSoup(updated_content, 'html.parser')
            all_product_container = soup.find_all('div', class_="product-one")
            for single_product_container in all_product_container:
                a_element = single_product_container.find('a')
                product_link = a_element['href']

                product_one__single = a_element.find('div', class_="product-one__single")
                product_one__single__inner = product_one__single.find('div', class_="product-one__single__inner")

                # img title price offer

                img_div = product_one__single__inner.find('div', class_="product-one__single__inner__img")
                content_div = product_one__single__inner.find('div', class_="product-one__single__inner__content")

                offer_div = product_one__single__inner.find('div', class_="product-offer")

                if offer_div is not None:
                    offer = offer_div.find('p').text.strip()
                else:
                    offer = '-0%'   

                title_tag = content_div.find('p')

                if title_tag is not None:
                    title = content_div.find('p').text.strip()
                else:
                    title = ""
                
                price_tag = content_div.find('span')
                
                if price_tag is not None:
                    price = content_div.find('span').text.strip()
                else:
                    price = ""
                
                id = id + 1
                product = {
                    'position': id,
                    'title': title,
                    'slug': slug,
                    'price': price.replace("\u09f3", ""),
                    'offer': offer,
                    'product_link': "https://www.pickaboo.com"+product_link,
                }

                product_list.append(product)
            break

    driver.quit()
    return product_list, id


category_base_url = "https://www.pickaboo.com/product/"
slug_array = []
with open('./assets/csv/category_list.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        slug_array.append(row['slug'])
for slug in slug_array:
    url = category_base_url+slug
    product_list, id = scrape_products(url, slug, id = 0)
    print(product_list)

    my_list_of_dicts = product_list
      
    # open a new CSV file for writing
    with open('./output/'+str(id)+'_products-'+slug+'.csv', 'w', newline='') as csvfile:
        fieldnames = ['position', 'title', 'slug', 'price', 'offer', 'product_link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # write the header row to the CSV file
        writer.writeheader()

        # write each dictionary in the list as a new row in the CSV file
        for item in my_list_of_dicts:
                writer.writerow(item)
    
