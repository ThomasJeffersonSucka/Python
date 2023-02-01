import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import numpy as np

url = 'https://www.ufc.com/athlete/shamil-abdurakhimov'
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

knockouts = []
submissions = []
first_round_finishes = []
striking_accuracy = []
takedown_accuracy = []
fighter_name = []
nickname = []
weight_class = []
record = []

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
athlete_stat_numbs = [element.text for element in soup.find_all(class_ = 'athlete-stats__text athlete-stats__stat-numb')]
athlete_stat_labels = [element.text for element in soup.find_all(class_ = 'athlete-stats__text athlete-stats__stat-text')]
accuracies_labels = [element.text for element in soup.find_all('h2', class_ = "e-t3")]
accuracies_texts = [element.text for element in soup.find_all('text', 'e-chart-circle__percent')]
if len(athlete_stat_numbs) == 3:
    knockouts.append(athlete_stat_numbs[0])
    submissions.append(athlete_stat_numbs[1])
    first_round_finishes.append(athlete_stat_numbs[2])
    print(athlete_stat_numbs[0])
    print(athlete_stat_numbs[1])
    print(athlete_stat_numbs[2])
elif 'knock' in  athlete_stat_labels[0].lower() and 'subm' in athlete_stat_labels[1].lower():
    knockouts.append(athlete_stat_numbs[0])
    submissions.append(athlete_stat_numbs[1])
elif 'knock' in  athlete_stat_labels[0].lower() and 'finish' in athlete_stat_labels[1].lower():
    knockouts.append(athlete_stat_numbs[0])
    first_round_finishes.append(athlete_stat_numbs[0])
elif 'subm' in  athlete_stat_labels[0].lower() and 'finish' in athlete_stat_labels[1].lower():
    submissions.append(athlete_stat_numbs[0])
    first_round_finishes.append(athlete_stat_numbs[0])
elif 'knock' in  athlete_stat_labels[0].lower():
    knockouts.append(athlete_stat_numbs[0])
elif 'subm' in athlete_stat_labels[0].lower():
    submissions.append(athlete_stat_numbs[0])
elif 'finish' in athlete_stat_labels[0].lower():
    first_round_finishes.append(athlete_stat_numbs[0])

if 'strik' in accuracies_labels[0].lower() and 'taked' in accuracies_labels[1].lower():
    striking_accuracy.append(accuracies_texts[0])
    takedown_accuracy.append(accuracies_texts[1])
    print(accuracies_texts[0])
    print(accuracies_texts[1])
elif 'strik' in accuracies_labels[0].lower():
    striking_accuracy.append(accuracies_texts[0])
elif 'taked' in accuracies_labels[0].lower():
    takedown_accuracy.append(accuracies_texts[0])

fighter_name.append(soup.find('h1', class_ = 'hero-profile__name').text)
nickname.append(soup.find('p', class_ = 'hero-profile__nickname').text)
weight_class.append(soup.find('p', class_ = 'hero-profile__division-title').text)
record.append(soup.find('p', class_ = 'hero-profile__division-body').text)

# data = list(zip(fighter_name, nickname, weight_class, record, knockouts, submissions, first_round_finishes, striking_accuracy, takedown_accuracy))
# df = pd.DataFrame(data, columns=['Fighter Name', 'Nickname', 'Weight Class', 'Record' 'Knockouts', 'Submissions', 'First Round Finishes', 'Striking Accuracy',
#  'Takedown Accuracy'])

data = list(zip(fighter_name, nickname, weight_class, record, knockouts, submissions, first_round_finishes, striking_accuracy, takedown_accuracy))
df = pd.DataFrame(data, columns=['Fighter Name', 'Nickname', 'Weight Class', 'Record', 'Knockouts', 'Submissions', 'First Round Finishes', 'Striking Accuracy',
 'Takedown Accuracy'])




print(df)