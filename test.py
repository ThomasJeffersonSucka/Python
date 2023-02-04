import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import numpy as np

fighter_urls = ['https://www.ufc.com/athlete/danny-abbadi']

knockouts = []
submissions = []
first_round_finishes = []
striking_accuracy = []
takedown_accuracy = []
fighter_name = []
nickname = []
weight_class = []
record = []
sig_strik_landed_per_min = []
sig_strikes_absorbed_per_min = []
takedown_avg_per_min = []
sub_avg_per_min = []
sig_strik_def = []
takedown_def = []
knockdown_avg = []
avg_fight_time = []

for fighter_url in tqdm(fighter_urls):
    response = requests.get(fighter_url)
    soup = BeautifulSoup(response.text, "html.parser")
    fighter_name_element = soup.find('h1', class_ = 'hero-profile__name').text
    fighter_name.append(fighter_name_element)

    labels = soup.find_all('div', class_ = 'c-stat-compare__label')
    numbers = []
    try:
        numbers = [element.text for element in soup.find_all('div', class_ = 'c-stat-compare__number')]
        if numbers is not None:
            for label, number in zip(labels, numbers):
                sig_strik_landed_per_min.append[number[0]]
                sig_strikes_absorbed_per_min.append[number[1]]
                takedown_avg_per_min.append[number[2]]
                sub_avg_per_min.append[number[3]]
                sig_strik_def.append[number[4]]
                takedown_def.append[number[5]]
                knockdown_avg.append[number[6]]
                avg_fight_time.append[number[7]]
        else:
                sig_strik_landed_per_min.append("N/A")
                sig_strikes_absorbed_per_min.append("N/A")
                takedown_avg_per_min.append("N/A")
                sub_avg_per_min.append("N/A")
                sig_strik_def.append("N/A")
                takedown_def.append("N/A")
                knockdown_avg.append("N/A")
                avg_fight_time.append("N/A")
    except:
        sig_strik_landed_per_min.append("N/A")
        sig_strikes_absorbed_per_min.append("N/A")
        takedown_avg_per_min.append("N/A")
        sub_avg_per_min.append("N/A")
        sig_strik_def.append("N/A")
        takedown_def.append("N/A")
        knockdown_avg.append("N/A")
        avg_fight_time.append("N/A")

    try:
        nickname_element = soup.find('p', class_ = 'hero-profile__nickname').text
        nickname.append(nickname_element)
    except AttributeError:
        nickname.append('None')
        
    try:
        accuracies_labels = []
        accuracies_texts = []
        accuracies_labels = [element.text for element in soup.find_all('h2', class_ = "e-t3")]
        accuracies_texts = [element.text for element in soup.find_all('text', 'e-chart-circle__percent')]
        labels = [label.lower() for label in accuracies_labels]
        if all(any(string in label for label in labels) for string in ["taked", "strik"]):
            print("both accuracies")
            for i, label in enumerate(accuracies_labels):
                if "strik" in label.lower():
                    striking_accuracy.append(accuracies_texts[i])
                if "taked" in label.lower():
                    takedown_accuracy.append(accuracies_texts[i])
        elif all(any(string in label for label in labels) for string in ["taked"]):
            striking_accuracy.append('N/A')
            print("Takedown Accuracy Only")
            for i, label in enumerate(labels):
                if "taked" in label:
                    takedown_accuracy.append(accuracies_texts[i])
        elif all(any(string in label for label in labels) for string in ["strik"]):
            takedown_accuracy.append("N/A")
            print("Striking Accuracy Only")
            for i, label in enumerate(labels):
                if "strik" in label:
                    striking_accuracy.append(accuracies_texts[i])
        elif None(any(string in label for label in labels) for string in ["taked", "strik"]):
            striking_accuracy.append("N/A")
            takedown_accuracy.append("N/A")
            print("No Accuracies")

    except:
        striking_accuracy.append("N/A")
        takedown_accuracy.append("N/A")

    try:
        athlete_stat_labels = []
        athlete_stat_numbs = []
        athlete_stat_labels = [element.text for element in soup.find_all('p', class_ = 'athlete-stats__text athlete-stats__stat-text')]
        athlete_stat_numbs = [element.text for element in soup.find_all('p', class_ = 'athlete-stats__text athlete-stats__stat-numb')]
        labels = [label.lower() for label in athlete_stat_labels]
        if all(any(string in label for label in labels) for string in ["knock", "finish", "subm"]):
            print('all 3')   
            for i, label in enumerate(labels):
                if "knock" in label:
                    knockouts.append(athlete_stat_numbs[i])
                if "subm" in label:
                    submissions.append(athlete_stat_numbs[i])
                if "finish" in label:
                    first_round_finishes.append(athlete_stat_numbs[i])

        elif all(any(string in label for label in labels) for string in ["knock", "subm"]):
            first_round_finishes.append('0')
            print("knock, sub")
            for i, label in enumerate(labels):
                if "knock" in label:
                    knockouts.append(athlete_stat_numbs[i])

        elif all(any(string in label for label in labels) for string in ["knock", "finish"]):
            submissions.append('0')
            print("knock, finish")
            for i, label in enumerate(labels):
                if "knock" in label:
                    knockouts.append(athlete_stat_numbs[i])
                if "finish" in label:
                    first_round_finishes.append(athlete_stat_numbs[i])

        elif all(any(string in label for label in labels) for string in ["knock"]):
            submissions.append('0')
            first_round_finishes.append('0')
            print("knock only")
            for i, label in enumerate(labels):
                if "knock" in label:
                    knockouts.append(athlete_stat_numbs[i])

        elif all(any(string in label for label in labels) for string in ["subm", "finish"]):
            knockouts.append('0')
            print('sub', 'finish')
            for i, label in enumerate(labels):
                if "subm" in label:
                    submissions.append(athlete_stat_numbs[i])
                if "finsih" in label:
                    first_round_finishes.append[i]
        elif all(any(string in label for label in labels) for string in ["subm"]):
            knockouts.append('0')
            first_round_finishes.append('0')
            print("sub only")
            for i, label in enumerate(labels):
                if "subm" in label:
                    submissions.append(athlete_stat_numbs[i])

        elif all(any(string in label for label in labels) for string in ["finish"]):
            knockouts.append('0')
            submissions.append('0')
            print('finish only')
            for i, label in enumerate(labels):
                if "finish" in label:
                    first_round_finishes.append(athlete_stat_numbs[i])
        elif None(any(string in label for label in labels) for string in ["finish", "knock", "subm"]):
            knockouts.append('0')
            submissions.append('0')
            first_round_finishes.append('0')
            print("No Fight Stats")

    except:
        knockouts.append('0')
        submissions.append('0')
        first_round_finishes.append('0')
        print("No Fight Stats")

       
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


data = list(zip(knockouts, submissions, first_round_finishes, striking_accuracy, takedown_accuracy, fighter_name, 
                nickname, weight_class, record, sig_strik_landed_per_min, sig_strikes_absorbed_per_min, 
                takedown_avg_per_min, sub_avg_per_min, sig_strik_def, takedown_def, knockdown_avg, avg_fight_time))

df = pd.DataFrame(data, columns=["Knockouts", "Submissions", "First Round Finishes", "Striking Accuracy","Takedown Accuracy",
 "Fighter Name", "Nickname", "Weight Class", "Record","Significant Strikes Landed per Minute", "Significant Strikes Absorbed per Minute",
 "Takedown Average per Minute", "Submission Average per Minute", "Significant Strike Defense", "Takedown Defense", "Knockdown Average",
 "Average Fight Time"])


print(data)

df.to_csv('test.csv', index=False)