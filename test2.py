# array1 = ['KNOCK','SUBM','FINISH']
# array2 = ['4','5','6']

# if array1 is not None:
#     for i, label in enumerate(array1):
#         if "knock" in label.lower():
#             print(array2[i])
#         elif "finish" in label.lower():
#             print(array2[i])
# else: print('none')

athlete_stat_numbs = ['1','2','3']
athlete_stat_labels = ['strik', 'taked']

takedown_accuracy = []
striking_accuracy = []

if athlete_stat_numbs is not None:
    for i, label in enumerate(athlete_stat_labels):
        if "strik" in label.lower():
            striking_accuracy.append(athlete_stat_numbs[i])
            print(athlete_stat_numbs[i])
        elif "taked" in label.lower():
            takedown_accuracy.append(athlete_stat_numbs[i])
            print(athlete_stat_numbs[i])
else:
    striking_accuracy.append('N/A')
    takedown_accuracy.append('N/A')