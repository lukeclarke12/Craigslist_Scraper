from selenium import webdriver

# Old way of doing things that works with Firefox
# driver = webdriver.Firefox()
# driver.get("http:google.com")

# The way of doings things that works in Google Chrome
# First download the chrome driver for your specific operating system

chromedriver = "home/lukeclarke/downloads/chromedriver"      # Insert the filepath towherever you have the chrome driver downloaded
driver = webdriver.Chrome(chromedriver)
driver.get('http:google.com')


