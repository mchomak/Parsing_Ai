import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_cards_from_page(url, names, urls):
    try:
        response = requests.get(url)
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')

        cards = soup.find_all('div', class_='hp-listing__image')
        print(f"[INFO] Cards count is {len(cards)}")
        for card in cards:
            card_url=card.find("a")["href"]
            card_name=card.find('img')["alt"]
            names.append(card_name)
            urls.append(card_url)
        
        return names, urls
            
    except (AttributeError, TypeError) as ex:
        print(f"[ERROR] {ex}")
        return names, urls


def save_data(names, urls):
    df2=pd.DataFrame({"name":names,
                      "card_link":urls
                      })
    df = pd.read_csv("my_data.csv")
    df = pd.concat([df, df2], ignore_index = True )
    df.to_csv('my_data2.csv', index= False )


def main():
    general_url = "https://aiscout.net/browse-ai-tools/page/"  
    pages_count = 36
    names, urls = [], []
    for page in range(1, pages_count + 1):
        print(f"[INFO] Now {page} page")
        url=f"{general_url}{page}/"
        names, urls = get_cards_from_page(url = url, names = names, urls = urls)
    
    save_data(names, urls)
    print(f"[INFO] DataBase sucsefully saved")


if __name__=="__main__":
    main()