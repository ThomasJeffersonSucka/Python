import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import numpy as np

first_url = 'https://www.ufc.com/athletes/all?gender=All&search=&page='

page_urls = []
for page in range(0, 2):
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

# fighter_urls = ['https://www.ufc.com/athlete/shamil-abdurakhimov']
fighter_name = []
nickname = []
weight_class = []
record = []
knockouts = []
submissions = []
first_round_finishes = []
striking_accuracy = []
takedown_accuracy = []
sig_strik_landed_per_min = []
sig_strikes_absorbed_per_min = []
takedown_avg_per_min = []
sub_avg_per_min = []
sig_strik_def = []
takedown_def = []
knockdown_avg = []
avg_fight_time = []
sig_strikes_while_standing = []
sig_strikes_while_clinching = []
sig_strikes_while_grounded = []
sig_strikes_head = []
sig_strikes_body = []
sig_strikes_leg = []
win_by_TKO_KO = []
win_by_decision = []
win_by_submission = []

for fighter_url in tqdm(fighter_urls):
    response = requests.get(fighter_url)
    soup = BeautifulSoup(response.text, "html.parser")
    fighter_name_element = soup.find('h1', class_ = 'hero-profile__name').text
    fighter_name.append(fighter_name_element)
    labels = soup.find_all('div', class_ = 'c-stat-compare__label')
    try:
        sig_strikes_head_total = (soup.find('text', id = 'e-stat-body_x5F__x5F_head_value').text)
        sig_strikes_head_percent = (soup.find('text', id = 'e-stat-body_x5F__x5F_head_percent').text)
        sig_strikes_head.append(sig_strikes_head_total + "(" + sig_strikes_head_percent + ")")
        sig_strikes_body_total = (soup.find('text', id = 'e-stat-body_x5F__x5F_body_value').text)
        sig_strikes_body_percent = (soup.find('text', id = 'e-stat-body_x5F__x5F_body_percent').text)
        sig_strikes_body.append(sig_strikes_body_total.strip().replace("  ","") + "(" + sig_strikes_body_percent.strip().replace("  ","") + ")")
        sig_strikes_leg_total = (soup.find('text', id = 'e-stat-body_x5F__x5F_leg_value').text)
        sig_strikes_leg_percent = (soup.find('text', id = 'e-stat-body_x5F__x5F_leg_percent').text)
        sig_strikes_leg.append(sig_strikes_leg_total + "(" + sig_strikes_leg_percent + ")")
        
        

    # Stats - such as sig strikes landed, absorbed, knockdown avg, fight time, etc
        try:
            numbers = [element.text.strip().replace("\n", "").replace(" ", "") for element in soup.find_all('div', class_ = 'c-stat-compare__number')]
            if len(numbers) == 8:
                sig_strik_landed_per_min.append(numbers[0].strip())
                sig_strikes_absorbed_per_min.append(numbers[1].strip())
                takedown_avg_per_min.append(numbers[2].strip())
                sub_avg_per_min.append(numbers[3].strip())
                sig_strik_def.append(numbers[4].strip())
                takedown_def.append(numbers[5].strip())
                knockdown_avg.append(numbers[6].strip())
                avg_fight_time.append(numbers[7].strip())
            else:   
                    sig_strik_landed_per_min.append("N/A")
                    sig_strikes_absorbed_per_min.append("N/A")
                    takedown_avg_per_min.append("N/A")
                    sub_avg_per_min.append("N/A")
                    sig_strik_def.append("N/A")
                    takedown_def.append("N/A")
                    knockdown_avg.append("N/A")
                    avg_fight_time.append("00:00")

        except (AttributeError, IndexError):
                    sig_strik_landed_per_min.append("N/A")
                    sig_strikes_absorbed_per_min.append("N/A")
                    takedown_avg_per_min.append("N/A")
                    sub_avg_per_min.append("N/A")
                    sig_strik_def.append("N/A")
                    takedown_def.append("N/A")
                    knockdown_avg.append("N/A")
                    avg_fight_time.append("00:00")
    # Sig strikes by position and win by method since they share the same element types
        try:
            sig_strikes_by_position_and_win_methods = [element.text.strip().replace("\n", "").replace(" ", "") for element in soup.find_all('div', class_ = 'c-stat-3bar__value')]
            sig_strikes_while_standing.append(sig_strikes_by_position_and_win_methods[0])
            sig_strikes_while_clinching.append(sig_strikes_by_position_and_win_methods[1])
            sig_strikes_while_grounded.append(sig_strikes_by_position_and_win_methods[2])
            win_by_TKO_KO.append(sig_strikes_by_position_and_win_methods[3])
            win_by_decision.append(sig_strikes_by_position_and_win_methods[4])
            win_by_submission.append(sig_strikes_by_position_and_win_methods[5])
        except (AttributeError, IndexError):
            sig_strikes_while_standing.append("0[0%]")
            sig_strikes_while_clinching.append("0[0%]")
            sig_strikes_while_grounded.append("0[0%]")

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
    except: continue

data = list(zip(fighter_name, nickname, weight_class, record, knockouts, submissions, first_round_finishes, striking_accuracy, takedown_accuracy, sig_strik_landed_per_min, sig_strikes_absorbed_per_min, takedown_avg_per_min, sub_avg_per_min, sig_strik_def, takedown_def, knockdown_avg, avg_fight_time, sig_strikes_while_standing, sig_strikes_while_clinching, sig_strikes_while_grounded, sig_strikes_head, sig_strikes_body, sig_strikes_leg, win_by_TKO_KO, win_by_decision, win_by_submission))
fighter_data = []
for d in data:
    fighter_data.append({
        'Fighter Name': d[0],
        'Nickname': d[1],
        'Weight Class': d[2],
        'Record': d[3],
        'Knockouts': d[4],
        'Submissions': d[5],
        'First Round Finishes': d[6],
        'Striking Accuracy': d[7],
        'Takedown Accuracy': d[8],
        'Significant Strikes Landed per Minute': d[9],
        'Significant Strikes Absorbed per Minute': d[10],
        'Takedown Average per Minute': d[11],
        'Submission Average per Minute': d[12],
        'Significant Strike Defense': d[13],
        'Takedown Defense': d[14],
        'Knockdown Average': d[15],
        'Average Fight Time': d[16],
        'Significant Strikes While Standing': d[17],
        'Significant Strikes While Clinching': d[18],
        'Significant Strikes While Grounded': d[19],
        'Significant Strikes - Head': d[20],
        'Significant Strikes - Body': d[21],
        'Significant Strikes - Leg': d[22],
        'Wins by TKO/KO': d[23],
        'Wins by Decision': d[24],
        'Wins by Submission': d[25]
    })

df = pd.DataFrame(fighter_data)
df.to_csv('fighter_data.csv', index=False)



