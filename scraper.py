import requests
from bs4 import BeautifulSoup
import re
import argparse

# RETURNS: TITLE OF PRODUCT, PRICE, TOTAL RATING, VALUE FOR MONEY RATING, WARRANTY IN MONTHS
# STATUS CODES
# 200 - SUCCESSFULL
# 201 - SCRAPE ERROR (POSSIBLY WRONG URL)
# 202 - PARTIAL SCRAPE ERROR
def scrape(url):
    r = requests.get(url)

    content = BeautifulSoup(r.text, 'html.parser')

    #INIT STATUS CODE
    statusCode = 200

    #CLASS EXTRACTION
    titleClass = content.find('span', {'class': '_35KyD6'})
    priceClass = content.find(class_ = '_1vC4OE _3qQ9m1')
    ratingClass = content.find(class_ = '_1i0wk8')
    vfmClass = content.find(class_ = 'PRNS4f')
    warrantyClass = content.find(class_ = '_3h7IGd')

    #INIT VALUES TO BE EXTRACTED
    title = ''
    price = ''
    rating = ''
    vfm = ''
    warranty = None

    #VALUE EXTRACTION
    try:
        title = titleClass.contents[0]
        price = re.sub('[^0-9\.]', '', priceClass.contents[0])
        rating = re.sub('[^0-9\.]', '', ratingClass.contents[0])
        if(vfmClass is not None):
            vfm = re.sub('[^0-9\.]', '', vfmClass.contents[0])
        else:
            statusCode = 202
        war = warrantyClass.contents[0].split()
        for i in range(len(war)):
            if war[i].isnumeric():
                if war[i + 1] == 'Year':
                    warranty = int(war[i]) * 12
                else:
                    warranty = int(war[i])
                break
    except:
        statusCode = 201
        return (statusCode, title, price, rating, vfm, warranty)


    #OUTPUT: STATUS CODE, TITLE OF PRODUCT, PRICE, TOTAL RATING, VALUE FOR MONEY RATING, WARRANTY IN MONTHS
    return (statusCode, title, price, rating, vfm, warranty)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Flipkart Value Scraper')
    parser.add_argument('url', type = str, help = 'Flipkart product link')
    args = parser.parse_args()

    print(scrape(args.url.split('?')[0]))
