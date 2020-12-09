#!/usr/bin/zsh python

import requests
import pandas as pd
import numpy as np
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import string
import random
import time
from alive_progress import alive_bar
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from selectorlib import Extractor
import os
from datetime import date
import shutil
import json
import warnings
from datetime import date
import twint
import nest_asyncio
nest_asyncio.apply()


#ignore concat warnings for pandas
warnings.simplefilter(action='ignore', category=FutureWarning)
os.environ['WDM_LOG_LEVEL'] = '0'

#the date for twitter search
today = date.today()


#load the main df used for modeling.
main_data = pd.read_csv('test_run.csv', index_col=0)

start_shape = main_data.shape[0]

print('\n')
print('                 Scraping observations from various sources, please be patient... \n')
print('                            ---- {} starting observations ----'.format(start_shape))



symbol = ['AAPL', 'PG', 'V', 'JNJ', 'MRK', 'VZ', 'MCD', 'NKE', 'JPM', 'IBM', 'CSCO', 'TRV', 'HD', 'MSFT', 'HON', 'KO', 'MMM', 'WBA', 'BA', 'INTC', 'AMGN', 'DIS', 'CVX', 'WMT', 'UNH', 'CRM']


# Yahoo Message Boards
print('\n')
print('✔ Gathering data from yahoo message boards..')
print('\n')

final = pd.DataFrame(columns=['username', 'message', 'time_posted', 'datetime', 'ticker','source'])


def yahoo_dicussions(ticker):
    import random
    import time
    import re
    global final
    global main_data
    is_link = 'https://finance.yahoo.com'
    #ChromeOptions = webdriver.ChromeOptions()
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.get(is_link)

    search_bar = driver.find_element_by_xpath('//*[@id="yfin-usr-qry"]')

    search_bar.click()
    search_bar.send_keys('{}'.format(ticker))
    time.sleep(np.random.randint(5,10))
    search_button = driver.find_element_by_xpath('//*[@id="header-desktop-search-button"]').click()

    time.sleep(6)

    forum = driver.find_element_by_xpath('//*[@id="quote-nav"]/ul/li[4]/a').click()


    #click to sort reactions
    time.sleep(np.random.randint(15,20))
    try:
        driver.find_element_by_xpath('//*[@id="canvass-0-CanvassApplet"]/div/div[3]/button').click()

    except NoSuchElementException:
        driver.find_element_by_xpath('//*[@id="canvass-0-CanvassApplet"]/div/div[2]/button').click()


    #click on newest reactions
    try:

        driver.find_element_by_xpath('//*[@id="canvass-0-CanvassApplet"]/div/div[3]/ul/li[2]/button').click()
    except NoSuchElementException:
        driver.find_element_by_xpath('//*[@id="canvass-0-CanvassApplet"]/div/div[2]/ul/li[2]').click()


    #scroll down to load content/ click 'Show More' x amount of times.
    time.sleep(2)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#canvass-0-CanvassApplet > div > button"))).click()

    with alive_bar(10, title='\033[1m{}\033[0m : loading yahoo posts'.format(ticker)) as bar:
        for i in list(range(0,10)):
            try:
                time.sleep(np.random.randint(1,5))
                driver.find_element_by_tag_name('body').send_keys(Keys.END)
                time.sleep(np.random.randint(1,2.5435))
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#canvass-0-CanvassApplet > div > button"))).click()
            except ElementClickInterceptedException:
                time.sleep(np.random.randint(1,3))
                driver.find_element_by_tag_name('body').send_keys(Keys.END)
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="canvass-0-CanvassApplet"]/div/button[2]'))).click()
            except TimeoutException:
                print('No more pages, getting replies.')
                break
            finally:
                pass
            bar()


    # grab the page source code
    html = driver.execute_script('return document.body.innerHTML;')
    time.sleep(1)
    soup = BeautifulSoup(html,'lxml')

    #grab info from the page source code
    mes1 = [entry.text for entry in soup.find_all('div', {'class':'C($c-fuji-grey-l) Mb(2px) Fz(14px) Lh(20px) Pend(8px)'})] #need initial number of messages so we can loop through replies.
    post_time = [entry.text for entry in soup.find_all('span', {'class':'Fz(12px) C(#828c93)'})]
    name = [entry.text for entry in soup.find_all('button', {'class':'D(ib) Fw(b) P(0) Bd(0) M(0) Mend(10px) Fz(16px) Ta(start) C($c-fuji-blue-1-a)'})]

    time.sleep(4)

    with alive_bar((len(mes1)-1), title='\033[1m{}\033[0m : grabbing yahoo posts'.format(ticker)) as bar:
        for i in range(1,len(mes1)):
            try:
                #come back to this line of code to clean it up, this block may never fail and may be able to remove all try/excepts below.
                WebDriverWait(driver, 3.5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="canvass-0-CanvassApplet"]/div/ul/li[{}]'.format(i)))).click()
            except NoSuchElementException:
                try:
                    f = driver.find_element_by_xpath('//*[@id="canvass-0-CanvassApplet"]/div/ul/li[{}]/div/div[5]/div[1]'.format(i))
                    print(f)
                    f.click()
                    print('have to check an alternate item.')

                    try:
                        WebDriverWait(driver, 3.5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="canvass-0-CanvassApplet"]/div/ul/li[{}]/div/div[5]/div[1]'.format(i)))).click()

                    except NoSuchElementException:
                        WebDriverWait(driver, 3.5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="canvass-0-CanvassApplet"]/div/ul/li[{}]/div/div[2]'.format(i)))).click()

                    except TimeoutException:
                        WebDriverWait(driver, 3.5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="canvass-0-CanvassApplet"]/div/ul/li[{}]/div/div[2]/div'.format(i)))).click()

                    finally:
                        pass

                except NoSuchElementException:
                    f = find_element_by_xpath('//*[@id="canvass-0-CanvassApplet"]/div/ul/li[{}]/div/div[2]/div'.format(i))
                    print('alternate item')
                    f.click()

            except ElementClickInterceptedException:
                pass
            except TimeoutException:
                try:
                    #when a post has a bullish/neutral/bearish tag we need to try a few paths.
                    WebDriverWait(driver, 3.5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="canvass-0-CanvassApplet"]/div/ul/li[{}]/div/div[2]'.format(i)))).click()

                except TimeoutException:
                    WebdriverWait(driver, 3.5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="canvass-0-CanvassApplet"]/div/ul/li[{}]/div/div[2]/div').format(i))).click()

                finally:
                    WebdriverWait(driver, 3.5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="canvass-0-CanvassApplet"]/div/ul/li[{}]/div/div[2]/div').format(i))).click()

            except ElementNotInteractableException:

                pass
            finally:
                pass
            bar()

    mes = [entry.text for entry in soup.find_all('div', {'class':'C($c-fuji-grey-l) Mb(2px) Fz(14px) Lh(20px) Pend(8px)'})] #grab all of the messages + replies.
    final_list = list(zip(name, mes, post_time))

    df = pd.DataFrame(final_list, columns=['username', 'message', 'time_posted'])
    df['ticker'] = '{}'.format(ticker)
    df['source'] = 'yahoo'

    # convert the relative posting times ('1 week ago', etc..) to specific datetimes.
    def ago_do_date(ago):
        try:
            value, unit = re.search(r'(\d+) (\w+) ago', ago).groups()
            if not unit.endswith('s'):
                unit += 's'
            delta = relativedelta(**{unit: int(value)})
            return datetime.now() - delta
        except AttributeError:
            yesterday = datetime.today() - timedelta(days=1)
            return yesterday

    df['datetime'] = df['time_posted'].apply(lambda x: ago_do_date(x))

    #remove special chars from posts
    def clean(x):
        s = re.sub(r"[-()\"$#/@;%:<>{}`+=~|.!?,]", "", x)
        return s

    #clean and make every post lowercase.
    df.message = df.message.apply(clean)
    df['message'] = df.message.str.lower()

    final = pd.concat([final, df], ignore_index=True)
    main_data = pd.concat([final, main_data])

    driver.close()


