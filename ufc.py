import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

first_url = 'https://www.ufc.com/athletes/all?gender=All&search=&page='

page_urls = []
for page in range(1, 254):
    url = first_url + str(page)
    page_urls.append(url)

fighter_urls = []
ufc_url = 'https://ufc.com'
for url in tqdm(page_urls):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    hrefs = soup.find_all('a', class_ = 'e-button--black')
    for href in hrefs:
        second_link = href['href']
        fighter_url = ufc_url + second_link
        fighter_urls.append(fighter_url)

knockouts = []
submissions = []
first_round_finishes = []


for fighter_url in fighter_urls:
    response = requests.get(fighter_url)
    soup = BeautifulSoup(response.text, "html.parser")
    athlete_stat_numbs = soup.find_all(class_ = 'athlete-stats__text athlete-stats__stat-numb')
    athlete_stat_label = soup.find_all(class_ = 'athlete-stats__text athlete-stats__stat-text')
    if len(athlete_stat_numbs) == 3:
        knockouts.append(athlete_stat_numbs[0].text)
        submissions.append(athlete_stat_numbs[1].text)
        first_round_finishes.append(athlete_stat_numbs[2].text)
        print(athlete_stat_numbs[0].text)
        print(athlete_stat_numbs[1].text)
        print(athlete_stat_numbs[2].text)
    elif 'knock' in  athlete_stat_label[0].text and 'subm' in athlete_stat_label[1].text:
        knockouts.append(athlete_stat_numbs[0].text)
        submissions.append(athlete_stat_numbs[1].text)
    elif 'knock' in  athlete_stat_label[0].text and 'finish' in athlete_stat_label[1].text:
        knockouts.append(athlete_stat_numbs[0].text)
        first_round_finishes.append(athlete_stat_numbs[1].text)
    elif 'subm' in  athlete_stat_label[0].text and 'finish' in athlete_stat_label[1].text:
        submissions.append(athlete_stat_numbs[0].text)
        first_round_finishes.append(athlete_stat_numbs[1].text)
    elif 'knock' in  athlete_stat_label[0].text:
        knockouts.append(athlete_stat_numbs[0].text)
    elif 'subm' in athlete_stat_label[0].text:
        submissions.append(athlete_stat_numbs[0].text)
    elif 'finish' in athlete_stat_label[0].text:
        first_round_finishes.append(athlete_stat_numbs[0].text)
    else:
        continue
        

