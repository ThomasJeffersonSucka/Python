import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import numpy as np

url = 'https://www.ufc.com/athlete/shamil-abdurakhimov'
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

athlete_stat_numbs = [element.text for element in soup.find_all(class_ = 'athlete-stats__text athlete-stats__stat-numb')]
athlete_stat_labels = [element.text for element in soup.find_all(class_ = 'athlete-stats__text athlete-stats__stat-text')]

if 'knock' in athlete_stat_labels[0]:
    print('a')