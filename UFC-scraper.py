import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

first_url = 'https://www.ufc.com/athletes/all?gender=All&search=&page='

page_urls = []
for page in range(0,253):
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


# print(fighter_urls)

name = []
nickname = []
weight_class = []
record = []
knockouts = []
submissions = []
first_round_finishes = []
takedown_accuracy = []
striking_accuracy = []
sig_str_landed_total = []
sig_str_attempted_total = []
takedowns_landed_total = []
takedowns_attempted_total = []
sig_strikes_per_min = []
takedown_avg_per_min = []
sig_str_def = []
knockdown_avg = []
sig_strikes_absorbed_per_min = []
sub_avg_per_min = []
takedown_def = []
avg_fight_time = []
sig_strikes_while_standing = []
sig_strikes_while_clinched = []
sig_strikes_while_grounded = []
win_by_ko_tko = []
win_by_decision = []
win_by_submission = []
sig_strikes_head = []
sig_strikes_body = []
sig_strikes_leg = []


# fighter_urls = ['https://www.ufc.com/athlete/israel-adesanya']

for url in tqdm(fighter_urls):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
 # Name   
    try:
        fighter_name_element = soup.find('h1', class_ = 'hero-profile__name').text
        name.append(fighter_name_element)
    except:
        name.append('None')
    
# loop through  for sig strikes, takedown avg, sig str def, knockdown avg
    try:
        groups1 = soup.find_all("div", class_="c-stat-compare__group c-stat-compare__group-1")
        if groups1:
            for group in groups1:
                # find the label
                label = group.find("div", class_="c-stat-compare__label").text.strip()
                # find the number element
                number = group.find("div", class_="c-stat-compare__number")
                # check if the label is sig strike landed
                if "str. landed" in label.lower():
                    # append N/A if there is no number element
                    if number is None:
                        sig_strikes_per_min.append("N/A")
                    if number:
                        sig_strikes_per_min.append(number.text.strip())
                # check if the label is takedown avg
                elif "taked" in label.lower():
                    # append the text from the number element
                    if number is None:
                        takedown_avg_per_min.append("N/A")
                    if number:
                        takedown_avg_per_min.append(number.text.strip())
                elif "str. def" in label.lower():
                    if number is None:
                        sig_str_def.append("N/A")
                    if number:
                        sig_str_def.append(number.text.strip().replace("\n", "").replace(" ",""))
                elif "knock" in label.lower():
                    if number is None:
                        knockdown_avg.append("N/A")
                    if number:
                        knockdown_avg.append(number.text.strip())
        else:
            sig_strikes_per_min.append("N/A")
            takedown_avg_per_min.append("N/A")
            sig_str_def.append("N/A")
            knockdown_avg.append("N/A")
    except:
        sig_strikes_per_min.append("N/A")
        takedown_avg_per_min.append("N/A")
        sig_str_def.append("N/A")
        knockdown_avg.append("N/A")

#loop through for sig str absorbed, submission avg, takedown def, avg fight time
    try:
        groups2 = soup.find_all("div", class_="c-stat-compare__group c-stat-compare__group-2")
        if groups2:
            for group in groups2:
                # find the label
                label = group.find("div", class_="c-stat-compare__label").text.strip()
                # find the number element
                number = group.find("div", class_="c-stat-compare__number")
                # check if the label is sig strike landed
                if "str. abs" in label.lower():
                    # append N/A if there is no number element
                    if number is None:
                        sig_strikes_absorbed_per_min.append("N/A")
                    if number:
                        sig_strikes_absorbed_per_min.append(number.text.strip())
                # check if the label is takedown avg
                elif "subm" in label.lower():
                    # append the text from the number element
                    if number is None:
                        sub_avg_per_min.append("N/A")
                    if number:
                        sub_avg_per_min.append(number.text.strip())
                elif "takedown def" in label.lower():
                    if number is None:
                        takedown_def.append("N/A")
                    if number:
                        takedown_def.append(number.text.strip().replace("\n", "").replace(" ",""))
                elif "fight time" in label.lower():
                    if number is None:
                        avg_fight_time.append("N/A")
                    if number:
                        avg_fight_time.append(number.text.strip())
        else:
            sig_strikes_absorbed_per_min.append("N/A")
            sub_avg_per_min.append("N/A")
            takedown_def.append("N/A")
            avg_fight_time.append("N/A")
    except:
        sig_strikes_absorbed_per_min.append("N/A")
        sub_avg_per_min.append("N/A")
        takedown_def.append("N/A")
        avg_fight_time.append("N/A")

