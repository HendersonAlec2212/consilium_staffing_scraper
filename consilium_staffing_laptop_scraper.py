from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd

# goal - grab all of the laptops on the page

# isolate into a list of the first 10 laptops

# guide the bot to click the href of each laptop and dump the info for the 256 & 1024GB versions into a list

# further parse the new list for all of the desired info

# add that info into a list of dictionaries

# form that list into a CSV

# format data types

# save the CSV file 

################################### Begin ###################################

# set up splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

url = 'https://webscraper.io/test-sites/e-commerce/allinone-popup-links/computers/laptops'
browser.visit(url)

# create the soup object
html = browser.html
laptop_soup = BeautifulSoup(html, 'html.parser')

# isolate the div will all of the laptops
all_laptops = laptop_soup.find_all('div', class_='col-sm-4 col-lg-4 col-md-4')

def links_to_list(num_laptops):
    
    '''
    This function accepts an integer for the number of links / laptops 
    to scrape from the front page of the test-scrape website
    
    :param: num_laptops - INT - the number of laptop links
    '''
    
    link_list = []

    for i, laptop in enumerate(all_laptops[:num_laptops]):
        #isolate the link
        a_tag = laptop.find('a')
        # extract the url from the onclick attribute, slice out the link
        element_link_partial = a_tag['onclick'].split("'")[1]
        # combine with string to construct full link
        element_link_full = f'https://webscraper.io{element_link_partial}'
        # add to list for later use
        link_list.append(element_link_full)
        
    return link_list


'''
For each link in the list:
    - navigate to the page
    - slice the desired information, manipulating HTML as needed for varying values
    - assign information to variables
    - assemble dictionary
    - add dictionary to list for conversion to Dataframe in later step
'''
# set list to hold laptop information
information_list = []

laptop_list = links_to_list(10)

for i in range(0,len(laptop_list)):
    
    # set up link for browser and soup object
    link = laptop_list[i]
    browser.visit(f'{link}')

    # create soup object now that HTML has changed (from front page)
    html = browser.html
    laptop_soup = BeautifulSoup(html, 'html.parser')
    
    # extract the static information
    description = laptop_soup.find('p', class_='description').get_text().replace(',','')
    
    name_div = laptop_soup.find('div',class_='caption')
    name = name_div.find_all('h4')[1].get_text()
    
    # isolate number of reviews, remove whitespace, take only numerical digits
    num_reviews = laptop_soup.find('div',class_='ratings').get_text().strip().split(' ')[0]
    
    # find the button for 256GB price, click it
    browser.find_by_value('256').click()
    
    # reset soup object due to changes in HTML
    html = browser.html
    laptop_soup = BeautifulSoup(html, 'html.parser')
    
    # set the price variable - clean the $ characters out for dtype changes later
    price_256 = laptop_soup.find('h4',class_='pull-right price').get_text().replace('$','')

    # find the button for 1024GB price, click it
    browser.find_by_value('1024').click()

    # reset soup object due to changes in HTML
    html = browser.html
    laptop_soup = BeautifulSoup(html, 'html.parser')
    
    # set the price variable - clean the $ characters out for dtype changes later
    price_1024 = laptop_soup.find('h4',class_='pull-right price').get_text().replace('$','')
    laptop_info = {
        'name': name,
        'price_256GB_usd': price_256,
        'price_1024GB_usd': price_1024,
        'description': description,
        'num_reviews': num_reviews,
    }
    information_list.append(laptop_info)
browser.quit()

# create the dataframe
df = pd.DataFrame(information_list)

# change dtypes to best fit the data
df['price_256GB_usd'] = df['price_256GB_usd'].astype('float')
df['price_1024GB_usd'] = df['price_1024GB_usd'].astype('float')
df['num_reviews'] = df['num_reviews'].astype('int')

# save the data as csv
df.to_csv('../data/scraped_laptop_info.csv', index=False)