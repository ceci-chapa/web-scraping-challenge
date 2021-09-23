from splinter import Browser
from bs4 import BeautifulSoup
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


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
    # End of Title Scrapping --------------



    # JPL Mars Space Images - Getting Featured Image --------------
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    #finding the button
    button = browser.find_by_tag('button')[1]

    #click button
    button.click()

    html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')

    find_image = soup.find('img', class_="fancybox-image")

    image_link = find_image.get('src')

    spaceimages = 'https://spaceimages-mars.com/'

    featured_image_url = spaceimages + image_link
    # End of Title Scrapping --------------


    # Start of Table Scrape ---------------
    url = 'https://galaxyfacts-mars.com/'
    table = pd.read_html(url)

    df = table[0]
    df.columns = ["Description", "Mars", "Earth"]
    df.set_index("Description", drop=True, inplace=True)

    table_html = df.to_html()

    # End of Table Scrape----------------


    # Mars Hemispheres - Getting the titles and each image --------------

    url = 'https://marshemispheres.com/'
    browser.visit(url)

    #scraping titles
    html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')

    title_search = soup.find_all('div', class_="collapsible results")

    titles = soup.find_all('h3')

    title_list = []
    for t in titles:
        if t.text != "Back":   
            title_list.append(t.text)

    
    #scrapping to get each image, getting through each hemisphere to search for the image 
    html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')

    image_search = soup.find_all('a', class_="itemLink product-item")
    image_set = []

    for image in image_search:
        if image["href"] != "#":
            image_set.append(image["href"])
    
    unique_set = []
    for i in image_set:
        if i not in unique_set:
            unique_set.append(i)

    
    # Continuation of getting the image links
    hemispheres_urls = []
    for image in unique_set:
        browser.visit("https://marshemispheres.com/" + image)
        sleep(.5)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        images = soup.select('li a')
    
        for image in images:
        
            if image["href"].endswith(".jpg"):
                hemispheres_urls.append(image["href"])


    #forming the image list
    img_list = []
    for links in hemispheres_urls:
        base_mars = "https://marshemispheres.com/"
        img_list.append(base_mars + links)
    
    
    # Forming the title/image dictionaries
    hemisphere_list = []

    full_zip = list(zip(title_list, img_list))

    for title, img_url in full_zip:
        hemisphere_list.append({"title": title, "img_url": img_url})

     # End of hemispheres Scrapping --------------    



    #Make a dictionary to contain all variables to use later in app/html

    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "hemisphere_list": hemisphere_list,
        "table_html": table_html
    }


    # Close the browser after scraping
    browser.quit()

    # Return results from the dictionary variable
    return mars_data