# looks for sig strik by standing, clinched, grounded
    try:
        groups3 = soup.find_all("div", class_ = 'c-stat-3bar__group')
        if groups3:
            for group in groups3:
                # find the label
                label = group.find("div", class_="c-stat-3bar__label").text.strip()
                # find the number element
                number = group.find("div", class_="c-stat-3bar__value")
                # check if the label is sig strike landed
                if "standing" in label.lower():
                    # append N/A if there is no number element
                    if number is None:
                        sig_strikes_while_standing.append("N/A")
                    if number:
                        sig_strikes_while_standing.append(number.text.strip().replace("\n", "").replace(" ",""))
                # check if the label is takedown avg
                elif "clinch" in label.lower():
                    # append the text from the number element
                    if number is None:
                        sig_strikes_while_clinched.append("N/A")
                    if number:
                        sig_strikes_while_clinched.append(number.text.strip().replace("\n", "").replace(" ",""))
                elif "ground" in label.lower():
                    if number is None:
                        sig_strikes_while_grounded.append("N/A")
                    if number:
                        sig_strikes_while_grounded.append(number.text.strip().replace("\n", "").replace(" ",""))
                elif "tko" in label.lower():
                    if number is None:
                        win_by_ko_tko.append("0(0%)")
                    if number:
                        win_by_ko_tko.append(number.text.strip().replace("\n", "").replace(" ",""))
                elif "dec" in label.lower():
                    if number is None:
                        win_by_decision.append("0(0%)")
                    if number:
                        win_by_decision.append(number.text.strip().replace("\n", "").replace(" ",""))
                elif "sub" in label.lower():
                    if number is None:
                        win_by_submission.append("0(0%)")
                    if number:
                        win_by_submission.append(number.text.strip().replace("\n", "").replace(" ",""))
        else:
            sig_strikes_while_standing.append("N/A")
            sig_strikes_while_clinched.append("N/A")
            sig_strikes_while_grounded.append("N/A")
            win_by_ko_tko.append("0(0%)")
            win_by_decision.append("0(0%)")
            win_by_submission.append("0(0%)")

    except:
        sig_strikes_while_standing.append("N/A")
        sig_strikes_while_clinched.append("N/A")
        sig_strikes_while_grounded.append("N/A")
        win_by_ko_tko.append("0(0%)")
        win_by_decision.append("0(0%)")
        win_by_submission.append("0(0%)")

# sig strikes by target (head, body, leg)
    try:
        sig_str_by_target = soup.find('div', class_ = 'c-stat-body__title')
        if sig_str_by_target:
            sig_strikes_head_total = (soup.find('text', id = 'e-stat-body_x5F__x5F_head_value').text)
            sig_strikes_head_percent = (soup.find('text', id = 'e-stat-body_x5F__x5F_head_percent').text)
            sig_strikes_head.append(sig_strikes_head_total + "(" + sig_strikes_head_percent + ")")
            sig_strikes_body_total = (soup.find('text', id = 'e-stat-body_x5F__x5F_body_value').text)
            sig_strikes_body_percent = (soup.find('text', id = 'e-stat-body_x5F__x5F_body_percent').text)
            sig_strikes_body.append(sig_strikes_body_total.strip().replace("  ","") + "(" + sig_strikes_body_percent.strip().replace("  ","") + ")")
            sig_strikes_leg_total = (soup.find('text', id = 'e-stat-body_x5F__x5F_leg_value').text)
            sig_strikes_leg_percent = (soup.find('text', id = 'e-stat-body_x5F__x5F_leg_percent').text)
            sig_strikes_leg.append(sig_strikes_leg_total + "(" + sig_strikes_leg_percent + ")")
        else:
            sig_strikes_head.append('N/A')
            sig_strikes_body.append('N/A')
            sig_strikes_leg.append('N/A')

    except:
        sig_strikes_head.append('N/A')
        sig_strikes_body.append('N/A')
        sig_strikes_leg.append('N/A')

