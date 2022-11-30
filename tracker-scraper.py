from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import concurrent.futures
from bs4 import BeautifulSoup

#---------------------------------#
# Global variables

cols = ['rank', 'rating', 'name', 'score/round', 'damage/round', 'k/d_ratio', 'hs_percentage(%)', 'win_percentage(%)', 'top_agents(agent, hours)', 'top_weapons(weapon, kills, hs%)']
df = pd.DataFrame(columns=cols)
url = "https://tracker.gg"
leaderboard_refs = ["/valorant/leaderboards/ranked/all/default?page=1&region=na",
                    "/valorant/leaderboards/ranked/all/default?page=2&region=na",
                    "/valorant/leaderboards/ranked/all/default?page=3&region=na",
                    "/valorant/leaderboards/ranked/all/default?page=4&region=na",
                    "/valorant/leaderboards/ranked/all/default?page=5&region=na"]

#---------------------------------#
# Selenium webdriver

def load_page_via_webdriver(url, output = ("", False)):
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

    if output[1] == True:
        with open("{0}.html".format(output[0]), "w", encoding="utf-8") as f:
            f.write(str(soup.prettify()))

    return soup

#---------------------------------#
# Get all player data from soup

def get_player_refs(soup):      
    players = []
    usernames = soup.find_all("td", class_="username")
    
    for username in usernames:
        user_url = username.div.a['href']
        players.append(user_url)        

    return players

def get_player_data(player_soup):
    name = get_name(player_soup)
    rr = get_rr(player_soup)
    rank = get_rank(player_soup)
    score = get_stat(player_soup, "Score/Round")
    dmg = get_stat(player_soup, "Damage/Round") 
    kd = get_stat(player_soup, "K/D Ratio")
    hs = get_stat(player_soup, "Headshot%")
    win = get_stat(player_soup, "Win %")
    agents = get_top_agents(player_soup)
    weapons = get_top_weapons(player_soup)

    row = pd.Series({'rank': rank, 'rating': rr, 'name': name, 'score/round': score, 'damage/round': dmg, 'k/d_ratio': kd, 'hs_percentage(%)': hs, 'win_percentage(%)': win, 'top_agents(agent, hours)': agents, 'top_weapons(weapon, kills, hs%)': weapons})

    return row

def get_rank(player_soup):
    rank_soup = player_soup.find("div", class_= "subtext")
    rank = rank_soup.get_text().replace("#","").strip()
    return rank

def get_rr(player_soup):
    rr_soup = player_soup.find("span", class_= "mmr")
    rr = rr_soup.get_text().replace(",","").replace("RR","").strip()
    return rr

def get_name(player_soup):
    name = player_soup.find("span", class_= "trn-ign__username")
    hashtag = player_soup.find("span", class_= "trn-ign__discriminator")
    return name.get_text().strip() + hashtag.get_text().strip()

def get_stat(player_soup, html_title):
    soup = player_soup.find("span", title=html_title)
    stat = soup.find_next_sibling("span").get_text().replace("%","").strip() 
    return stat

def get_top_agents1(player_soup):
    agents = []
    soups = player_soup.find_all("div", "st-content__item")
    for soup in soups:
        agent_soup = soup.find("div", class_="value")
        agent = agent_soup.get_text().strip()
        agents.append(agent)

    return agents

def get_top_agents(player_soup):
    agents = []
    soups = player_soup.find_all("div", "st-content__item")
    for soup in soups:
        agent_soup = soup.find_all("div", class_="value")
        agent = agent_soup[0].get_text().strip()
        hours = agent_soup[1].get_text().replace("hrs","").strip()
        agents.append([agent, hours])

    return agents   

def get_top_weapons(player_soup):
    weapons = []
    weapon_soup = player_soup.find_all("div", class_= "weapon__name")
    weapon_kill_soup = player_soup.find_all("div", class_= "weapon__main-stat")
    weapon_hs_soup = player_soup.find_all("div", class_="weapon__accuracy-hits")
    
    for i in range(3):
        res = []
        res.append(weapon_soup[i].get_text().strip())
        res.append(weapon_kill_soup[i].find("span", class_="value").get_text().strip())
        res.append(weapon_hs_soup[i].contents[0].get_text().replace("%","").strip())
        weapons.append(res)

    return weapons

#---------------------------------#
# Threading function

def load_player_data(ref):
    global df
    player_soup = load_page_via_webdriver("https://tracker.gg" + ref)
    player_data = get_player_data(player_soup)
    df = pd.concat([df, player_data.to_frame().T], ignore_index=True)

#---------------------------------#

def clean_df():
    global df    
    df['rank'] = df['rank'].astype(int)
    df['rating'] = df['rating'].astype(int)
    df['score/round'] = df['score/round'].astype(float)
    df['damage/round'] = df['damage/round'].astype(float)
    df['k/d_ratio'] = df['k/d_ratio'].astype(float)
    df['hs_percentage(%)'] = df['hs_percentage(%)'].astype(float)
    df['win_percentage(%)'] = df['win_percentage(%)'].astype(float)
    df = df.sort_values(by=['rank'])

def run_scraper():
    global df

    soups = []
    player_refs = []

    # Load each page of 100 players for 5 total pages
    for ref in leaderboard_refs:
        soups.append(load_page_via_webdriver(url + ref))

    # Compile all player refs of 500 players into one list
    for soup in soups:
        player_refs.append(get_player_refs(soup))

    player_refs = [item for sublist in player_refs for item in sublist]

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(load_player_data, player_refs)

    clean_df()

    df.to_csv("combined_player_data.csv", encoding='utf-8', index=False)
    