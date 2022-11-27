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
@st.cache
def load_data():
    url = "https://tracker.gg/valorant/profile/riot/reach%23lavi/overview"

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

    with open("output.txt", "w") as f:
        print(soup.prettify(), file=f)

load_data()