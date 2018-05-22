"""Utility functions."""

import datetime
import feedparser
import hashlib
import json
import justext
import nltk
import requests
import sys
import urllib3

from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import RegexpTokenizer

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def to_bool(value):
    """Take a value and convert it to a boolean type.

    :param value: string or int signifying a bool
    :type value: str
    :returns: converted string to a real bool
    """
    positive = ("yes", "y", "true",  "t", "1")
    if str(value).lower() in positive:
        return True
    negative = ("no",  "n", "false", "f", "0", "0.0", "", "none", "[]", "{}")
    if str(value).lower() in negative:
        return False
    raise Exception('Invalid value for boolean conversion: ' + str(value))


def now_time(str=True):
    """Get the current time and return it back to the app."""
    if str:
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return datetime.datetime.now()


def now_date(str=True):
    """Get the current date and return it back to the app."""
    if str:
        return datetime.date.datetime().strftime("%Y-%m-%d")
    return datetime.datetime.now()


def load_time(str_time):
    """Convert the date string to a real datetime."""
    return datetime.datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S")


def load_date(str_time):
    """Convert the date string to a real datetime."""
    return datetime.datetime.strptime(str_time, "%Y-%m-%d")


def paranoid_clean(query_value):
    """Take a user query value and cleans.

    :param query_value: query value to clean up
    :type query_value: str
    :returns: string a clean value
    """
    if not query_value:
        return ''
    remove = ['{', '}', '<', '>', '"', "'", ";"]
    for item in remove:
        query_value = query_value.replace(item, '')
    query_value = query_value.rstrip().lstrip().strip()
    return query_value


def derive_source(url):
    """Derive the source of data from the URL."""
    parts = url.split('/')
    return '//'.join([parts[0], parts[2]])


def get_page_content(url):
    """Get the HTML content from the URL."""
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'https://' + url
    try:
        response = requests.get(url, verify=False)
    except Exception as e:
        print(e)
        return None
    return response.content


def get_tokens(text):
    """Tokenize the input text."""
    soup = BeautifulSoup(text, "html.parser")
    tokenizer = RegexpTokenizer(r'\w+')
    return tokenizer.tokenize(soup.get_text())


def cleaned_tokens(tokens):
    """Clean the tokens by removing stop words and stemming."""
    # stemmer = SnowballStemmer("english")
    # stemmed = [stemmer.stem(token) for token in tokens]
    s = set(stopwords.words('english'))
    tokens = [x.lower() for x in tokens if not x.isdigit()]
    return filter(lambda w: not w.lower() in s, tokens)


def get_sentiment(text):
    """Estimate the sentiment of text."""
    url = "http://text-processing.com/api/sentiment/"
    response = requests.post(url, data={'text': text})
    if response.status_code != 200:
        return "UNKNOWN"
    try:
        loaded = json.loads(response.content)
    except Exception as e:
        return "UNKNOWN"
    if loaded['label'] == 'pos':
        return "POSITIVE"
    elif loaded['label'] == 'neg':
        return "NEGATIVE"
    return "NEUTRAL"


def strip_google(url):
    """Remove the Google tracking on links."""
    url = url.replace('https://', '', 1).split('/')
    url.pop(0)
    url = '/'.join(url)
    start = url.find('url=') + 4  # Handles the offset of the locater
    end = url.find('&ct=')
    return url[start:end]
