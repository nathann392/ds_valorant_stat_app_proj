import tracker_scraper as ts
import pandas as pd
import streamlit as st
from PIL import Image
import base64
import matplotlib.pyplot as plt
import time
import sys

#ts.run_scraper()
df = pd.read_csv('player_data1.csv')

image = Image.open('./images/logo.jpg')
st.image(image, width = 500)

st.title('Valorant Stat App')
st.markdown("""
This app retrieves and analyzes the top 500 Valorant players from the **tracker.gg**!
""")

expander_bar = st.expander("About")
expander_bar.markdown("""
* **Python libraries:** pandas, numpy, streamlit, sklearn, matplotlib, seaborn, selenium, concurrent.futures, BeautifulSoup
* **Data source:** [tracker.gg](http://tracker.gg/valorant/leaderboard)
""")