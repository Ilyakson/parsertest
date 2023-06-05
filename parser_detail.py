import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

with open('links.json', 'r') as f:
    data = json.load(f)

output = []


def parse_data(link):
    service = Service()
    # proxy = Proxy()
    # proxy.proxy_type = ProxyType.MANUAL
    # proxy.http_proxy = "your_proxy"

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--proxy-server=https://{}".format(proxy.http_proxy))

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(link)

    closer = driver.find_element(By.XPATH, '//*[@id="pop"]/div/section/button')
    closer.click()

    title = driver.find_element(By.XPATH, "/html/head/meta[4]").get_property("content")

    brand = driver.find_element(
        By.XPATH, '//div[contains(text(), "Marque:") and contains(@class, "-pvxs")]'
    ).text.split()

    price = driver.find_element(By.CLASS_NAME,
                                '-b.-ltr.-tal.-fs24'
                                ).text.strip()

    reviews = driver.find_element(By.CLASS_NAME,
                                  '-plxs._more'
                                  ).text.strip()

    sellers = driver.find_element(By.CSS_SELECTOR,
                                  'p.-m.-pbs:not(.additional-class)'
                                  ).text.strip()

    elements = driver.find_elements(By.CLASS_NAME, 'hdr.-upp.-fs14.-m.-pam')

    weight = ""
    for element in elements:
        if element.text == "DESCRIPTIF TECHNIQUE":
            weight = element.find_element(By.XPATH,
                                          '//ul/li[contains(span, "Poids (kg)")]'
                                          ).text

    stock_status = driver.find_element(By.CLASS_NAME, '-df.-i-ctr.-fs12.-pbs').text.strip()

    try:
        driver.find_element(By.CLASS_NAME, "bdg._mall._sm.-mts")
        store = "official"
    except:
        store = "not official"
    result = {
        "title": title,
        "brand": brand[1],
        "store": store,
        "price": price,
        "reviews": reviews,
        "sellers": sellers,
        "weight": weight,
        "stock_status": stock_status,
        "link": link
    }

    output.append(result)

    driver.quit()


for item in data:
    parse_data(item)

with open('detail.json', 'w') as f:
    json.dump(output, f)
