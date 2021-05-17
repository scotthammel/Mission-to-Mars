#!/usr/bin/env python
# coding: utf-8

# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page
# Search for elements with a specific combination of tag (div) and attribute (list_text)
# Tell our browser to wait one second before searching for components
browser.is_element_present_by_css('div.list_text', wait_time=1)


# Set up the HTML parser
html = browser.html
news_soup = soup(html, 'html.parser')
# Assign slide_elem as the variable to look for the <div /> tag and its descendent(other tags within the <div /> element)
# 'div.list_text' pinpoints the <div /> tag with the class of list_text
slide_elem = news_soup.select_one('div.list_text')

# chain ".find" onto our previously assigned variable, slide_elem.
slide_elem.find('div', class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
# .get_text(). -this method is chained onto .find(), only the text of the element is returned
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


### Featured Images

# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
# The browser finds an element by its tag
# Splinter will "click" 
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Use the image tag and class (<img />and fancybox-img) to build the URL to the full-size image
# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
# Use an f-string for this print statement 
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

# Scrape the entire table with Pandas' .read_html() function
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

# Convert our DataFrame back into HTML-ready code
df.to_html()

browser.quit()