#gets knockouts, subs, first round wins
    try:
        labels1 =[]
        numbs = []
        labels1 = [element.text for element in soup.find_all("p", class_="athlete-stats__text athlete-stats__stat-text")]
        numbs = [element.text for element in soup.find_all("p", class_="athlete-stats__text athlete-stats__stat-numb")]
        labels2 = [label.lower() for label in labels1]
        if numbs:
            if all(any(string in label for label in labels2) for string in ["knock", "finish", "subm"]):
                for i, label in enumerate(labels2):
                    if "knock" in label:
                        knockouts.append(numbs[i])
                    if "subm" in label:
                        submissions.append(numbs[i])
                    if "finish" in label:
                        first_round_finishes.append(numbs[i])

            elif all(any(string in label for label in labels2) for string in ["knock", "subm"]):
                first_round_finishes.append('0')
                for i, label in enumerate(labels2):
                    if "knock" in label:
                        knockouts.append(numbs[i])
                    if "subm" in label:
                        submissions.append(numbs[i])

            elif all(any(string in label for label in labels2) for string in ["knock", "finish"]):
                submissions.append('0')
                for i, label in enumerate(labels2):
                    if "knock" in label:
                        knockouts.append(numbs[i])
                    if "finish" in label:
                        first_round_finishes.append(numbs[i])

            elif all(any(string in label for label in labels2) for string in ["knock"]):
                submissions.append('0')
                first_round_finishes.append('0')
                for i, label in enumerate(labels2):
                    if "knock" in label:
                        knockouts.append(numbs[i])

            elif all(any(string in label for label in labels2) for string in ["subm", "finish"]):
                knockouts.append('0')
                for i, label in enumerate(labels2):
                    if "subm" in label:
                        submissions.append(numbs[i])
                    if "finish" in label:
                        first_round_finishes.append(numbs[i])

            elif all(any(string in label for label in labels2) for string in ["subm"]):
                knockouts.append('0')
                first_round_finishes.append('0')
                for i, label in enumerate(labels2):
                    if "subm" in label:
                        submissions.append(numbs[i])

            elif all(any(string in label for label in labels2) for string in ["finish"]):
                knockouts.append('0')
                submissions.append('0')
                for i, label in enumerate(labels2):
                    if "finish" in label:
                        first_round_finishes.append(numbs[i])

            elif None(any(string in label for label in labels2) for string in ["finish", "knock", "subm"]):
                knockouts.append('0')
                submissions.append('0')
                first_round_finishes.append('0')
        else:
            knockouts.append('0')
            submissions.append('0')
            first_round_finishes.append('0')
    except:
        knockouts.append("0")
        submissions.append("0")
        first_round_finishes.append("0")

#total strikes landed/attempted, total takedowns landed/attempted
    try:
        labels1 = []
        numbs = []
        labels1 = [element.text for element in soup.find_all('dt', class_ = 'c-overlap__stats-text')]
        numbs = [element.text for element in soup.find_all('dd', class_ = 'c-overlap__stats-value')]
        labels2 = [label.lower() for label in labels1]
        if numbs:
            if all(any(string in label for label in labels2) for string in ["strikes lan", "strikes att", "takedowns lan", "takedowns att"]):
                for i, label in enumerate(labels2):
                    if "strikes landed" in label:
                        sig_str_landed_total.append(numbs[i])
                    if "strikes attempted" in label:
                        sig_str_attempted_total.append(numbs[i])
                    if "takedowns landed" in label:
                        takedowns_landed_total.append(numbs[i])
                    if "takedowns attempted" in label:
                        takedowns_attempted_total.append(numbs[i])

            elif all(any(string in label for label in labels2) for string in ["strikes landed", "strikes attempted"]):
                takedowns_landed_total.append('0')
                takedowns_attempted_total.append('0')
                for i, label in enumerate(labels2):
                    if "strikes landed" in label:
                        sig_str_landed_total.append(numbs[i])
                    if "strikes attempted" in label:
                        sig_str_attempted_total.append(numbs[i])

            elif all(any(string in label for label in labels2) for string in ["takedowns landed", "takedowns attempted"]):
                sig_str_attempted_total.append('0')
                sig_str_landed_total.append('0')
                for i, label in enumerate(labels2):
                    if "takedowns landed" in label:
                        takedowns_landed_total.append(numbs[i])
                    if "takedowns attempted" in label:
                        takedowns_attempted_total.append(numbs[i])

        else:
            sig_str_attempted_total.append('0')
            sig_str_landed_total.append('0')
            takedowns_landed_total.append('0')
            takedowns_attempted_total.append('0')
    
    except:
        sig_str_landed_total.append("N/A")
        sig_str_attempted_total.append("N/A")
        takedowns_landed_total.append("N/A")
        takedowns_attempted_total.append("N/A")

