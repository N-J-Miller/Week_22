#!/usr/bin/env python

# Dependencies and modules:

import pandas as pd
import numpy as np
import time
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

# I decided to scrape for local restaurants! (And I endeavor to visit a new one each month!)
# I will tune my code in notebook before running it in VS code or terminal

# function to pull addresses by following the link for every entry.
# running by itself because it was giving me problems
addresses = []
        
# base url with zip code parameter placeholder:
url=f'https://www.yelp.com/search?find_desc=Restaurants&find_loc=62220'

executable_path = {'executable_path':ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=True) 
def locations():
    for page in range(1,51):

        page_url = url + f'&start={page}'
        soup = bs(browser.html, 'html.parser')

        browser.visit(page_url)
        time.sleep(2)
        # I have to follow each restaurant link to get their address:
        browser.links.find_by_partial_href('/biz/').click()
        time.sleep(2)
        loc = soup.find('p', class_='css-qyp8bo')
        if loc is None:
            loc = "Unavailable"
            addresses.append(loc)
        else:
            address = loc.contents[-1].strip()
            addresses.append(address)
            time.sleep(2)
 
    #return addresses

# define a function to scrape my desired items, plus calling location func: 
def scrape_food():
    call_addresses = locations()
    # These are lists for the items I want to scrape:
    call_addresses
    names = []
    pricing = []
    ratings = []
    nreviews = []
    
    # base url with zip code parameter placeholder:
    url=f'https://www.yelp.com/search?find_desc=Restaurants&find_loc=62220'

    executable_path = {'executable_path':ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True) 
    
    # there are 10 entries per page, so I will step my range by 10:
    for page in range(0,50,10):
        
        page_url = url + f'&start={page}'
        browser.visit(page_url)
        soup = bs(browser.html, 'html.parser')
               
        try:
            # Getting the name:
            name_divs = soup.find_all("div", class_="businessName__09f24__EYSZE display--inline-block__09f24__fEDiJ border-color--default__09f24__NPAKY")
            for n in name_divs:
                name = n.find('a', class_='css-1422juy').text
                names.append(name)
           # Check to make sure I'm getting stuff: 
            #print(len(names))
            

            # Price range:
            para = soup.find_all('p', class_='css-1gfe39a')
            for span in para:
                prices = span.find('span', class_='css-1e4fdj9').text
                pricing.append(prices)
            
            #print(len(pricing))
            
            # Rating:
            rating_divs = soup.find_all("div", class_="attribute__09f24__hqUj7 display--inline-block__09f24__fEDiJ margin-r1__09f24__rN_ga border-color--default__09f24__NPAKY")
            for d in rating_divs:
                for x in d:
                    stars = x.div['aria-label']
                    ratings.append(stars)
            
                #print(len(ratings))
            
            # Number of reviews:
            review_divs = soup.find_all("div", class_="attribute__09f24__hqUj7 display--inline-block__09f24__fEDiJ border-color--default__09f24__NPAKY")
            for r in review_divs:
                reviews = r.find('span', class_="reviewCount__09f24__tnBk4 css-1e4fdj9").text
                nreviews.append(reviews)
            
            #print(len(nreviews))            

        except Exception as e:
            print(e)
    
   
    # Let's make a nice dictionary out of our bunch of lists:
    food_scrape_dict = {'Rank':np.arange(1,51,1),
                        'Retaurant Name':names,
                        'Location': addresses,                    
                        'Price Point':pricing, 
                        'Rating':ratings, 
                        'No. of Reviews':nreviews}

    food_scrape_df = pd.DataFrame({k:pd.Series(v) for k,v in food_scrape_dict.items()})
    food_scrape_df.set_index("Rank",inplace=True)
    return food_scrape_df

