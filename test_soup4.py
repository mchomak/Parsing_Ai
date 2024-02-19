import requests
from bs4 import BeautifulSoup
import csv

url = "https://aiscout.net/listing/sanebox/#content"  

# Make a request to the website and get the HTML content
response = requests.get(url)
html_content = response.content

# Parse HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Extract link
try:
    link_element = soup.find('h1', class_='hp-listing__title').find('a')
    link = link_element['href']
except (AttributeError, TypeError):
    link = "Link not found"

# Extract description
try:
    description_element = soup.find('div', class_='hp-listing__description')
    description = description_element.get_text(strip=True)
except (AttributeError, TypeError):
    description = "Description not found"

# Extract tags
try:
    tags_elements = soup.find('div', class_='hp-listing__categories').find_all('a')
    tags = [tag.get_text(strip=True) for tag in tags_elements]
except (AttributeError, TypeError):
    tags = []

# Display the extracted data
print(f"Link: {link}")
print(f"Description: {description}")
print(f"Tags: {', '.join(tags)}")
