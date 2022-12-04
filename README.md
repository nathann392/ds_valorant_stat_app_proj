# Data Science Valorant Stat App: Project Overview 
* Created a tool that retrieves and analyzes the top 500 [Valorant](https://playvalorant.com/en-us/) player statistics to help understand current game balance.
* Individually scraped 500 player profiles from tracker.gg using python, selenium, and concurrent.futures(multithreading)

## Code and Resources Used 
**Python Version:** 3.97
**Packages:** pandas, numpy, streamlit, sklearn, matplotlib, seaborn, selenium, concurrent.futures, BeautifulSoup
**Data Source:**  [tracker.gg](http://tracker.gg/valorant/leaderboard)   
**Multithreaded Scraper Article:** https://betterprogramming.pub/faster-web-scraping-in-python-using-multithreading-496da9eaf0c2

## Web Scraping
Loaded leaderboard webpage with selenium webdriver, pulled player hrefs off the leaderboard, and individually scraped 500 player profiles from tracker.gg using multithreading. With each profile, we got the following:
*	Rank
*	Rating
*	Name
*	Score/Round
*	Damage/Round
*   Kill/Death Ratio
*	Headshot Percentage
*	Win Percentage
*	Top Agents (Agent, Hours Played)
*	Top Weapons (Weapon, Kills, Headshot %)

## EDA
After cleaning data to create separate agent/weapons columns and categorize agent roles, I looked at the distributions of the data and found a few key highlights below.

![alt text](https://github.com/nathann392/ds_valorant_stat_app_proj/blob/main/images/eda/agent_hours.png "Agent Hours")
![alt text](https://github.com/nathann392/ds_valorant_stat_app_proj/blob/main/images/eda/weapon_kills.png "Weapon Kills")
![alt text](https://github.com/nathann392/ds_valorant_stat_app_proj/blob/main/images/eda/role_vs_acs.png "Average Score per Role")

# App
Using streamlit, I created an interactive website to ...
