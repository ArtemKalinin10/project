import time
import datetime
import sqlite3 as sq
from selenium import webdriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent


#Currency rates that are tracked
values = ['AED', 'AMD', 'AUD', 'AZN', 'BGN', 'BYN', 'CAD', 'CHF', 'CNY', 'CZK', 'DKK', 'EUR', 'GBP',
          'HKD', 'HUF', 'INR', 'JPY', 'KGS', 'KRW', 'KZT', 'MDL', 'NOK', 'PLN', 'SEK', 'SGD', 'THB',
          'TJS', 'TRY', 'USD', 'ZAR']


#parser function
def parser(values):
    global responce
    
    useragent = UserAgent().random
    #options
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument(f'user-agent={useragent}')
    #driver
    driver = webdriver.Chrome(options=options)
    values_buy_sell = []
    
    for i in values:
        url = f'https://www.xe.com/currencyconverter/convert/?Amount=1&From={i}&To=RUB'
        try:
            driver.get(url=url)
            time.sleep(0.5)
            exchange_rate = driver.find_element(By.XPATH, '//*[@id="__next"]/div[4]/div[2]/section/div[2]/div/main/div/div[2]/div[1]/div/p[2]').text.rstrip(' Russian Rubles')
            values_buy_sell.append({'currency': i, 'exchange_rate': round(float(exchange_rate), 6)})
        except Exception as e:
            print(url)
    date = datetime.datetime.now()
    responce = {str(date)[:-10]: values_buy_sell}


#function for writing data to the database
def data_baze(responce):
    with sq.connect('date_base.db') as con:
        cur = con.cursor()
        cur.execute(f"""CREATE TABLE IF NOT EXISTS '{list(responce.keys())[0]}' (
            currency TEXT,
            exchange_rate REAL)""")
        for i in responce[list(responce.keys())[0]]:
            cur.execute(f"""INSERT INTO '{list(responce.keys())[0]}' (currency, exchange_rate) VALUES ('{i['currency']}', {i['exchange_rate']})""")

#main function         
def main():
    cnt = 1
    while True:
        print(f'[{cnt}] Starting parsing')
        parser(values)
        data_baze(responce)
        print(f'[{cnt}] Success')
        time.sleep(121)
        cnt += 1

if __name__ == '__main__':
    main()
