import csv
import requests
from bs4 import BeautifulSoup
import time



url = "https://www.pickaboo.com/product-detail/oneplus-nord-n20-se-4gb-64gb/"



# Send an HTTP request to the web page and get the HTML content
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

time.sleep(2)
title_element = soup.find('h1')
if title_element is not None:
    title = title_element.text.strip()
    print(title)
else:
    print('h1 element with class "title" not found.')

# price

div_element = soup.find('div', {'class': 'price-view'})

if div_element is not None:
    h2_element = div_element.find(lambda tag: tag.name == 'h2')
    discount_element = div_element.find(lambda tag: tag.name == 'div')
    discount = discount_element.find(lambda tag: tag.name == 'span')
    if h2_element is not None:
        price = h2_element.text.strip()
        print(price)
    else:
        print('No h2 element found inside div element with class "some-class"')
    if discount_element is not None:
        discount_info = discount.text.strip()
        print(discount_info)
    else:
        print('No discount found!')
else:
    print('Div element with class "some-class" not found.')



product_details = {
        'name': str(title),
        'price': price.replace("\u09f3", ""),
        'discount': str(discount_info)
}



# Open the CSV file in append mode
with open('product_list.csv', 'a', newline='') as csvfile:

    # Define the fieldnames for the CSV file
    fieldnames = ['name', 'price', 'discount']

    # Create a DictWriter object and write the header row if the file is empty
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    if csvfile.tell() == 0:
        writer.writeheader()

    # Write the product_details dictionary to the CSV file
    writer.writerow(product_details)


# discounted_price = price - (price * discount)