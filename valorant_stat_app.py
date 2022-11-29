import tracker_scraper as ts
import pandas as pd
import streamlit as st
from PIL import Image
import base64
import matplotlib.pyplot as plt
import time
import sys

#---------------------------------#


#---------------------------------#
# Main

def main():
    # ts.run_scraper()
    df = pd.read_csv('combined_player_data.csv')
    
    
if __name__ == "__main__":
    main()