import pandas as pd
import bs4
import requests
import time
import asyncio
from playwright.async_api import async_playwright
import os

# set the data path and csv filename
os.environ['DATA_PATH'] = "/Users/marko/data_science/cycling_marketplace/scraping/global/wheels/data"
csv_filename = 'wheels_pdk.csv'

# Define base URL and initial URL
base_url = 'https://www.probikekit.com'
url = "https://www.probikekit.com/bike-wheels.list"
job_no = 4


# automate the cookie accept button
async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto('https://www.probikekit.com/bike-wheels.list')

        # Locate the accept button (the selector may change depending on the website)
        # We're using '#accept' as a placeholder.
        accept_button = await page.query_selector('#accept')

        # If the accept button exists (i.e., there is a cookie prompt), click it
        if accept_button:
            await accept_button.click()

        # Scrape your data here...

        # Example: Get the page title
        title = await page.title()
        print(f'Title of the page: {title}')

        await browser.close()

asyncio.run(run())


# data variable setting. no change needed for all websites
top_page_data_col = ['item_title', 'item_description', 'item_url']
det_page_data_col = ['item_component', 'item_price']
data_col_names = top_page_data_col + det_page_data_col

# Define HTML variables
html_vars = {
    'items_var': ('li', 'class', 'productListProducts_product'),
    'title_var': ('div', 'class', 'productBlock_title'),
    'link_var': ('a', 'class', 'productBlock_link'),
    'item_desc_var': ('div', 'class', 'productDescription_synopsisContent productDescription_synopsisContent-tabbed'),
    'component_var': ('select', 'class', 'productVariations_dropdown'),
    'price_var': ('p', 'class', 'productPrice_price'),
    'next_page_var': ('a', 'class', 'responsivePageSelectorActive')
}

while job_no < 5:
    response = requests.get(url)
    data = response.text
    soup = bs4.BeautifulSoup(data, 'html.parser')
    items = soup.find_all(html_vars['items_var'][0], {html_vars['items_var'][1]: html_vars['items_var'][2]})
    df_all = pd.DataFrame(columns=data_col_names)
    print("Page:", job_no)

    for item in items:
        item_title = []
        item_description = []
        item_url = []

        # add the location so as if nothing is there, not an error but NA is retuned
        location_title = item.find(html_vars['title_var'][0], {html_vars['title_var'][1]: html_vars['title_var'][2]})
        title = location_title.text.strip() if location_title else "NA"
        item_title.append(title)

        # get the urls to go to the details page
        link = item.find(html_vars['link_var'][0], {html_vars['link_var'][1]: html_vars['link_var'][2]}).get('href')
        # concatenate the base URL with the relative URL
        full_url = base_url + link
        item_url.append(full_url)
        # print no of iterratiosn
        print("Item:", len(item_url))

        item_response = requests.get(full_url)
        item_data = item_response.text
        # after getting the url, make a parser for that page, and based on the job, get further details
        item_soup = bs4.BeautifulSoup(item_data, 'html.parser')

        desc = item_soup.find(html_vars['item_desc_var'][0], {html_vars['item_desc_var'][1]: html_vars['item_desc_var'][2]})
        item_desc = desc.text.strip() if desc else "N/A"
        item_description.append(item_desc)
        # print iteration and description
        print("before top page, Description:", len(item_description))

        top_page_data = []
        for items_scraped_top in zip(item_title, item_description, item_url):
            top_page_data.append(items_scraped_top)

        top_page_data_pd = pd.DataFrame(top_page_data, columns=top_page_data_col)

        # get the type, price, discount within details page

        component = []
        price = []

        # If no components found, try to find 'select' tag with the class 'productVariations_dropdown'
        if not component:
            select_tag = item_soup.find(html_vars['component_var'][0], {html_vars['component_var'][1]: html_vars['component_var'][2]})
            # If the tag exists, get the text of the option with the class 'default'
            if select_tag:
                option_text = select_tag.find('option', class_='default').text.strip()
                if not option_text.startswith('Please select'):
                    component.append(option_text.replace('Please select', ''))

        # Try price_var
        for item in item_soup.findAll(html_vars['price_var'][0], {html_vars['price_var'][1]: html_vars['price_var'][2]}):
            price.append(item.get_text(strip=True))


        # If there are still no prices found, set the price to 'No price found'
        if not price:
            price = ['No price found']

        # As before, if no components are found, set the component to 'No components found'
        if not component:
            component = ['No components found']

        detail_page_data = []
        for items_scrapped_det in zip(component, price):
            detail_page_data.append(items_scrapped_det)

        detail_page_data_pd = pd.DataFrame(detail_page_data, columns=det_page_data_col)
        print("detail_page_data_pd:", detail_page_data_pd, len(top_page_data_pd))

        print("top_page_data_pd:", top_page_data_pd, len(top_page_data_pd))

        # multiply rows based on the number of compovariations, description is always the same
        top_page_data_pd = pd.concat([top_page_data_pd] * detail_page_data_pd.shape[0], ignore_index=True)
        print("after top page, Description:", len(top_page_data_pd))
        page_data = pd.concat([top_page_data_pd, detail_page_data_pd], axis=1, sort=False)
        job_no += 1
        print("Top page data:", len(top_page_data_pd))

        # add to the overall dataset
        df_all = pd.concat([df_all, page_data], axis=0, sort=False)

    # Moving to the next page (updated based on your HTML snippet)
    next_page_tag = soup.find(html_vars['next_page_var'][0], {html_vars['next_page_var'][1]: html_vars['next_page_var'][2]})
    if next_page_tag and 'href' in next_page_tag.attrs:
        url = next_page_tag['href']
        job_no += 1
        print(f"Moving to next page: {url}")
    else:
        print("No more pages to process.")
        break



# Get the directory path from environment variable
data_dir = os.environ.get('DATA_PATH', '.')

# Construct the full path to the file
file_path = os.path.join(data_dir, csv_filename)

# Save the data to this file path
print("Total Jobs:", job_no)
df_all.to_csv(file_path, index=False, encoding='utf-8-sig')

