from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import csv
import time
import re
import concurrent.futures
from concurrent.futures.thread import ThreadPoolExecutor

url = "https://www.ebay.com/b/Computer-Components-Parts/175673/bn_1643095?rt=nc&_pgn=1"
Path = r"C:\Program Files\chromedriver.exe"
driver = webdriver.Chrome(Path)


url_list = [
    'https://www.ebay.com/b/Computer-Components-Parts/175673/bn_1643095?rt=nc&_pgn=1',
    'https://www.ebay.com/b/Computer-Components-Parts/175673/bn_1643095?rt=nc&_pgn=2',
    'https://www.ebay.com/b/Computer-Components-Parts/175673/bn_1643095?rt=nc&_pgn=3',
    'https://www.ebay.com/b/Computer-Components-Parts/175673/bn_1643095?rt=nc&_pgn=4',
    'https://www.ebay.com/b/Computer-Components-Parts/175673/bn_1643095?rt=nc&_pgn=5',
]

def write_csv(data):
    with open('result.csv', 'a') as f:
        fields = ['img_link', 'title', 'price', 'shipping_price']
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writerow(data)

def Get_Data(link):
    driver.get(link)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    
    img_link = []
    title = []
    price = []
    shipping_price = []

    item_list = soup.findAll("li", {"class": "s-item"})

    for item in item_list:
        result = soup.find("a", {"class": "s-item__link"})['href']
        img_link.append(result)

        result = item.find('h3').text
        title.append(result)

        result = soup.find("span", {"class": "ITALIC"}).text
        price.append(result)

        result = soup.find("span", {"class": "s-item__shipping"}).text.replace('shipping', '')
        shipping_price.append(result)

    data = {
            'img_link': img_link,
            'title': title,
            'price': price,
            'shipping_price': shipping_price
        }
    write_csv(data)



with concurrent.futures.ThreadPoolExecutor() as executor:
    results = [executor.submit(Get_Data, url) for url in url_list]

    for f in concurrent.futures.as_completed(results):
        print(f.result())