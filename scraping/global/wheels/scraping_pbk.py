# -*- coding: utf-8 -*-

import pandas as pd
import bs4
import requests
import time
import asyncio
from playwright.async_api import async_playwright


# define the base URL
base_url = 'https://www.probikekit.com'


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

url = "https://www.probikekit.com/bike-wheels.list"
job_no = 4

# data variable setting
top_page_data_col = ['item_title','item_description', 'item_url']
det_page_data_col=['item_component','item_price']

data_col_names = top_page_data_col + det_page_data_col

# html variable setting
items_var = ['li', 'class', 'productListProducts_product']

# get the title of the item
title_var = ["div", "class", "productBlock_title"]
link_var = ['a','class', 'productBlock_link']
item_desc_var = ['div','class','productDescription_synopsisContent productDescription_synopsisContent-tabbed']

#component_var = ['ul','class', 'VariantAttributePicker_variantAttributePicker__WtDeM']
component_var = ['select', 'class', 'productVariations_dropdown']

price_var = ['p', 'class', 'productPrice_price']

price_var = ['span', 'class', 'productPrice_fromPrice']



next_page_var = ['a','class','responsivePageSelectorActive']

while job_no < 5:

    response = requests.get(url)
    data = response.text
    # giving it the format
    soup = bs4.BeautifulSoup(data, 'html.parser')
    # get all within a wrapper for easiness 
    items = soup.find_all(items_var[0],{items_var[1]:items_var[2]})
    
    df_all = pd.DataFrame(columns=data_col_names)
    print("Page:", job_no)

    for item in items:
        item_title = []
        item_description = []
        item_url = []

        # add the location so as if nothing is there, not an error but NA is retuned
        location_title = item.find(title_var[0], {title_var[1]:title_var[2]})
        title = location_title.text.strip() if location_title else "NA"
        item_title.append(title)
      
        # get the urls to go to the details page
        link = item.find(link_var[0], {link_var[1]: link_var[2]}).get('href')
        # concatenate the base URL with the relative URL
        full_url = base_url + link
        item_url.append(full_url)
        # print no of iterratiosn
        print("Item:", len(item_url))

        item_response = requests.get(full_url)
        item_data = item_response.text
        # after getting the url, make a parser for that page, and based on the job, get further details
        item_soup = bs4.BeautifulSoup(item_data, 'html.parser')

        desc = item_soup.find(item_desc_var[0],{item_desc_var[1]:item_desc_var[2]})
        item_desc = desc.text.strip() if desc else "N/A"
        item_description.append(item_desc)
        #printitteration and description
        print("before top page, Description:", len(item_description))

        top_page_data = []
        for items_scraped_top in zip(item_title, item_description,item_url):
            top_page_data.append(items_scraped_top)
            
        top_page_data_pd = pd.DataFrame(top_page_data,columns=top_page_data_col)  

        # get the type, price, discount within details page
        # have to find the way to check within the wrapper, in sub-clases

        component = []
        price = []

		# If no components found, try to find 'select' tag with the class 'productVariations_dropdown'
        if not component:
            select_tag = item_soup.find('select', class_='productVariations_dropdown')
            # If the tag exists, get the text of the option with the class 'default'
            if select_tag:
                option_text = select_tag.find('option', class_='default').text.strip()
                if not option_text.startswith('Please select'):
                    component.append(option_text.replace('Please select', ''))


		# Try first price_var
        price_var = ['p', 'class', 'productPrice_price']
        for item in item_soup.findAll(price_var[0], {price_var[1]: price_var[2]}):
            price.append(item.get_text(strip=True))  

        # If no price was found using the first price_var, try the second one
        if not price:
            price_var = ['span', 'class', 'productPrice_fromPrice']
            for item in item_soup.findAll(price_var[0], {price_var[1]: price_var[2]}):
                price.append(item.get_text(strip=True))  

		# If there are still no prices found, set the price to 'No price found'
        if not price:
            price = ['No price found']

        # As before, if no components are found, set the component to 'No components found'
        if not component:
            component = ['No components found']


        detail_page_data = []
        for items_scrapped_det in zip(component,price):
            detail_page_data.append(items_scrapped_det)



        # for sales, better calculate aggainst the original price as comparison will not make much sense    
        detail_page_data_pd = pd.DataFrame(detail_page_data,columns=det_page_data_col)    
        # print top_page_data_pd, detail_page_data_pd.shape[0]  values
        print("detail_page_data_pd:",detail_page_data_pd, len(top_page_data_pd) )

        print("top_page_data_pd:",top_page_data_pd, len(top_page_data_pd) )
                        
        # multiplicate rows based on the number of compovariations, descreption is always the same
        top_page_data_pd = pd.concat([top_page_data_pd]*detail_page_data_pd.shape[0], ignore_index=True)
        print("after top page, Description:", len(top_page_data_pd) ) 
        page_data = pd.concat([top_page_data_pd, detail_page_data_pd], axis=1, sort=False)
        job_no+=1
        # print the number of iterations and top page data
        print("Top page data:", len(top_page_data_pd))

        # add to the overral dataset
        df_all = pd.concat([df_all, page_data], axis=0, sort=False)

    # moving to the next page
    active_page = soup.find('a', {'class': 'responsivePaginationButton responsivePageSelector responsivePageSelectorActive'})
    # print the active page and the next page number
    print("Active page:", active_page, "Next page number:", next_page_number)

    if active_page:
        current_page_number = int(active_page.text.strip())
        next_page_number = current_page_number + 1

        # Construct the URL for the next page
        url = f"https://www.probikekit.com/bike-wheels.list?pageNumber={next_page_number}"
        print(url)
        # print the url and the next page number
        print("last loop URL:", url, "Next page number:", next_page_number)
        # make it sleep to avoid errors
        page = ''
        while page == '':
            try:
                page = requests.get(url)
                break
            except:
                print("Connection refused by the server..")
                print("Let me sleep for 5 seconds")
                print("ZZzzzz...")
                time.sleep(5)
                print("Was a nice sleep, now let me continue...")
                continue

    else:
        break

print("Total Jobs:", job_no)

# write df_all to csv in current directory
df_all.to_csv('scraping_wiggle.csv', index=False, encoding='utf-8-sig')

   
#### test 

# open the file in write mode ('w')
with open('myfile.txt', 'w') as f:
    f.write(str(item_soup))