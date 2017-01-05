from bs4 import BeautifulSoup
import urllib.request as urllib
from selenium import webdriver
from datetime import timedelta, date
import csv

url = "http://www.twse.com.tw/ch/trading/exchange/BWIBBU/BWIBBU_d.php"

#content = urllib.urlopen(url).read()
#soup = BeautifulSoup(content)

#driver = webdriver.Chrome('/usr/local/bin/chromedriver')
#driver.get(url)

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def get_stock_info(date):
    return {'1101':0.1, '1102':0.2, '1103':0.3}
    input_date = driver.find_element_by_name("input_date")
    input_date.clear()
    input_date.send_keys(date)
    input_date.submit()

    soup = BeautifulSoup(driver.page_source)
    try:
        trs = soup.find('div',{'id':'tbl-containerx'}).find('tbody').find_all('tr')
        info = {}
        for tr in trs:
            tds = tr.find_all('td')
            info[tds[0].text] = tds[4].text

        return info
    except:
        return [None, None]

start_date = date(106, 1, 1)
end_date = date(106, 1, 6)

stock_codes = set()
stock_info = {}
for single_date in daterange(start_date, end_date):
    date = single_date.strftime("%Y/%m/%d")
    stock_date_info = get_stock_info(date)

    for key, _ in stock_date_info.items():
        stock_codes.add(int(key))

    stock_info[date] = stock_date_info

    print(stock_info)

sorted(stock_codes)
print(stock_codes)
print(stock_info)

data = []
for single_date in daterange(start_date, end_date):
    date = single_date.strftime("%Y/%m/%d")

    

#driver.close()
