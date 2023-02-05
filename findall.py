import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import numpy as np

fighter_urls = ['https://www.ufc.com/athlete/shamil-abdurakhimov']
for url in fighter_urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    numbers = [element.text for element in soup.find_all('div', class_ = 'c-stat-compare__number')]
    sig_strikes_by_position_and_win_methods = [element.text.strip().replace("\n", "").replace(" ", "") for element in soup.find_all('div', class_ = 'c-stat-3bar__value')]
    print(sig_strikes_by_position_and_win_methods[5])
  

    sig_strikes_head_total = (soup.find('text', id = 'e-stat-body_x5F__x5F_head_value').text)
    print(sig_strikes_head_total)