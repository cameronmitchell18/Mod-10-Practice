# %%
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


def scrape_all():
     #Initialize headless driver for deployment 
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

def mars_news(browser):

    # setting url to the website we want to scrape 
    url = 'https://redplanetscience.com/'

    browser.visit(url)

    # Optional delay for loading the page 

    # NOTE: The optional delay is useful because sometimes dynamic pages take a little while to load, 
    # especially if they are image-heavy.

    browser.is_element_present_by_css('div.list_test' , wait_time = 1)

    html = browser.html

    news_soup = soup(html , 'html.parser')

    slide_elem = news_soup.select_one('div.list_text')

    # slide_elem as the variable to look for the <div /> tag and its descendent. This is our parent element.

    # 'div.list_text' pinpoints the <div /> tag with the class of list_text.
    try:

        slide_elem.find('div' , class_ = 'content_title')

        # we chained .find onto our previously assigned variable, slide_elem.
        # When we do this, we're saying, "This variable holds a ton of information, 
        # so look inside of that information to find this specific data."

        # Use the parent element to find the first `a` tag and save it as `news_title`

        news_title = slide_elem.find('div', class_='content_title').get_text()

        # .get_text(). When this new method is chained onto .find(), only the text of the element is returned. 

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None , None

    return news_title , news_p

    


### Featured Images

# Visit URL
def featured_image(browser):
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

# Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

# Parse the resulting html with soup
  
    html = browser.html
    img_soup = soup(html, 'html.parser')

# Find the relative image url
    try:
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

# NOTE: .get('src') pulls the link to the image.
# Use the base URL to create an absolute URL

    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

def mars_facts():
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    except BaseException:
        return None

    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    return df.to_html()

#browser.quit()

# df = pd.read_html('https://galaxyfacts-mars.com')[0]
# df.columns=['description', 'Mars', 'Earth']
# df.set_index('description', inplace=True)
# df.to_html()

#browser.quit()


