import streamlit as st
from PIL import Image
import pandas as pd
import base64
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import json
import time
 
st.set_page_config(layout='wide')

st.title('Price App')
st.markdown('This app retrieves statistical data from the ____')