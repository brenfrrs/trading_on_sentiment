import re
import tldextract
import pandas as pd
from twelvedata import TDClient
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.tokenize import regexp_tokenize
import nltk
import time
from dateutil.relativedelta import relativedelta

def clean_text(text):
    text.replace("\n"," ")
    text =  ' '.join(re.sub("([^0-9A-Za-z])"," ",text).split())
    return text.lower()


def get_outlet(link):
    '''
    When a URL is passed, this function will return the company name of the entity associated with the URL.
    '''
    res = tldextract.extract(link)
    return res.domain

def get_month_day_range(year):
    '''
    When given a year, returns a list of tuples with the start and end dates for each month of the provided year.
    '''

    ranges = []

    target_year = [(pd.datetime(year,1,1)), (pd.datetime(year,2,1)), (pd.datetime(year,3,1)),
           (pd.datetime(year,4,1)), (pd.datetime(year,5,1)), (pd.datetime(year,6,1)),
           (pd.datetime(year,7,1)), (pd.datetime(year,8,1)), (pd.datetime(year,9,1)),
           (pd.datetime(year,10,1)), (pd.datetime(year,11,1)), (pd.datetime(year,12,1))]

    for date in target_year:
        last_day = date + relativedelta(day=1, months=+1, days=-1)
        first_day = date + relativedelta(day=1)
        ranges.append((first_day.strftime('%Y-%m-%d'), last_day.strftime('%Y-%m-%d')))

    return ranges


def get_past_prices(range, ticker):
    '''
    Input: a list of date tuples in the format (%Y%m%d,%Y%m%d), and the stock ticker symbol.

    Output: a dataframe with the open/close/high/low and volume historical figures related to the provided stock ticker.

    Example: get_past_prices([('2010-12-01', '2010-12-31')], 'AAPL')
    '''

    td = TDClient(apikey="ef26202dacaf412fb157a05403f81ca3")
    times = []

    counter =1

    for start,end in range:
        #delay to prevent API limits.
        time.sleep(20)
        ts = td.time_series(
        symbol=ticker,
        interval="1day",
        start_date=start,
        end_date=end
        ).as_pandas()
        times.append(ts)
        print(str(counter) + ')', str(start) + ' to',end)
        counter +=1

    stock_prices = pd.concat(times)

    print("Final shape: {}".format(stock_prices.shape))
    return stock_prices



analyzer = SentimentIntensityAnalyzer()

def sentiment_analyzer_scores(article):
    '''
    VADER Sentiment used to tag the.
    Returns the predicted labels: positive/negative/neutral.
    Instantiate analyzer before running this function:
    analyzer = SentimentIntensityAnalyzer()
    '''
    global analyzer

    score = analyzer.polarity_scores(article)

    if score['compound'] >= .05:
        sent = 'positive'
    elif score['compound'] <= -.05:
        sent = 'negative'
    else:
        sent = 'neutral'

    return sent

def toke(text):
    '''
    Input: a string value

    Output: A list of tokens extracted from the string.
    '''
    tokens = regexp_tokenize(text, "[\w']+")
    return tokens



def unlist(x):
    return ", ".join(x)


tokenizer = nltk.tokenize.TweetTokenizer()

def tokenize(text):
    return nltk.word_tokenize(text)

lemmatizer = nltk.stem.WordNetLemmatizer()

def lemmatize_text(text):
    '''
    Input: a string value

    Output: The lemmatized words of the passed string.
    '''
     return [lemmatizer.lemmatize(word) for word in text]
