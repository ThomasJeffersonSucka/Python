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
    print(fighter_url)

knockouts = ['0'] * len(fighter_urls)
submissions = ['0'] * len(fighter_urls)
first_round_finishes = ['0'] * len(fighter_urls)
striking_accuracy = ['N/A'] * len(fighter_urls)
takedown_accuracy = ['N/A'] * len(fighter_urls)
fighter_name = []
nickname = ['None'] * len(fighter_urls)
weight_class = ['0'] * len(fighter_urls)
record = ['0'] * len(fighter_urls)

for fighter_url in tqdm(fighter_urls):
    response = requests.get(fighter_url)
    soup = BeautifulSoup(response.text, "html.parser")
    athlete_stat_numbs = [element.text for element in soup.find_all('p', class_ = 'athlete-stats__text athlete-stats__stat-numb')]
    athlete_stat_labels = [element.text for element in soup.find_all('p', class_ = 'athlete-stats__text athlete-stats__stat-text')]
    accuracies_labels = [element.text for element in soup.find_all('h2', class_ = "e-t3")]
    accuracies_texts = [element.text for element in soup.find_all('text', 'e-chart-circle__percent')]
    fighter_name_element = soup.find('h1', class_ = 'hero-profile__name').text
        
    for i, athlete_stat_label in enumerate(athlete_stat_labels):
        if 'knock' in athlete_stat_label:
            knockouts[i] = athlete_stat_numbs[i]
        elif 'subm' in athlete_stat_label:
            submissions[i] = athlete_stat_numbs[i]
        elif 'finish' in athlete_stat_label:
            first_round_finishes[i] = athlete_stat_numbs[i]
        else:
            knockouts.append('0')
            submissions.append('0')
            first_round_finishes.append('0')
     
    fighter_name.append(fighter_name_element)
    try:
        record_element = soup.find('p', class_ = 'hero-profile__division-body').text
        record.append(record_element)
    except AttributeError:
        record.append('None')

    try:
        record_element = soup.find('p', class_ = 'hero-profile__nickname').text
        nickname.append(record_element)
    except AttributeError:
        nickname.append('None')
    
    try:
        weight_class_element = soup.find('p', class_ = 'hero-profile__division-title').text
        weight_class.append(weight_class_element)
    except AttributeError:
        weight_class.append('None')

    for i, athlete_stat_label in enumerate(athlete_stat_labels):
        if 'strik' in athlete_stat_label:
            striking_accuracy.append(athlete_stat_numbs[i])
        elif 'taked' in athlete_stat_label:
            takedown_accuracy.append(athlete_stat_numbs[i])
        else:
            takedown_accuracy.append('N/A')
            striking_accuracy.append('N/A')


data = list(zip(fighter_name, nickname, weight_class, record, knockouts, submissions,
 first_round_finishes, striking_accuracy, takedown_accuracy))
df = pd.DataFrame(data, columns=['Fighter Name', 'Nickname', 'Weight Class', 'Record', 'Knockouts', 'Submissions',
 'First Round Finishes', 'Striking Accuracy', 'Takedown Accuracy']) 



print(weight_class)
print(fighter_name)
print(nickname)
print(knockouts)
print(submissions)
print(first_round_finishes)
print(striking_accuracy)
print(takedown_accuracy)
print(record)

df.fillna('N/A', inplace=True)
print(df)

df.to_csv('test.csv', index=False)