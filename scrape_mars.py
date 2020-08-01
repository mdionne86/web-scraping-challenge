# import dependencies
from bs4 import BeautifulSoup as soup
from splinter import Browser
import pandas as pd
import requests
import pymongo


def init_browser():
   # open chrome driver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()

    
    # # NASA Mars News 
    
    # # define url
    mars_news_url = "https://mars.nasa.gov/news/"
    browser.visit(mars_news_url)

    # # create the soup
    html = browser.html
    mars_news_soup = soup(html, 'html.parser')

    # set the parent element up to search through later
    news_parent_element = mars_news_soup.select_one("ul.item_list li.slide")

    # find the first news title
    news_title = news_parent_element.find("div", class_="content_title").get_text()

    # find the paragraph associated with the first title
    news_p = news_parent_element.find("div", class_="article_teaser_body").get_text()


    # JPL Mars Space Images - Featured Image

    # define the url and visit it with browser
    mars_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(mars_image_url)

    # click on the link to access the full image
    browser.click_link_by_id('full_image')

    # click on the more info button to get to the large image
    browser.click_link_by_partial_text('more info')

    # create the soup
    image_html = browser.html
    mars_image_soup = soup(image_html, 'html.parser')

    # store the class
    image = mars_image_soup.body.find("figure", class_="lede")

    # find the "a element" to extract the url
    link = image.find('a')
    href = link['href']

    # complete the url
    featured_image_url = 'https://www.jpl.nasa.gov' + href


    # Mars Weather

    # open url in browser
    mars_weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(mars_weather_url)

    # soup time
    html = browser.html
    mars_weather_soup = soup(html, 'html.parser')

    # find the tweet text
    mars_weather = mars_weather_soup.body.find('div','css-901oao r-jwli3a r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0').text
    
    
    # Mars Facts
    
    # define url
    mars_facts_url = "https://space-facts.com/mars/"

    # read html into pandas
    tables = pd.read_html(mars_facts_url)

    # set up dataframe
    mars_facts_df = tables[0]
    mars_facts_df.columns = ["Description", "Value"]

    # convert to html
    mars_facts_html=mars_facts_df.to_html()


    # Mars Hemispheres

    # set up for Cerberus Hemisphere

    # define url and open in browser
    mars_hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser.visit(mars_hemispheres_url)

    browser.click_link_by_partial_text('Cerberus')
    browser.click_link_by_partial_text('Open')

    # soup
    hemispheres_html = browser.html
    cerberus_soup = soup(hemispheres_html, 'html.parser')

    cerberus = cerberus_soup.body.find('img', class_ = 'wide-image')
    cerberus_img = cerberus['src']

    hem_base_url = 'https://astrogeology.usgs.gov'
    cerberus_url = hem_base_url + cerberus_img
    
    # set up for Schiaparelli Hemisphere

    # define url and open in browser
    mars_hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser.visit(mars_hemispheres_url)

    browser.click_link_by_partial_text('Schiaparelli')
    browser.click_link_by_partial_text('Open')

    # soup
    schiaparelli_html = browser.html
    schiaparelli_soup = soup(schiaparelli_html, 'html.parser')

    schiaparelli = schiaparelli_soup.body.find('img', class_ = 'wide-image')
    schiaparelli_img = schiaparelli['src']

    hem_base_url = 'https://astrogeology.usgs.gov'
    schiaparelli_url = hem_base_url + schiaparelli_img

    # set up for Syrtis Major Hemisphere

    # define url and open in browser
    mars_hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser.visit(mars_hemispheres_url)

    browser.click_link_by_partial_text('Syrtis')
    browser.click_link_by_partial_text('Open')


    # soup
    syrtis_html = browser.html
    syrtis_soup = soup(syrtis_html, 'html.parser')

    syrtis = syrtis_soup.body.find('img', class_ = 'wide-image')
    syrtis_img = syrtis['src']

    hem_base_url = 'https://astrogeology.usgs.gov'
    syrtis_url = hem_base_url + syrtis_img

    # set up for Valles Marineris Hemisphere

    # define url and open in browser
    mars_hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser.visit(mars_hemispheres_url)

    browser.click_link_by_partial_text('Valles')
    browser.click_link_by_partial_text('Open')

    # soup
    valles_html = browser.html
    valles_soup = soup(valles_html, 'html.parser')

    valles = valles_soup.body.find('img', class_ = 'wide-image')
    valles_img = valles['src']

    hem_base_url = 'https://astrogeology.usgs.gov'
    valles_url = hem_base_url + valles_img

    hemispheres_image_urls = [
        {"title": "Cerberus Hemisphere", "img_url": cerberus_url},
        {"title": "Schiaparelli Marineris Hemisphere", "img_url": schiaparelli_url},
        {"title": "Syrtis Major Hemisphere", "img_url": syrtis_url},
        {"title": "Valles Marineris Hemisphere", "img_url": valles_url}
    ]

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts": mars_facts,
        "hemispheres_image_urls": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data

if __name__ == '__main__':
    scrape()