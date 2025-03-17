import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
from time import sleep

# Lists to store the scraped data
Product_urls = []
Product_name = []
Original_price = []
Discount = []
Price_after_discount = []
Ratings = []  # Now scraping ratings from product page

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Referer": "https://www.google.com/",
    "Connection": "keep-alive",
}

# Step 1: Scrape main listing page and extract product URLs for each product
for i in range(20, 37):  # Loop through 5 pages
    url = "https://www.flipkart.com/search?q=mi+mobile&as=on&as-show=on&otracker=AS_Query_OrganicAutoSuggest_3_3_na_na_na&otracker1=AS_Query_OrganicAutoSuggest_3_3_na_na_na&as-pos=3&as-type=RECENT&suggestionId=mi+mobile&requestId=0be4a66d-4e52-44cc-9893-5686f254798b&as-searchtext=mi+mobile&page="+str(i)
    
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")

    # Find all product links on the current page
    product_list = soup.find_all("a", class_="CGtC98")  # Same class for product containers
    
    for item in product_list:
        link = item['href']  # Extract href attribute
        full_link = "https://www.flipkart.com" + link  # Create full product URL
        Product_urls.append(full_link)  # Append to the product URLs list

    print(f"Page {i}: Found {len(product_list)} products")

    sleep(random.uniform(1, 3))  # Delay to avoid detection

print(f"Total product URLs collected: {len(Product_urls)}")

# Step 2: Scrape product details from each product page
for product_url in Product_urls:
    product_response = requests.get(product_url, headers=headers)
    product_soup = BeautifulSoup(product_response.text, "lxml")

    # Extract specific details from the product page
    try:
        brand = product_soup.find_all("span", class_="VU-ZEz")[0].text.strip()  # Same class for brand name
        Product_name.append(brand)
    except:
        Product_name.append("N/A")

    try:
        price = product_soup.find_all("div", class_="Nx9bqj CxhGGd")[0].text.strip()  # Same class for price after discount
        Price_after_discount.append(price)
    except:
        Price_after_discount.append("N/A")
    
    try:
        original_price = product_soup.find_all("div", class_="yRaY8j A6+E6v")[0].text.strip()  # Same class for original price
        Original_price.append(original_price)
    except:
        Original_price.append("N/A")
    
    try:
        discount = product_soup.find_all("div", class_="UkUFwK")[0].text.strip()  # Same class for discount
        Discount.append(discount)
    except:
        Discount.append("N/A")

    try:
        rating = product_soup.find_all("div", class_="XQDdHH")[0].text.strip()  # Same class for ratings
        Ratings.append(rating)
    except:
        Ratings.append("No Rating")

    sleep(random.uniform(1, 3))  # Random delay to avoid detection

# Step 3: Create a DataFrame to store the scraped data
df = pd.DataFrame({
    "Product name": Product_name,
    "Original Price": Original_price,
    "Discount": Discount,
    "Price After Discount": Price_after_discount,
    "Ratings": Ratings
})

print(df)  # Print the data frame to ensure correct scraping

# Step 4: Save the data to a CSV file
df.to_csv("C:/Python Programs/Web_scraping/Mi_Mobiles3.csv", index=False)
