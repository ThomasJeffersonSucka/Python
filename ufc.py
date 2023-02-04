import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import numpy as np

first_url = 'https://www.ufc.com/athletes/all?gender=All&search=&page='

page_urls = []
for page in range(0, 253):
    url = first_url + str(page)
    page_urls.append(url)

fighter_urls = []
ufc_url = 'https://ufc.com'
for url in page_urls[:1]:
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
fighter_name = []
nickname = []
weight_class = []
record = []

for fighter_url in tqdm(fighter_urls):
    response = requests.get(fighter_url)
    soup = BeautifulSoup(response.text, "html.parser")
    athlete_stat_numbs = [element.text for element in soup.find_all('p', class_ = 'athlete-stats__text athlete-stats__stat-numb')]
    athlete_stat_labels = [element.text for element in soup.find_all('p', class_ = 'athlete-stats__text athlete-stats__stat-text')]
    accuracies_labels = [element.text for element in soup.find_all('h2', class_ = "e-t3")]
    accuracies_texts = [element.text for element in soup.find_all('text', 'e-chart-circle__percent')]
    fighter_name_element = soup.find('h1', class_ = 'hero-profile__name').text

    fighter_name.append(fighter_name_element)
    print(fighter_name_element)

    try:
        nickname_element = soup.find('p', class_ = 'hero-profile__nickname').text
        nickname.append(nickname_element)
        print(nickname_element)
    except AttributeError:
        nickname.append('None')
        print('none')
        
    if athlete_stat_numbs:
        for i, label in enumerate(accuracies_labels):
            if "strik" in label.lower():
                striking_accuracy.append(accuracies_texts[i])
                print(accuracies_texts[i])
            else:
                print('N/A')
                striking_accuracy.append('N/A')
    else:
        striking_accuracy.append('N/A')
        print('N/A')

    if athlete_stat_labels:
        for i, label in enumerate(athlete_stat_labels):
            if "taked" in label.lower():
                knockouts.append(athlete_stat_numbs[i])
                print(athlete_stat_numbs[i])
            else: 
                takedown_accuracy.append('N/A')
                print('N/A')

    else:
        takedown_accuracy.append('N/A')
        print('N/A')

    if athlete_stat_labels:
        for i, label in enumerate(athlete_stat_labels):
            label = label.lower()
            if "knock" in label:
                knockouts.append(athlete_stat_numbs[i])
            else:
                knockouts.append('0')

            if "subm" in label:
                submissions.append(athlete_stat_numbs[i])
            else:
                submissions.append('0')

            if "finish" in label:
                first_round_finishes.append(athlete_stat_numbs[i])
            else:
                first_round_finishes.append('0')
    else:
        knockouts.append('0')
        submissions.append('0')
        first_round_finishes.append('0')

        
    try:
        record_element = soup.find('p', class_ = 'hero-profile__division-body').text
        record.append(record_element)
        print(record_element)
    except AttributeError:
        record.append('None')
    
    try:
        weight_class_element = soup.find('p', class_ = 'hero-profile__division-title').text
        weight_class.append(weight_class_element)
        print(weight_class_element)
    except AttributeError:
        weight_class.append('None')


data = list(zip(fighter_name, nickname, weight_class, record, knockouts, submissions,
 first_round_finishes, striking_accuracy, takedown_accuracy))
df = pd.DataFrame(data, columns=['Fighter Name', 'Nickname', 'Weight Class', 'Record', 'Knockouts', 'Submissions',
 'First Round Finishes', 'Striking Accuracy', 'Takedown Accuracy'])

print(data)

df.to_csv('test.csv', index=False)