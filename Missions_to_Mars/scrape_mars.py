from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    mars_dict={}
    browser=init_browser()

    # Navigate to Nasa page
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html=browser.html
    soup=bs(html,'html.parser')
    #find title of latest news
    news_title=soup.find_all('div', class_='content_title')[1].find('a').text
    #Latest news paragraph
    news=soup.find_all('div', class_='article_teaser_body')[0].text

    # Navigate to JPL mars page
    jpl_url='https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(jpl_url)
    html=browser.html
    soup=bs(html,'html.parser')
    # find features image in JPL mars page
    featured_image_url=soup.find('img', class_='headerimage fade-in')['src']
    featured_image_url='https://data-class-jpl-space.s3.amazonaws.com/JPL_Space'+featured_image_url

    # Navigate to space fact website, save data in table formtat as html
    Fact_url="https://space-facts.com/mars/"
    tables=pd.read_html(Fact_url)
    html_tbale=tables[0].to_html()

    # Scrape Mars hemisphere title and image
    image_website="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(image_website)
    html=browser.html
    soup=bs(html,'html.parser')

    # find image urls and titles
    hemisphere_image_urls=[]
    images_links=soup.find_all('div', class_='description')
    for images in images_links:
        image_title=images.find('h3').text
        image_page_url='https://astrogeology.usgs.gov'+images.find('a')['href']
        browser.visit(image_page_url)
        page=browser.html
        img_soup=bs(page, 'html.parser')
        download=img_soup.find_all('div', class_='downloads')
        image_url=download[0].find_all('a')[1]['href']
        url_dict={'Title':image_title, 'Image URL':image_url}
        hemisphere_image_urls.append(url_dict)
    mars_dict={
        "News Title": news_title,
        "News Paragraph": news,
        "Featured Image URL": featured_image_url,
        "Fact Table": html_tbale,
        "Hemisphere Images": hemisphere_image_urls
    }
    browser.quit()
    return mars_dict








