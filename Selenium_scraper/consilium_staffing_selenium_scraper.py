from selenium import webdriver
from selenium.webdriver.common.by import By # for locating elements in the document
import pandas as pd
# create the chrome driver instance
chrome_driver_path = '../../../../ChromeDriver/ChromeDriver_102/chromedriver.exe'
driver = webdriver.Chrome(chrome_driver_path)

#set up URL for navigation
url = 'https://webscraper.io/test-sites/e-commerce/allinone-popup-links/computers/laptops'
# move to URL
driver.get(url);

# create list to hold scraped info ( will be using List of Dictionaries )
information_list = []

# isolate the div that holds all links
laptop_links_div = driver.find_element_by_class_name('col-md-9')

# parse the links from within the parent div-element
laptop_links = laptop_links_div.find_elements_by_class_name('title')

'''
For each link in the first 10:

    designate the primary window for navigation after nth scrape
    
    click the link to open laptop info page/pop-up
    
    designate pop-up window
    
    switch into the pop-up window "re-initiating" the driver to the new pop up HTML
    
    isolate the div-element with all of the desired information
    
    parse the child elements and slice/clean info for adding to dictionary
    
    create dictionary at bottom to format column order ahead of time
    
    send dictionary to list and repeat.
    
'''
for i,link in enumerate(laptop_links[:10]):
    # designate the primary window for navigation after nth scrape
    
    primary_window = driver.window_handles[0]
    # click the link to open laptop info page/pop-up
    
    clickable_title = link.click()
    # designate pop-up window
    
    secondary_window = driver.window_handles[1]
    # switch into the pop-up window "re-initiating" the driver to the new pop up HTML
    
    driver.switch_to.window(secondary_window)
    # isolate the div-element with all of the desired information
    
    pop_up_info_div = driver.find_element_by_class_name('col-lg-10')
    # parse the child elements and slice/clean info for adding to dictionary
    
    # find the second h4, extract the text
    name = pop_up_info_div.find_elements_by_tag_name('h4')[1].text

    # Find the button to change price to ***GB, click it, set price with minor formatting
    option_256GB = pop_up_info_div.find_element(By.XPATH, "//button[@type='button'][@value='256']")
    option_256GB.click()
    price_256GB = pop_up_info_div.find_elements_by_tag_name('h4')[0].text.replace('$','')

        
    # Find the button to change price to ***GB, click it, set price with minor formatting
    option_1024GB = pop_up_info_div.find_element(By.XPATH, "//button[@type='button'][@value='1024']")
    option_1024GB.click()
    price_1024GB = pop_up_info_div.find_elements_by_tag_name('h4')[0].text.replace('$','')

    # find the description, extract the text
    description_element = pop_up_info_div.find_element_by_class_name('description')
    description_text = description_element.text

    # find the reviews, extract the number of reviews
    reviews_div = pop_up_info_div.find_element_by_class_name('ratings')
    num_reviews = reviews_div.find_element_by_tag_name('p').text.split(' ')[0]
    
    # create dictionary at bottom to format column order ahead of time
    laptop_info_dict = {
        'name': name,
        'price_256GB_usd': price_256GB,
        'price_1024GB_usd': price_1024GB,
        'description': description_text,
        'num_reviews': num_reviews
    }
    
    # send dictionary to list and repeat.    
    information_list.append(laptop_info_dict)

    # close the current pop-up window, switch to primary window
    driver.close()
    driver.switch_to.window(primary_window)

# close browser after scraping is complete
driver.quit()

# create the dataframe
df = pd.DataFrame(information_list)

# change dtypes to best fit the data
df['price_256GB_usd'] = df['price_256GB_usd'].astype('float')
df['price_1024GB_usd'] = df['price_1024GB_usd'].astype('float')
df['num_reviews'] = df['num_reviews'].astype('int')

# save the dataframe as csv
df.to_csv('scraped_laptop_info.csv', index=False)