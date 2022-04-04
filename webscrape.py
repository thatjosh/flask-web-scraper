import os
import requests
import urllib.parse
#import pandas as pd
#import numpy as np

from cs50 import SQL
from functools import wraps
from bs4 import BeautifulSoup

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///webscrape.db")


""" 1. Web Scraping """
def bswebscrape(html_site):
    # Beautiful soup to webscrape
    web_input = requests.get(html_site)

    if web_input.status_code > 399:
        return 1

    soup = BeautifulSoup(web_input.text, 'lxml')
    contents = soup.find_all('p')

    # Store data in a new list
    scraped_data = []
    for content in contents:
        scraped_data.append(content.text)

    return scraped_data


""" 2. Data Cleaning """
def data_clean(scraped_data):

# Declare dictionary to keep track of words - dict is the fastest
    unique_wordlist = {}
    word_count = 0

    # Data is return in paragraphs
    for paragraphs in scraped_data:

        # Split into lists
        paragraphs = paragraphs.split(" ")

        # Split
        for x in range(len(paragraphs)):

            # Remove punctuation
            paragraphs[x] = paragraphs[x].replace(",", "")
            paragraphs[x] = paragraphs[x].replace(".", "")
            paragraphs[x] = paragraphs[x].replace("!", "")
            paragraphs[x] = paragraphs[x].replace("?", "")
            paragraphs[x] = paragraphs[x].replace("“", "")
            paragraphs[x] = paragraphs[x].replace("”", "")
            paragraphs[x] = paragraphs[x].replace("(", "")
            paragraphs[x] = paragraphs[x].replace(")", "")

        for words in paragraphs:

            # Insert new row
            if words not in unique_wordlist:
                unique_wordlist.update({words: 1})
                word_count += 1

            # Update row count
            else:
                int_increment = int(unique_wordlist[words]) + 1
                unique_wordlist.update({words : int_increment})
                word_count += 1

    return {"WordCount" : word_count, "Data" : unique_wordlist}


""" 4. Update SQL Database """
def webscrapedb_update(unique_wordlist):

    # Update SQL database
    counter = 0
    for word in unique_wordlist:
        counter += 1
        sqlcmd = db.execute("INSERT INTO word_list VALUES (?, ?, ?)", counter, str(word), int(unique_wordlist[word]))
    return 0


""" 5. Delete All Rows in SQL Database """
def webscrapedb_delete():
    sqlcmd = db.execute("DELETE FROM word_list")
    return 0