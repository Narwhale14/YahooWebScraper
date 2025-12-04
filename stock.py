#!/usr/bin/env python3 
#   If needed run
#       sudo apt install python3-pip
#       pip3 install requests beautifulsoup4

import sys
import os
import requests
from datetime import datetime
from bs4 import BeautifulSoup

def scraper(symbols):
    # request URL bypassing script detector
    URL = "https://finance.yahoo.com/markets/world-indices/"
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    page = requests.get(URL, headers=headers)

    # load HTML content and find all rows that contain stock info
    soup = BeautifulSoup(page.content, "html.parser")
    rows = soup.find_all("tr", class_="row")

    for symbol in symbols: # loop through user inputted stock symbols
        symbol = symbol.upper()
        for row in rows: # loop through all rows
            _symbol = row.find("span", class_="symbol").get_text(strip=True)[1:]

            if _symbol == symbol: # if on correct stock
                _name = row.find("div", class_="companyName").get_text(strip=True)
                _price = row.find("fin-streamer", attrs={"data-field": "regularMarketPrice"}).get_text(strip=True)
                _time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
                filename = _symbol + "_" + _time + ".txt"
                export(filename, [_symbol, _name, _price, _time])

def export(fname, elements):
    # create .finance dir if it doesn't exist
    dir = ".finance"
    if not os.path.exists(dir):
        os.makedirs(dir)

    # print default price
    print(elements[0])
    print("Current price is $" + elements[2])

    # remove previous record of stock
    for file in os.listdir(dir):
        if file.startswith(elements[0]):
            file_path = os.path.join(dir, file)

            # get the previous price
            with open(file_path, 'r') as r:
                price_old = r.read().strip()
            diff = float(elements[2].replace(',', '')) - float(price_old.replace(',', ''))

            outcome = "increased by $" + str(round(diff, 2))
            if(diff < 0):
                outcome = "decreased by $" + str(round(diff, 2))
            elif (diff == 0):
                outcome = "has not changed"

            print("The old price was $" + price_old)
            print("Price " + outcome + " since you last checked on " + elements[3].replace('_', ' '))

            # remove old file
            os.remove(file_path)
            break

    print()

    # write to file
    with open(os.path.join(dir, fname), 'w') as w:
        w.write(elements[2])

# main
if __name__ == "__main__":
    if len(sys.argv) < 2: # print program usage if needed
        print("Usage: ./stock.py {SYMBOL ...}")
        sys.exit(1)

    # removes executable call argument and sends all stock symbols to scraper
    symbols = sys.argv[1:]
    scraper(symbols)