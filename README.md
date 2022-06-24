# consilium_staffing_scraper
A light scraper for obtaining the first X laptops of an internet sales page, then saving as a CSV on local.


# Brief Explanation:

## Why Splinter?

Splinter is a wrapper for Selenium that allows for an extension of the automation while also reducing the amount of code needed to produce the same results.

I highly recommend Splinter do to its straight forward documentation and ease of use with beautifulsoup4.
This combination of scraping software is my go-to team when I need to scrape digital information from websites.

Here is a link to the Documentation:
[Check it out!](https://splinter.readthedocs.io/en/latest/why.html)


# Demonstration:

Just to be safe, I'm including a video demonstration of the Scripting Logic to show how Splinter works in conjunction with BS4.

[Video Link is here!](https://youtu.be/-_gFnLUSqQ4)


# Challenges:

For a test website, 'https://webscraper.io/test-sites/e-commerce/allinone-popup-links/computers/laptops' had a strange set up HTML-wise.

For example when attempting to navigate the website, all clickable links from the front page didn't follow a traditional link arrangemt like:

        a href= 'website.com'

and instead were like this:

        a href="#" onclick="window.open('/test-sites/e-commerce/allinone-popup-links/product/545',
        'product545', 'height=768,width=1024')" class="title">Asus VivoBook X4.../a

Meaning that the link used browser commands to open a blank window then navigate to the page, making link scraping a bit more of a hassle.

To get around this, I used Beautiful Soup to isolate the Attribute information for the laptops in question and created a list of useable links for the Selenium Browser to visit.

        # extract the url from the onclick attribute, slice out the link
        element_link_partial = a_tag['onclick'].split("'")[1]
        # combine with string to construct full link
        element_link_full = f'https://webscraper.io{element_link_partial}'

Manipulating the a tag attributes like this allowed me to simplify the scraping process by not adding logic for navigating the newly opened windows, and instead have simple commands to conduct all scraping in one window.

Once visited, the scraping bot would collect all static information, then click two of four buttons that, when activated, changed the listed price of the currently viewed laptop. After clicking this button, I had the bot slice out the desired price for 256GB & 1024GB HDD/SSD laptops, then the information goes through some light transformations before it is stored into a dictionary. The loop then repeats with the next laptop in question.

Once all of the information was collected, I used Pandas to construct a Dataframe from the list of dictionaries before utilizing pd.series.astype() method to change the scraped data from strings to float or integer as needed before saving as a CSV on local.



# Odds and Ends:

## Why the function for a small program?

In line 50, I made a function for the sake of adjusting should the client want more laptop information.
This wayI can return and change one number in line 74 then run the program for maximum ease and utility.

    Line 50:
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

        Line 74:
        laptop_list = links_to_list(10)

## Cleaning the Data during the Gathering/Extraction step:
The data cleaning I performed was a simple mix of removing characters that would get in the way of further cleaning / aggregations.

For example:
The prices were float values, collected as strings, with '$' symbols in the mix. I removed the currency symbol and set the column as a float so that aggregations could be performed in other software, shoudl the CSV never make it back to Pandas.

The Reviews was another matter of Data Type conversion. I made sure to convert these into integers before saving the final CSV.

The laptops contained the names and colors in the same lines of the HTML code meaning that some have Colors in the name and some do not. To make future data cleaning simplier, I removed all of the commas so that the series elements could be split() and colors removed using a filter/replace logic if needed. Since this was the first step of the Data ETL process, I left data cleaning to a minimum.

# Conclusion:

Scraping data is fun and I really enjoyed the unconventional set up of this website. It helped me flex my brain muscles in coming up with a means of isolating and parsing data that I did not originally have easy access to, giving me a new approach to this problem should I encounter it again.

