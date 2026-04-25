import requests
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate
import datetime

def scrape_books(limit):
    # Send a GET request to the website
    url = 'https://books.toscrape.com/'
    response = requests.get(url)
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all book articles
    books = soup.find_all('article', class_='product_pod')
    
    # Extract title and price for the first 'limit' books
    book_list = []
    for i in range(min(limit, len(books))):
        book = books[i]
        
        # Extract title
        title = book.h3.a['title']
        
        # Extract price
        price = book.find('p', class_='price_color').text
        
        book_list.append({'title': title, 'price': price})
    
    return book_list

def fetch_exchange_rate():
    response = requests.get('https://api.exchangerate-api.com/v4/latest/GBP')
    data = response.json()
    return data['rates']['KES']

def scrape_products():
    global books
    books = scrape_books(10)
    print("Products scraped.")

def convert_currency():
    global books, rate, df
    if not books:
        print("Please scrape products first.")
        return
    rate = fetch_exchange_rate()
    timestamp = datetime.datetime.now().isoformat()
    data_list = []
    for book in books:
        gbp_price_str = book['price']
        gbp_price = float(gbp_price_str.replace('£', ''))
        kes_price = gbp_price * rate
        data_list.append({
            'Title': book['title'],
            'Price_GBP': gbp_price_str,
            'Price_KES': f"{kes_price:.2f}",
            'Timestamp': timestamp
        })
    df = pd.DataFrame(data_list)
    print("Currency converted.")

def view_products():
    global df
    if df.empty:
        print("Please scrape and convert currency first.")
        return
    print(tabulate(df, headers='keys', tablefmt='grid'))

def save_to_csv():
    global df
    if df.empty:
        print("Please scrape and convert currency first.")
        return
    df.to_csv('products.csv', index=False)
    print("Data saved to products.csv")

def main():
    global books, rate, df
    books = []
    rate = None
    df = pd.DataFrame()
    while True:
        print("\nMenu:")
        print("1. Scrape products")
        print("2. Convert currency")
        print("3. View products")
        print("4. Save to CSV")
        print("5. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            scrape_products()
        elif choice == '2':
            convert_currency()
        elif choice == '3':
            view_products()
        elif choice == '4':
            save_to_csv()
        elif choice == '5':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()