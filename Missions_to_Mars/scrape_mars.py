from bs4 import BeautifulSoup as soup
from splinter import Browser
import pandas as pd
import datetime as dt

def scrape_all():

    executable_path = {'executable_path': 'C:\ShankersDocs\chromedriver_win32\chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_p = mars_news(browser)

    data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser),
        "last_modified": dt.datetime.now()
    }

    browser.quit()
    return data

def mars_news(browser):

    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    news_soup = soup(html, 'html.parser')

    try:

        slideelement = news_soup.select_one('ul.item_list li.slide')
        slideelement.find("div",class_='content_title')

        news_title = slideelement.find("div",class_='content_title').get_text()
        news_title

        news_p = slideelement.find("div",class_='article_teaser_body').get_text()
        news_p
    except AttributeError:
        return None,None

    return news_title,news_p

def featured_image(browser):


    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    full_image_element = browser.find_by_id('full_image')
    full_image_element.click()

    browser.is_element_present_by_text('more info',wait_time=1)
    more_info_element = browser.links.find_by_partial_text('more info')
    more_info_element.click()

    html = browser.html
    imagesoup = soup(html,'html.parser')

    try:
        imageurlrelative = imagesoup.select_one('figure.lede a img').get("src")

    except AttributeError:  
        return None

    featured_image_url = f"https:/www.jpl.nasa.gov{imageurlrelative}"
    return featured_image_url

def mars_facts():
    
    df = pd.read_html("https://space-facts.com/mars/")[0]
    df.head()

    df.columns = ['Description','Mars']
    df.set_index('Description',inplace=True)
    return df.to_html(classes="table table-striped")

def hemispheres(browser):

    hemisphere_image_urls = []

    mars_hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_hemi_url)
    links = browser.find_by_css("a.product-item h3")
    for i in range(len(links)):
        hemisphere = {}
        browser.find_by_css("a.product-item h3")[i].click()
        sample_element = browser.links.find_by_text('Sample').first
        hemisphere["img_url"] = sample_element['href']
        hemisphere['title'] = browser.find_by_css("h2.title").text
        hemisphere_image_urls.append(hemisphere)
        browser.back()

    return hemisphere_image_urls