#Striking and takedown accuracy
    try:
        accuracies_labels = [element.text for element in soup.find_all('h2', class_ = "e-t3")]
        accuracies_texts = [element.text for element in soup.find_all('text', 'e-chart-circle__percent')]
        labels = [label.lower() for label in accuracies_labels]
        if accuracies_texts:
            if all(any(string in label for label in labels) for string in ["strik", "taked"]):
                for i, label in enumerate(labels):
                    if "strik" in label:
                        striking_accuracy.append(accuracies_texts[i])
                    elif "taked" in label:
                        takedown_accuracy.append(accuracies_texts[i])
            elif all(any(string in label for label in labels) for string in ["strik"]):
                takedown_accuracy.append('N/A')
                for i, label in enumerate(labels):
                    if "strik" in label:
                        striking_accuracy.append(accuracies_texts[i])
            elif all(any(string in label for label in labels) for string in ["taked"]):
                striking_accuracy.append('N/A')
                for i, label in enumerate(labels):
                    if "taked" in label:
                        takedown_accuracy.append(accuracies_texts[i])
        else:
            striking_accuracy.append('N/A')
            takedown_accuracy.append('N/A')

    except:
        striking_accuracy.append("N/A")
        takedown_accuracy.append("N/A")     
    
    #weight class
    try:
        weight_class_element = soup.find('p', class_ = 'hero-profile__division-title').text
        weight_class.append(weight_class_element)
    except AttributeError:
        weight_class.append('None')

    #nickname
    try:
        nickname_element = soup.find('p', class_ = 'hero-profile__nickname').text.strip()
        nickname.append(nickname_element)
    except AttributeError:
        nickname.append('None')

    #record
    try:
        record_element = soup.find('p', class_ = 'hero-profile__division-body').text.strip()
        record.append(record_element)
    except AttributeError:
        record.append('None')

data = {
    'Name': name,
    'Nickname': nickname,
    'Weight Class': weight_class,
    'Record': record,
    'Knockouts': knockouts,
    'Submissions': submissions,
    'First Round Finishes': first_round_finishes,
    'Striking Accuracy': striking_accuracy,
    'Takedown Accuracy': takedown_accuracy,
    'Sig Str Landed Total': sig_str_landed_total,
    'Sig Str Attempted Total': sig_str_attempted_total,
    'Takedowns Landed Total': takedowns_landed_total,
    'Takedowns Attempted Total': takedowns_attempted_total,
    'Sig Strikes Per Min': sig_strikes_per_min,
    'Takedown Avg Per Min': takedown_avg_per_min,
    'Sig Str Def': sig_str_def,
    'Knockdown Avg': knockdown_avg,
    'Sig Strikes Absorbed Per Min': sig_strikes_absorbed_per_min,
    'Sub Avg Per Min': sub_avg_per_min,
    'Takedown Def': takedown_def,
    'Avg Fight Time': avg_fight_time,
    'Sig Strikes While Standing': sig_strikes_while_standing,
    'Sig Strikes While Clinched': sig_strikes_while_clinched,
    'Sig Strikes While Grounded': sig_strikes_while_grounded,
    'Sig Strikes Head': sig_strikes_head,
    'Sig Strikes Body': sig_strikes_body,
    'Sig Strikes Leg': sig_strikes_leg,
    'Win by KO/TKO': win_by_ko_tko,
    'Win by Decision': win_by_decision,
    'Win by Submission': win_by_submission
}

df = pd.DataFrame(data)

df.to_csv('fighters.csv', index=False)


