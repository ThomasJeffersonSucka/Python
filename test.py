import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import numpy as np
import re


fighter_urls = ['https://www.ufc.com/athlete/hamdy-abdelwahab']

knockouts = []
submissions = []
first_round_finishes = []
striking_accuracy = []
takedown_accuracy = []
fighter_name = []
nickname = []
weight_class = []
record = []

for fighter_url in tqdm(fighter_urls):
    response = requests.get(fighter_url)
    soup = BeautifulSoup(response.text, "html.parser")
    fighter_name_element = soup.find('h1', class_ = 'hero-profile__name').text
    fighter_name.append(fighter_name_element)

    try:
        nickname_element = soup.find('p', class_ = 'hero-profile__nickname').text
        nickname.append(nickname_element)
    except AttributeError:
        nickname.append('None')
        
    try:
        accuracies_labels = [element.text for element in soup.find_all('h2', class_ = "e-t3")]
        accuracies_texts = [element.text for element in soup.find_all('text', 'e-chart-circle__percent')]
        if accuracies_labels:
            for i, label in enumerate(accuracies_labels):
                if "strik" in label.lower():
                    striking_accuracy.append(accuracies_texts[i])
                else:
                    striking_accuracy.append('N/A')
                if "taked" in label.lower():
                    takedown_accuracy.append(accuracies_texts[i])
    except Exception:
        takedown_accuracy.append('N/A')
        striking_accuracy.append('N/A')

    try:
        athlete_stat_labels = [element.text for element in soup.find_all('p', class_ = 'athlete-stats__text athlete-stats__stat-text')]
        athlete_stat_numbs = [element.text for element in soup.find_all('p', class_ = 'athlete-stats__text athlete-stats__stat-numb')]
        labels = [label.lower() for label in athlete_stat_labels]
        if all(any(string in label for label in labels) for string in ["knock", "finish"]):
            for i, label in enumerate(labels):
                if "knock" in label:
                    knockouts.append(athlete_stat_numbs[i])
                else: pass
                if "subm" in label:
                    submissions.append(athlete_stat_numbs[i])
            print('hey')  
                
    except Exception:
        knockouts.append('0')
        submissions.append('0')
        first_round_finishes.append('0')
        
    try:
        record_element = soup.find('p', class_ = 'hero-profile__division-body').text
        record.append(record_element)
    except AttributeError:
        record.append('None')
    
    try:
        weight_class_element = soup.find('p', class_ = 'hero-profile__division-title').text
        weight_class.append(weight_class_element)
    except AttributeError:
        weight_class.append('None')


data = list(zip(fighter_name, nickname, weight_class, record, knockouts, submissions,
 first_round_finishes, striking_accuracy, takedown_accuracy))
df = pd.DataFrame(data, columns=['Fighter Name', 'Nickname', 'Weight Class', 'Record', 'Knockouts', 'Submissions',
 'First Round Finishes', 'Striking Accuracy', 'Takedown Accuracy'])

print(data)

df.to_csv('test.csv', index=False)