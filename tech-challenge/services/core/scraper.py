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

    initial_response = requests.get(base_url)
    initial_soup = BeautifulSoup(initial_response.content, 'html.parser')

    # Find the category list
    category_list_ul = initial_soup.find('div', class_='side_categories').find('ul').find('li').find('ul')
    category_links = category_list_ul.find_all('li')

    for link in category_links:
        category_name = link.a.text.strip()
        # The category links are relative, so prepend base_url
        category_relative_path = link.a['href']
    
        # Base URL for categories is usually http://books.toscrape.com/catalogue/
        # But the links themselves already include catalogue/ inside their href
        # So it's effectively base_url + category_relative_path
        # Example: http://books.toscrape.com/catalogue/category/books/travel_2/index.html
        
        # The base_url already points to the root.
        # The category_relative_path already contains the catalogue segment.
        # Ensure we don't duplicate 'catalogue' or 'index.html' if it's not the first page.
        
        # Correctly construct the category URL. The `href` attributes for categories
        # are like `catalogue/category/books/travel_2/index.html`.
        # So we just append this to the main base_url.
        full_category_url = base_url + category_relative_path
        print("full_category_url: ", full_category_url)
        
        all_books.extend(scrape_category_books(full_category_url, category_name))

    df = pd.DataFrame(all_books)
    df.to_csv('data/books.csv', index=False)
    
    print("Scraping complete.")

def scrape_category_books(category_url, category_name):
    """
    Scrapes all books from a given category URL, iterating through all pages.
    """
    category_books = []
    current_url = category_url
    page_num = 1
    while True:
        print(f"Scraping category '{category_name}', page {page_num}: {current_url}")
        response = requests.get(current_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        books = soup.find_all('article', class_='product_pod')

        for book in books:
            title = book.h3.a['title']
            price = book.find('p', class_='price_color').text
            rating = book.p['class'][1]
            availability = book.find('p', class_='instock availability').text.strip()
            image = book.div.a.img['src']

            category_books.append({
                'title': title,
                'category': category_name,
                'price': price,
                'rating': rating,
                'availability': availability,
                'image': image
            })

        next_page = soup.find('li', class_='next')
        if next_page:
            # Construct the next page URL relative to the category base
            if "index.html" in current_url: # First page of a category often ends with index.html
                current_url = current_url.replace("index.html", next_page.a['href'])
            else: # Subsequent pages are relative to the current category path
                current_url = "/".join(current_url.split('/')[:-1]) + "/" + next_page.a['href']
            page_num += 1
        else:
            break
    return category_books