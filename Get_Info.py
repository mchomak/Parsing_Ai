import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


def get_info_from_card(url):
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Get link
    try:
        link_element = soup.find('h1', class_='hp-listing__title').find('a')
        link = link_element['href']

    except (AttributeError, TypeError) as ex:
        # print(f"[ERROR] {ex}, \n Url {url}")
        link = None

    # Get description
    try:
        description_element = soup.find('div', class_='hp-listing__description')
        description = description_element.get_text(strip=True)

    except (AttributeError, TypeError) as ex:
        # print(f"[ERROR] {ex}, \n Url {url}")
        description = None

    # Get tags
    try:
        tags_elements = soup.find('div', class_='hp-listing__categories').find_all('a')
        tags = [tag.get_text(strip=True) for tag in tags_elements]
        tags=', '.join(tags)

    except (AttributeError, TypeError) as ex:
        # print(f"[ERROR] {ex}, \n Url {url}")
        tags = None
    
    # Get pricing type
    try:
        pricing_type_element = soup.find('div', class_='hp-listing__attribute hp-listing__attribute--pricing-type')
        pricing_type = pricing_type_element.get_text(strip=True).replace("Pricing Type: ", "")

    except (AttributeError, TypeError) as ex:
        # print(f"[ERROR] {ex}, \n Url {url}")
        pricing_type = None
    
    # Get price
    try:
        price_elements = soup.find('div', class_='hp-listing__attribute hp-listing__attribute--price')
        price = price_elements.get_text(strip=True).replace("Price: ", "")

    except (AttributeError, TypeError) as ex:
        # print(f"[ERROR] {ex}, \n Url {url}")
        price = None
    
    # Get platform
    try:
        platform_elements = soup.find('div', class_='hp-listing__attribute hp-listing__attribute--platform')
        platform = platform_elements.get_text(strip=True).replace("Platform(s): ", "")
        # platform = re.split(",", platform)

    except (AttributeError, TypeError) as ex:
        # print(f"[ERROR] {ex}, \n Url {url}")
        platform = None
    
    return link, description, tags, pricing_type, price, platform


def save_data(names, urls, links, descriptions, tagss, pricing_types, prices, platforms):
    print(f"names count is {len(names)}")
    print(f"urls count is {len(urls)}")
    print(f"links count is {len(links)}")
    print(f"descriptions count is {len(descriptions)}")
    print(f"tagss count is {len(tagss)}")
    print(f"pricing_types count is {len(pricing_types)}")
    print(f"prices count is {len(prices)}")
    print(f"platforms count is {len(platforms)}")

    df2=pd.DataFrame({"name":names, 
                      "product_link": links,
                      "card_link":urls,
                      "tags": tagss,
                      "descriptions": descriptions, 
                      "pricing_types": pricing_types, 
                      "price":prices, 
                      "platforms":platforms,
                      }, 
                    #   index=[0]
                      )
    df2.to_csv('my_data3.csv', index = False)


def main():
    links, descriptions, tagss, pricing_types, prices, platforms = [], [], [], [], [], []
    df = pd.read_csv("my_data2.csv")
    urls=df["card_link"]
    names=df["name"]

    print(f"[INFO] Start loop")
    for url in urls:
        
        link, description, tags, pricing_type, price, platform = get_info_from_card(url = url)

        links.append(link)
        descriptions.append(description)
        tagss.append(tags)
        pricing_types.append(pricing_type)
        prices.append(price)
        platforms.append(platform)

    
    save_data(names, urls, links, descriptions, tagss, pricing_types, prices, platforms)
    print(f"[INFO] DataBase sucsefully saved")

if __name__=="__main__":
    main()