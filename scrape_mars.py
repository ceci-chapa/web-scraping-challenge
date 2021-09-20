from splinter import Browser
from bs4 import BeautifulSoup
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager


def scrape_info():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # NASA Mars News - Getting the titles --------------
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')

    results = soup.find_all('div', class_='list_text')
    news_title = results[0].find('div', class_='content_title').text
    news_p = results[0].find('div', class_='article_teaser_body').text




    

    #Make a dictionary to contain all variables to use later in my app/html



    # Close the browser after scraping
    browser.quit()

    # Return results from the dictionary variable
    return 
