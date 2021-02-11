#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup
import urllib.request
import csv

# open a csv called craigslist products
with open('craigslist_products.csv', 'w') as f:
    f.write("Date, Title, Price, url \n")

location = "sfbay"
postal = "94201"
max_price = "500"
radius = "5"


class CraigslistScraper(object):
    def __init__(self, location, postal, max_price, radius):
        self.location = location
        self.postal = postal
        self.max_price = max_price
        self.radius = radius

        self.url = f"https://{location}.craigslist.org/search/sss?search_distance={radius}&postal={postal}&max_price={max_price}"
        self.driver = webdriver.Firefox()
        self.delay = 3  # three seconds

    def load_craigslist_url(self):
        self.driver.get(self.url)    # get navigates to the url that we pass to it

        # we need to build a try & except statement to try until the website
        # loads or else the script will run faster then the website can load
        # and there will be nothing to scrape

        try:
            wait = WebDriverWait(self.driver, self.delay)
            wait.until(EC.presence_of_element_located((By.ID, "searchform")))
                       #can specify, id css class etc.
                       #id="searchform" can be found in webpage code
                       #Note EC for expected condition, we are waiting until
                       #the expected object is loaded on the web page we want to
                       #scrape content from

            print("Page is ready")

        except:

            print("Loading took to much time")            
    

    def extract_post_information(self):
        all_posts = self.driver.find_elements_by_class_name("result-row")
        
        dates = []
        titles = []
        prices = []

        for post in all_posts:
            title = post.text.split("$")

            if title[0] == "":
                title = title[1]

            else:
                title = title[0]

            title = title.split("\n")
            price = title[0]
            title = title[-1]

            date_and_title_list = title.split(" ")
            month = date_and_title_list[0]
            day = date_and_title_list[1]
            date = month + " " + day
            title = ' '.join(date_and_title_list[2:])


            titles.append(title)
            dates.append(date)
            prices.append(price)

        return titles, prices, dates

    def extract_post_urls(self):
        html_page = urllib.request.urlopen(self.url)   # opens url as specified by a string
        #html_page = urllib3.PoolManager.request(method='GET', url=self.url)
        soup = BeautifulSoup(html_page, 'lxml')       # lxml isnt necessary just gets rid of warnings
        #We out url into beautifulsoup object which gives us some nice
        #functionalty to easily extract information

        #links in beautiful soup are specified by "a"
        url_list = [link["href"] for link in soup.findAll('a', {"class":"result-title hdrlnk"})]
        return url_list

    def quit(self):
        self.driver.close()



scraper = CraigslistScraper(location, postal, max_price, radius)


scraper.load_craigslist_url()
titles, prices, dates = scraper.extract_post_information()
urls = scraper.extract_post_urls()


num_page_items = len(urls)
# write retrieved data into the craigslist_pruducts csv file
with open('craigslist_products.csv', 'a') as f:
    for i in range(num_page_items):
        f.write(dates[i] + "," + titles[i] + "," + prices[i] + "," + urls[i] + '\n')

scraper.quit()



