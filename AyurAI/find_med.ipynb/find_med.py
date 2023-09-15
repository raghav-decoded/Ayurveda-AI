import requests
from bs4 import BeautifulSoup

def scrape_ayurkart(search_query):
    ayurkart_url = f"https://www.ayurkart.com/search?q={search_query}"
    print(ayurkart_url)

    # Send an HTTP GET request to the URL
    response = requests.get(ayurkart_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract data using class selectors
        price_elements = soup.find_all('span', class_='product-price__price')
        title_elements = soup.find_all('a', class_='list-view-item__title')
        link_elements = soup.find_all('a', class_='list-view-item__title')   

        # Process and print the data
        for price_element, title_element, link_element in zip(price_elements, title_elements, link_elements):
            price = price_element.get_text()
            title = title_element.get_text()
            link = 'https://www.ayurkart.com' + link_element['href'] if link_element else "Link not found"

            print("Title:", title)
            print("Price:", price)
            print("Link:", link)
    else:
        print("Failed to retrieve the web page.")

if __name__ == "__main__":
    search_query = "vyaghradi kashaya"
    scrape_ayurkart(search_query)
