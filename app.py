from flask import Flask, render_template, request, jsonify 
from scraper import scrape
from urllib.parse import quote_plus, urlparse
import requests
import json

app = Flask(__name__)

#STORE CONVERSION
data = {}

#API CALL TO STORE CONVERSION
def apiConvert():
    global data

    #API SETUP
    url = "https://fixer-fixer-currency-v1.p.rapidapi.com/latest"
    headers = {
    "X-RapidAPI-Host": "fixer-fixer-currency-v1.p.rapidapi.com",
    "X-RapidAPI-Key": "e22598e71fmsh79ab05e94e3b5ffp1d6072jsn9b0382f88b54"
    }
    finalURL = url + '?base=INR&symbols=USD%2CJPY%2CEUR'

    #REQUEST
    resp = requests.get(finalURL, headers = headers)
    data = resp.json()

#API CALL TO GET IMAGE
def apiImage(title):
    #CONVERTING TITLE TO URL FRIENDLY
    title = quote_plus(title)

    #API SETUP
    url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/ImageSearchAPI"
    headers = {
    "X-RapidAPI-Host": "contextualwebsearch-websearch-v1.p.rapidapi.com",
    "X-RapidAPI-Key": "e22598e71fmsh79ab05e94e3b5ffp1d6072jsn9b0382f88b54"
    }
    finalURL = url + '?autoCorrect=false&pageNumber=1&pageSize=1&q=' + title + '&safeSearch=true'

    #REQUEST
    resp = requests.get(finalURL, headers = headers)
    imgResp = resp.json()

    #RETURN URL
    url = imgResp['value'][0]['thumbnail']

    return url


#CONVERSION OF CURRENCIES
def convertCurr(amt):
    global data

    try:
        #CONVERSION
        amt = float(amt)
        usd = round(amt * data['rates']['USD'], 2)
        jpy = round(amt * data['rates']['JPY'], 2)
        eur = round(amt * data['rates']['EUR'], 2)
    except:
        #API ERROR
        print(data)
        usd = jpy = eur = ''
    finally:
        return(usd, jpy, eur)

@app.route('/', host="ibmappendly.herokuapp.com")
def student():
   return render_template('index.html')

@app.route('/result', methods = ['POST', 'GET'], host="ibmappendly.herokuapp.com")
def result():
   if request.method == 'POST':
      #FORM RESULT
      result = request.form['Name']

      #VALIDATE URL
      parsedURL = urlparse(result)
      print(parsedURL.netloc)
      if(parsedURL.netloc != 'www.flipkart.com'):
          return jsonify(warn = 'Enter a valid Flipkart URL')

      #SCRAPE RESULTS
      result = scrape(result)

      #CHECK IF STATUS RETURNS SUCCESS OR PARTIAL SUCCESS
      statusCode = result[0]
      if(statusCode == 201):
          return jsonify(warn = 'Enter a valid Flipkart Product URL')

      #VALUES FROM SCRAPE RESULT
      title = result[1]
      price = result[2]
      rating = result[3]
      value = result[4]
      warranty = result[5]
      CPL = int(price)/int(warranty)
      CPL = int(CPL)

      #API CALLS
      apiConvert()
      imgURL = apiImage(title)

      #CURRENCY CONVERSION
      p = convertCurr(price)
      c = convertCurr(CPL)
      return jsonify(title = title, imgURL = imgURL, price = price, rating = rating, value = value, warranty = warranty, CPL = CPL, pusd = p[0], pyen = p[1], peur = p[2], cusd = c[0], cyen = c[1], ceur = c[2])

if __name__ == '__main__':
    app.run(debug=True)
