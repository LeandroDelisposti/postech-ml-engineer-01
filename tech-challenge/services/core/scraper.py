import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_books():
    """
    This script will scrape the book data from https://books.toscrape.com/
    and save it to a CSV file in the data/ directory.
    """
    print("Scraping books...")
    
    base_url = "http://books.toscrape.com/"
    url = base_url
    
    all_books = []

    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        books = soup.find_all('article', class_='product_pod')
        
        for book in books:
            title = book.h3.a['title']
            price = book.find('p', class_='price_color').text
            rating = book.p['class'][1]
            availability = book.find('p', class_='instock availability').text.strip()
            image = book.div.a.img['src']
            
            all_books.append({
                'title': title,
                'price': price,
                'rating': rating,
                'availability': availability,
                'image': image
            })
            
        next_page = soup.find('li', class_='next')
        if next_page:
            url = base_url + "catalogue/" + next_page.a['href']
        else:
            break
            
    df = pd.DataFrame(all_books)
    df.to_csv('data/books.csv', index=False)
    
    print("Scraping complete.")
