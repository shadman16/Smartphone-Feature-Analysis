import requests
from bs4 import BeautifulSoup
import pandas as pd

records = []
# loop through sort type
# sort_types = ['price_desc', 'price_asc', 'recency_desc', 'popularity', 'relevance']

# read list of brands scrapped manually from website
brands_div = open('brands.txt').readlines()[0]
brands_div = BeautifulSoup(brands_div, "html.parser")
brands_div = brands_div.find_all("div")
# find all brands
brands = ['Apple']
for brand in brands_div:
    if len(brand.text) > 1 and brand.text not in brands:
        brands.append(brand.text)

# for sort_type in sort_types:
for n_brand, brand in enumerate(brands):
    formatted_brand = brand.replace(' ', '%2B')
    # loop through pages
    for i in range(1, 50):
        # Bse url
        # url = "https://www.flipkart.com/search?q=mobiles&sort={}&page={}".format(sort_type, i)
        url = "https://www.flipkart.com/search?q=mobiles&p%5B%5D=facets.brand%255B%255D%3D{}&sort=price_desc&page={}".\
            format(formatted_brand, i)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        # get response
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        mobile_items = soup.find_all("div", {"class": "_1AtVbE col-12-12"})
        # exit current loop if no phones
        if len(mobile_items) < 5:
            break
        print(n_brand, brand, f'page {i}')
        # get phones data
        for item in mobile_items:
            # Extract the name of the mobile phone
            try:
                name = item.find('div', {'class': '_4rR01T'}).text
                name = name.lower().replace(brand.lower(), '')
                name = name.strip()
            except AttributeError:
                continue

            # Extract the rating of the mobile phone, if available
            rating = item.find('div', {'class': '_3LWZlK'}).text if item.find('div', {'class': '_3LWZlK'}) else 'N/A'
            num_ratings_reviews = item.find('span', {'class': '_2_R_DZ'}).text if item.find('span', {'class': '_2_R_DZ'}) else 'N/A'

            # Extract the price of the mobile phone
            price = item.find('div', {'class': '_30jeq3 _1_WHN1'}).text if item.find('div', {'class': '_30jeq3'}) else 'N/A'

            ram_rom = 'N/A'
            battery = 'N/A'
            display = 'N/A'
            processor = 'N/A'
            camera = 'N/A'
            # Extract the features of the mobile phone
            features = item.find_all('li', {'class': 'rgWa7D'})
            features_list = [feature.text.lower() for feature in features]
            for feature in features_list:
                if ' ram' in feature or ' rom' in feature or 'expandable' in feature:
                    ram_rom = feature
                elif ' mah' in feature:
                    battery = feature
                elif 'display' in feature:
                    display = feature
                elif 'processor' in feature:
                    processor = feature
                elif 'camera' in feature and 'mp' in feature:
                    camera = feature
            final_list = [brand, name, rating, num_ratings_reviews, price,
                          ram_rom, battery, display, processor, camera]
            records.append(final_list)

df = pd.DataFrame(records, columns=['brand', 'name', 'rating', 'num_rating_reviews', 'price',
                                    'ram_rom', 'battery', 'display', 'processor', 'camera'])
df.to_excel("flipkart_mobiles.xlsx", index=False, sheet_name='data')
