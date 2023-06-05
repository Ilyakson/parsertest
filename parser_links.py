import json
import time

from selenium import webdriver
from selenium.webdriver import Proxy
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import ProxyType


def parse_links():
    service = Service()
    # proxy = Proxy()
    # proxy.proxy_type = ProxyType.MANUAL
    # proxy.http_proxy = "your_proxy"

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--proxy-server=https://{}".format(proxy.http_proxy))

    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://www.jumia.dz/tvs/")
    closer = driver.find_element(By.XPATH, '//*[@id="pop"]/div/section/button')
    closer.click()
    link_list = []
    while True:
        elements = driver.find_elements(By.CLASS_NAME, 'prd._fb.col.c-prd')
        for element in elements:
            elem = element.find_element(By.CLASS_NAME, 'core')
            link = elem.get_attribute("href")
            link_list.append(link)
        try:
            button = driver.find_element(By.XPATH, '//a[@aria-label="Page suivante"]')
            help_element = driver.find_element(By.XPATH, '//*[@id="jm"]/main/div[2]/div[3]/section/div[1]/article[39]')
            driver.execute_script("arguments[0].scrollIntoView();", help_element)
            time.sleep(3)
        except:
            break
        button.click()
    time.sleep(3)
    with open('links.json', 'w') as f:
        json.dump(link_list, f)


parse_links()
