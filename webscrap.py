# Import packages
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

def get_reviews(url):
# Header to set the requests as a browser requests
    def getRandomProxy():
        # Using Proxy 
        headers = {
        'authority': 'www.amazon.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9,bn;q=0.8',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
    }
        return headers

    # URL of The amazon Review page
    productUrl = url
    reviews_url = productUrl.replace("dp", "product-reviews") + "?pageNumber=" + str(1)

    def totalPages(productUrl):
        resp = requests.get(productUrl, headers= getRandomProxy())
        soup = BeautifulSoup(resp.text, 'html.parser')
        reviews = soup.find('div', {'data-hook':"cr-filter-info-review-rating-count"})
        return (int(reviews.text.strip().split(', ')[1].split(" ")[0].replace(',' , ''))//10) + 1

    try:
        len_page = totalPages(reviews_url)
    except Exception as e:
        len_page = 0
    ### <font color="red">Functions</font>

    # Extra Data as Html object from amazon Review page
    def reviewsHtml(url, len_page):
        
        # Empty List define to store all pages html data
        soups = []
        
        # Loop for gather all 3000 reviews from 300 pages via range
        for page_no in range(1, len_page + 1):
            
            # parameter set as page no to the requests body
            params = {
                'ie': 'UTF8',
                'reviewerType': 'all_reviews',
                'filterByStar': 'critical',
                'pageNumber': page_no,
            }
            
            # Request make for each page
            response = requests.get(url, headers=getRandomProxy())
            
            # Save Html object by using BeautifulSoup4 and lxml parser
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Add single Html page data in master soups list
            soups.append(soup)
            
        return soups

    # Grab Reviews name, description, date, stars, title from HTML
    def getReviews(html_data):

        # Create Empty list to Hold all data
        data_dicts = []
        
        # Select all Reviews BOX html using css selector
        boxes = html_data.select('div[data-hook="review"]')
        
        # Iterate all Reviews BOX 
        for box in boxes:

            try:
                description = box.select_one('[data-hook="review-body"]').text.strip()
            except Exception as e:
                description = 'N/A'

            # create Dictionary with al review data 
            data_dict = {
                'Reviews' : description
            }

            # Add Dictionary in master empty List
            data_dicts.append(data_dict)
        
        return data_dicts

    # Grab all HTML
    html_datas = reviewsHtml(reviews_url, len_page)

    # Empty List to Hold all reviews data
    reviews = []

    # Iterate all Html page 
    for html_data in html_datas:
        
        # Grab review data
        review = getReviews(html_data)
        
        # add review data in reviews empty list
        reviews += review

    # Create a dataframe with reviews Data
    df_reviews = pd.DataFrame(reviews)
    return df_reviews