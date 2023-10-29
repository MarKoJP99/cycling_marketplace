import pandas as pd
import bs4
import requests
import time
import asyncio
from playwright.async_api import async_playwright
import os
import re  


# set the data path and csv filename
os.environ['DATA_PATH'] = "/Users/marko/data_science/cycling_marketplace/scraping/global/wheels/data"
csv_filename = 'wheels_wiggle.csv'


# Define base URL and initial URL
base_url = 'https://www.wiggle.com/'
url = "https://www.wiggle.com/c/cycle/bike-parts/wheels-and-tyres/wheels?index=y&discipline=Road+bike"
job_no = 1

# automate the cookie accept button
async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134")
        page = await context.new_page()
        await page.goto('https://www.wiggle.com/c/cycle/bike-parts/wheels-and-tyres/wheels')

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
top_page_data_col = ['item_title','item_description', 'item_url']
det_page_data_col=['item_component','item_price']
data_col_names = top_page_data_col + det_page_data_col

job_no = 1
html_vars = {
    'items_var': ('li', 'data-testid', 'ProductCard'),
    'title_var': ('span', 'class', 'Button_wrapper__Q7fHm'),
    'link_var': ('a', 'class', 'ProductCard_imageContainer__yZLWr'),
    'item_desc_var': ('div.RichText_body__TTyRx:not(.MessageStrip_richTextContainer__S5Fb3)', 'css selector'),
    'component_ul_var': ('ul', 'class', 'VariantAttributePicker_variantAttributePicker__X6shd'),
    'component_h2_var': ('h2', 'class', 'ProductVariantSelector_label__mMTE2'),

    'price_var': ('p', 'data-testid', 'product-price'),
    'next_page_var': ('a', 'data-testid', 'pagination-next')
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

        desc = item_soup.select_one(html_vars['item_desc_var'][0])
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

        # Find all 'li' elements
        li_tags = item_soup.find_all('li', class_='ProductVariantSelector_productFilter__kHwM5')

        # Iterate through the 'li' elements
        for li_tag in li_tags:
            # Find the 'h2' tag within the current 'li' tag
            h2_tag = li_tag.find('h2', class_='ProductVariantSelector_label__mMTE2')
            if h2_tag:
                # Check if the 'h2' tag text contains "Freehub Body"
                if "Freehub Body" in h2_tag.text:
                    # Check if there's a 'ul' tag with class 'VariantAttributePicker_variantAttributePicker__X6shd' within the current 'li' tag
                    ul_tag = li_tag.find('ul', class_='VariantAttributePicker_variantAttributePicker__X6shd')
                    if ul_tag:
                        # If 'ul' tag is found, iterate through its 'button' children
                        for button in ul_tag.find_all('button', class_='VariantAttribute_variantAttribute__d6Cs3'):
                            # Check if the button does not have the unwanted class
                            if 'VariantAttribute_noStock__SLuEt' not in button['class']:
                                # Extract the text from the nested 'span' element and add it to the 'component' list
                                component.append(button.find('span').text)
                    else:
                        # If 'ul' tag is not found, extract the component option directly from the 'h2' tag text
                        component_option = h2_tag.text.split(': ')[1]
                        component.append(component_option)
                    break  # Exit the loop as we've found what we were looking for







        # Try price_var
        price_tag = item_soup.find(html_vars['price_var'][0], {html_vars['price_var'][1]: html_vars['price_var'][2]})
        if price_tag:
            price.append(price_tag.get_text(strip=True))


        # If there are still no prices found, set the price to 'No price found'
        if not price:
            price = ['No price found']

        # As before, if no components are found, set the component to 'No components found'
        if not component:
            component = ['No components found']

        # Join the elements of 'component' and 'price' into single strings
        component_str = ', '.join(component)
        price_str = ', '.join(price)

        # Create a tuple containing the two strings, and append it to 'detail_page_data'
        detail_page_data = [(component_str, price_str)]

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




