#!/usr/bin/env python
import csv                                                          
from selenium import webdriver

MAX_PAGE_NUM = 5
MAX_PAGE_DIG = 3

# Buyer | Price
# name1 | Price1

with open('result.csv', 'w') as f:    # open a csv file called result.csv and write
    f.write("Buyers, Price \n")       # buyers column, price column and a line then to start write in info

# Open up a firefox browser and navigate to webdriverr
driver = webdriver.Firefox()

for i in range(1, MAX_PAGE_NUM + 1):    # range 1 to max number of pages plus 1
    page_num = (MAX_PAGE_DIG - len(str(i)))*"0" + str(i)
    url = "http://econpy.pythonanywhere.com/ex/" + page_num  +  ".html"

    driver.get(url)

    # Extract lists of buyers and prices based on Xpath
    buyers = driver.find_elements_by_xpath('//div[@title="buyer-name"]')
    prices = driver.find_elements_by_xpath('//span[@class="item-price"]')
    # function in selenium, there are many other methods to find things other then
    # xpath, the above will extract all of the buyer name elements and put them
    # into a list, so next thing is that we need to extract the text from these
    # elements

    num_page_items = len(buyers)
    with open('result.csv', 'a') as f:     # append as f
        for i in range(num_page_items):
            f.write(buyers[i].text + "," + prices[i].text + '\n')   # add comma as it is a comma separated file and the \n for a new line
            

# Clean up or close the browser once the task is completed 
driver.close()
