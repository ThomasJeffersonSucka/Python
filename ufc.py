import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import numpy as np

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
striking_accuracy = []
takedown_accuracy = []


for fighter_url in fighter_urls:
    response = requests.get(fighter_url)
    soup = BeautifulSoup(response.text, "html.parser")
    athlete_stat_numbs = [element.text for element in soup.find_all(class_ = 'athlete-stats__text athlete-stats__stat-numb')]
    athlete_stat_labels = [element.text for element in soup.find_all(class_ = 'athlete-stats__text athlete-stats__stat-text')]
    accuracies_labels = [element.text for element in soup.find_all(class_ = "e-t3")]
    accuracies_texts = [element.text for element in soup.find_all('e-chart-circle__percent')]
    if len(athlete_stat_numbs) == 3:
        knockouts.append(athlete_stat_numbs[0])
        submissions.append(athlete_stat_numbs[1])
        first_round_finishes.append(athlete_stat_numbs[2])
        print(athlete_stat_numbs[0])
        print(athlete_stat_numbs[1])
        print(athlete_stat_numbs[2])
    elif 'knock' in  athlete_stat_labels[0] and 'subm' in athlete_stat_labels[1]:
        knockouts.append(athlete_stat_numbs[0])
        submissions.append(athlete_stat_numbs[1])
    elif 'knock' in  athlete_stat_labels[0] and 'finish' in athlete_stat_labels[1]:
        knockouts.append(athlete_stat_numbs[0])
        first_round_finishes.append(athlete_stat_numbs[0])
    elif 'subm' in  athlete_stat_labels[0] and 'finish' in athlete_stat_labels[1]:
        submissions.append(athlete_stat_numbs[0])
        first_round_finishes.append(athlete_stat_numbs[0])
    elif 'knock' in  athlete_stat_labels[0].te:
        knockouts.append(athlete_stat_numbs[0])
    elif 'subm' in athlete_stat_labels[0]:
        submissions.append(athlete_stat_numbs[0])
    elif 'finish' in athlete_stat_labels[0]:
        first_round_finishes.append(athlete_stat_numbs[0])
    else: continue
    if 'strik' in accuracies_labels[0] and 'taked' in accuracies_labels[0]:
        striking_accuracy.append(accuracies_texts[0])
        takedown_accuracy.append(accuracies_texts[0])
    elif 'strik' in accuracies_labels[0]:
        striking_accuracy.append(accuracies_texts[0])
    elif 'taked' in accuracies_labels[0]:
        takedown_accuracy.append(accuracies_texts[0])
    else: continue

master_array = np.concatenate(knockouts, submissions, first_round_finishes, striking_accuracy, takedown_accuracy)
print(master_array)