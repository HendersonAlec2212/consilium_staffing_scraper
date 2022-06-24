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

Once visited, the scraping bot would collect all static information, then click two of four buttons that, when activated, changed the listed price of the currently viewed laptop. After clicking this button, I had the bot slice out the desired price for 256GB & 1024GB HDD/SSD laptops, then store the information into a dictionary before repeating with the next laptop in question.

Once all of the information was collected, I used Pandas to construct a Dataframe from the list of dictionaries before utilizing pd.series.astype() method to change the scraped data from strings to float or integer as needed before saving as a CSV on local.

# Conclusion:

Scraping data is fun and I really enjoyed the unconventional set up of this website. It helped me flex my brain muscles in coming up with a means of isolating and parsing data that I did not originally have easy access to, giving me a new approach to this problem should I encounter it again.

