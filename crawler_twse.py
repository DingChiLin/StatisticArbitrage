from bs4 import BeautifulSoup
import urllib.request as urllib
from selenium import webdriver
from datetime import timedelta, date
import csv

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield (start_date + timedelta(n)).strftime("%Y/%m/%d")[1:]

def get_stock_info(driver, date):
    input_date = driver.find_element_by_name("input_date")
    input_date.clear()
    input_date.send_keys(date)
    input_date.submit()

    soup = BeautifulSoup(driver.page_source, "html.parser")
    try:
        trs = soup.find('div',{'id':'tbl-containerx'}).find('tbody').find_all('tr')
        info = {}
        for tr in trs:
            tds = tr.find_all('td')
            info[tds[0].text] = tds[4].text

        return info
    except:
        return None

def get_stock_codes_and_info(driver, start_date, end_date):
    stock_codes = set()
    stock_info = {}

    for date in daterange(start_date, end_date):
        stock_date_info = get_stock_info(driver, date)

        if stock_date_info:
            for key, _ in stock_date_info.items():
                stock_codes.add(key)

            stock_info[date] = stock_date_info

    stock_codes = sorted(stock_codes)

    return stock_codes, stock_info

def crawler(url, start_date, end_date):
    driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    driver.get(url)

    [stock_codes, stock_info] = get_stock_codes_and_info(driver, start_date, end_date)

    data = []
    data.append(['date'] + stock_codes)
    for date in daterange(start_date, end_date):
        if date not in stock_info:
            continue

        stock_date_info = stock_info[date]
        stock_date_values = []
        stock_date_values.append(date)
        for code in stock_codes:
            if code in stock_date_info:
                stock_date_values.append(stock_date_info[code])
            else:
                stock_date_values.append(None)

        data.append(stock_date_values)

    driver.close()
    return data

def main():
    url = "http://www.twse.com.tw/ch/trading/exchange/BWIBBU/BWIBBU_d.php"
    start_date = date(105, 1, 1)
    end_date = date(106, 1, 6)

    data = crawler(url, start_date, end_date)

    myfile = open('twse_pb_data.csv', 'w')
    wr = csv.writer(myfile)
    wr.writerows(data)

if __name__ == "__main__": main()
