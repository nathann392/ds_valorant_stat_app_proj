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

#---------------------------------#
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

def get_player_refs(soup):      
    players = []
    usernames = soup.find_all("td", class_="username")
    
    for index, username in enumerate(usernames):
        user_url = username.div.a['href']
        players.append(user_url)        
        print(str(index + 1) + " " + user_url)

    return players

#---------------------------------#
# Get player information

def get_player_data(player_soup):
    print(get_name(player_soup))
    print(get_rr(player_soup))
    print(get_rank(player_soup))
    print(get_stat(player_soup, "Score/Round"))
    print(get_stat(player_soup, "Damage/Round"))    
    print(get_stat(player_soup, "K/D Ratio"))
    print(get_stat(player_soup, "Headshot%"))
    print(get_stat(player_soup, "Win %"))
    print(get_top_agents(player_soup))
    print(get_top_weapons(player_soup))
    print(get_top_weapon_hs(player_soup))


def get_rank(player_soup):
    rank_soup = player_soup.find("div", class_= "subtext")
    rank = rank_soup.get_text().strip().replace("#","")
    return rank

def get_rr(player_soup):
    rr_soup = player_soup.find("span", class_= "mmr")
    rr = rr_soup.get_text().strip().replace(",","").replace("RR","")
    return int(rr)

def get_name(player_soup):
    name = player_soup.find("span", class_= "trn-ign__username")
    hashtag = player_soup.find("span", class_= "trn-ign__discriminator")
    return name.get_text().strip() + hashtag.get_text().strip()

def get_stat(player_soup, html_title):
    soup = player_soup.find("span", title=html_title)
    stat = soup.find_next_sibling("span").get_text().strip().replace("%","")    
    return stat

def get_top_agents(player_soup):
    agents = []
    soups = player_soup.find_all("div", "st-content__item")
    for soup in soups:
        agent_soup = soup.find("div", class_="value")
        agent = agent_soup.get_text().strip()
        agents.append(agent)

    return agents


def get_top_weapons(player_soup):
    weapons = []
    weapon_soup = player_soup.find_all("div", class_= "weapon__name")
    for weapon in weapon_soup:
        weapons.append(weapon.get_text().strip())

    return weapons


def get_top_weapon_hs(player_soup):
    weapon_hs_soup = player_soup.find("div", class_="weapon__accuracy-hits")
    weapon_hs =  weapon_hs_soup.contents[0].get_text().strip().replace("%","") 
    return weapon_hs


#---------------------------------#
# Main

url = "https://tracker.gg"
leaderboard_ref = "/valorant/leaderboards/ranked/all/default?page=1&region=na"

cols = ['rank', 'rating', 'name', 'score/round', 'damage/round', 'k/d_ratio', 'hs_percentage(%)', 'win_percentage(%)', 'top_3_agents', 'top_weapon', 'top_weapon_hs_percentage(%)']
df = pd.DataFrame(columns=cols)

def main():

    soup = load_webdriver("leaderboard", url + leaderboard_ref, output=True)
    player_refs = get_player_refs(soup)   

    # TODO: Set up multithread 
    one = load_webdriver("player1", url + player_refs[0], output=True)

    get_player_data(one)

if __name__ == "__main__":
    main()