for i in symbol:
    changed_shape =  abs(start_shape - main_data.shape[0])
    yahoo_dicussions(i)
    main_data.drop_duplicates(subset=['message'], inplace=True)
    main_data.to_csv('test_run.csv')
    end_shape =  abs(start_shape - main_data.shape[0])
    print("\033[92m+++ {} observations\033[00m".format(end_shape - changed_shape))



print('\n')
print('                                ---- ending total {} ----'.format(main_data.shape[0]))
print('\n')


#twitter

starting_twitter_shape = main_data.shape[0]

def twint_to_pd(columns):
    return twint.output.panda.Tweets_df[columns]

def column_names():
    return twint.output.panda.Tweets_df.columns

dfs = []

for ticker in symbol:
    today = date.today()
    c = twint.Config()
    c.Search = ticker
    c.Lang = "en"
    c.Pandas = True
    c.Limit = 600
    twint.run.Search(c)
    data = twint_to_pd(['date','tweet', 'username'])
    data['ticker'] = ticker
    data['source'] = 'twitter'
    data.rename(columns = {'tweet':'message', 'created_at':'datetime'}, inplace=True)
    dfs.append(data)

#save all the twitter data to the main df
main_data = pd.concat([main_data, *dfs], sort=True)
main_data.drop_duplicates(subset=['message'], inplace=True)
main_data.to_csv('test_run.csv')

print('\n')
print('starting shape: {}'.format(starting_twitter_shape))
print('main shape: {}'.format(main_data.shape[0]))
print('\033[92m+++ {} observations added\033[00m'.format(main_data.shape[0] - starting_twitter_shape))

print('\n')
