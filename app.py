import streamlit as st
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import base64
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import json
import time
import sys
 
#st.set_page_config(layout='wide')

#st.title('App')
#st.markdown('This app retrieves statistical data from the ____')


# Web scraping
def load_webdriver(name, url, output = False):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('log-level=3')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.minimize_window()
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'title')))

    soup = BeautifulSoup(driver.page_source, features="html.parser")

    if output == True:
        with open("{0}.html".format(name), "w", encoding="utf-8") as f:
            f.write(str(soup.prettify()))

    return soup

# TODO: Run webdriver for top 100 players
def load_player(soup):   
    usernames = soup.find_all("td", class_="username")

    for index, username in enumerate(usernames):
        user_url = username.div.a['href']
        print(str(index + 1) + " " + user_url)

# TODO: View top 3 agents, vandal/phantom

def main():
    leaderboard_url = "https://tracker.gg/valorant/leaderboards/ranked/all/default?page=1&region=na"

    soup = load_webdriver("leaderboard", leaderboard_url, output=True)

    load_player(soup)

if __name__ == "__main__":
    main()